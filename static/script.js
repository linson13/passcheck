const form = document.getElementById('tailor-form');
const dropzone = document.getElementById('dropzone');
const dropzoneInner = document.getElementById('dropzone-inner');
const resumeInput = document.getElementById('resume-input');
const jdInput = document.getElementById('jd-input');
const submitBtn = document.getElementById('submit-btn');
const errorMsg = document.getElementById('error-msg');

const intakeSection = document.getElementById('intake-section');
const processingSection = document.getElementById('processing-section');
const resultsSection = document.getElementById('results-section');
const gateStatus = document.getElementById('gate-status');

const scoreBefore = document.getElementById('score-before');
const scoreAfter = document.getElementById('score-after');
const improvementText = document.getElementById('improvement-text');
const downloadBtn = document.getElementById('download-btn');
const resetBtn = document.getElementById('reset-btn');

let selectedFile = null;
let selectedTemplate = null;
const templateGrid = document.getElementById('template-grid');

// ---- Load templates on page load ----
async function loadTemplates() {
  try {
    const res = await fetch('/api/templates');
    const data = await res.json();
    selectedTemplate = data.default;
    renderTemplateGrid(data.templates, data.default);
  } catch (err) {
    templateGrid.innerHTML = '<p class="hint">Couldn\'t load templates — the default will be used.</p>';
    selectedTemplate = 'classic';
  }
}

function renderTemplateGrid(templates, defaultId) {
  templateGrid.innerHTML = '';
  templates.forEach((t) => {
    const card = document.createElement('div');
    card.className = 'template-card' + (t.id === defaultId ? ' selected' : '');
    card.dataset.templateId = t.id;
    card.innerHTML = `
      <div class="tpl-thumb-wrap">
        <img class="tpl-thumb" src="/template-previews/${t.id}.png" alt="${escapeHtml(t.name)} template preview" loading="lazy">
        <span class="tpl-zoom-hint">view larger</span>
      </div>
      <p class="tpl-name">${escapeHtml(t.name)}</p>
      <p class="tpl-desc">${escapeHtml(t.description)}</p>
    `;
    card.addEventListener('click', (e) => {
      selectedTemplate = t.id;
      document.querySelectorAll('.template-card').forEach(c => c.classList.remove('selected'));
      card.classList.add('selected');
    });
    card.querySelector('.tpl-thumb-wrap').addEventListener('click', (e) => {
      e.stopPropagation();
      openLightbox(`/template-previews/${t.id}.png`, t.name);
    });
    templateGrid.appendChild(card);
  });
}

function openLightbox(src, name) {
  const overlay = document.createElement('div');
  overlay.className = 'lightbox-overlay';
  overlay.innerHTML = `
    <div class="lightbox-inner">
      <img src="${src}" alt="${escapeHtml(name)} template, full preview">
      <p class="lightbox-caption">${escapeHtml(name)} — click anywhere to close</p>
    </div>
  `;
  overlay.addEventListener('click', () => overlay.remove());
  document.body.appendChild(overlay);
}

loadTemplates();

// ---- Dropzone interactions ----
dropzone.addEventListener('click', () => resumeInput.click());

dropzone.addEventListener('dragover', (e) => {
  e.preventDefault();
  dropzone.classList.add('dragover');
});
dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));
dropzone.addEventListener('drop', (e) => {
  e.preventDefault();
  dropzone.classList.remove('dragover');
  if (e.dataTransfer.files.length) {
    setFile(e.dataTransfer.files[0]);
  }
});

resumeInput.addEventListener('change', () => {
  if (resumeInput.files.length) setFile(resumeInput.files[0]);
});

function setFile(file) {
  const allowed = ['.pdf', '.docx', '.txt'];
  const ext = '.' + file.name.split('.').pop().toLowerCase();
  if (!allowed.includes(ext)) {
    showError('Please choose a .pdf, .docx, or .txt file.');
    return;
  }
  if (file.size > 5 * 1024 * 1024) {
    showError('That file is over 5MB — try a smaller version.');
    return;
  }
  selectedFile = file;
  dropzone.classList.add('has-file');
  dropzoneInner.innerHTML = `
    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M9 12l2 2 4-4m5 2a9 9 0 1 1-18 0 9 9 0 0 1 18 0z"/></svg>
    <p><strong>${escapeHtml(file.name)}</strong></p>
    <p class="hint">Click to choose a different file</p>
  `;
  clearError();
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

function showError(msg) {
  errorMsg.textContent = msg;
}
function clearError() {
  errorMsg.textContent = '';
}

// ---- Form submit ----
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  clearError();

  if (!selectedFile) {
    showError('Please upload your resume first.');
    return;
  }
  if (!jdInput.value.trim()) {
    showError('Please paste the job description.');
    return;
  }

  submitBtn.disabled = true;
  intakeSection.hidden = true;
  processingSection.hidden = false;

  const statuses = [
    'Reading your resume…',
    'Parsing the job description…',
    'Tailoring your resume to the role…',
    'Scoring against the ATS filter…',
  ];
  let statusIdx = 0;
  gateStatus.textContent = statuses[0];
  const statusTimer = setInterval(() => {
    statusIdx = Math.min(statusIdx + 1, statuses.length - 1);
    gateStatus.textContent = statuses[statusIdx];
  }, 3500);

  try {
    const formData = new FormData();
    formData.append('resume', selectedFile);
    formData.append('jd_text', jdInput.value);
    formData.append('template', selectedTemplate || 'classic');

    const res = await fetch('/api/tailor', { method: 'POST', body: formData });
    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.detail || 'Something went wrong. Please try again.');
    }

    clearInterval(statusTimer);
    showResults(data);
  } catch (err) {
    clearInterval(statusTimer);
    processingSection.hidden = true;
    intakeSection.hidden = false;
    submitBtn.disabled = false;
    showError(err.message || 'Something went wrong. Please try again.');
  }
});

function showResults(data) {
  const { original_score, tailored_score, improvement } = data.ats_report;

  scoreBefore.textContent = `${original_score}%`;
  scoreAfter.textContent = `${tailored_score}%`;
  improvementText.textContent = `+${improvement} points after tailoring`;
  downloadBtn.href = data.download_url;

  processingSection.hidden = true;
  resultsSection.hidden = false;
}

resetBtn.addEventListener('click', () => {
  selectedFile = null;
  resumeInput.value = '';
  jdInput.value = '';
  dropzone.classList.remove('has-file');
  dropzoneInner.innerHTML = `
    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 3v12m0-12 4 4m-4-4-4 4M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2"/></svg>
    <p><strong>Drop your resume</strong> or click to browse</p>
    <p class="hint">.pdf · .docx · .txt — up to 5MB</p>
  `;
  submitBtn.disabled = false;
  resultsSection.hidden = true;
  intakeSection.hidden = false;
});
