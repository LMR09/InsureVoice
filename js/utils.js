// ============================================================
// InsureVoice — Utility Helpers
// ============================================================

// ── Star HTML Generator ──
function starsHTML(rating) {
  const full  = Math.floor(rating);
  const empty = 5 - full;
  return '★'.repeat(full) + '☆'.repeat(empty);
}

// ── Format Timestamp ──
function formatDate(timestamp) {
  if (!timestamp) return '';
  const d = timestamp.toDate ? timestamp.toDate() : new Date(timestamp);
  return d.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });
}

// ── Relative Time ──
function relativeTime(timestamp) {
  if (!timestamp) return '';
  const d   = timestamp.toDate ? timestamp.toDate() : new Date(timestamp);
  const now = new Date();
  const sec = Math.floor((now - d) / 1000);
  if (sec < 60)   return 'just now';
  if (sec < 3600) return Math.floor(sec/60) + 'm ago';
  if (sec < 86400)return Math.floor(sec/3600) + 'h ago';
  if (sec < 2592000) return Math.floor(sec/86400) + 'd ago';
  return formatDate(timestamp);
}

// ── Sentiment Badge HTML ──
function sentimentBadge(sentiment) {
  if (!sentiment) return '';
  const map = {
    positive: { cls: 'badge-positive', icon: '😊', label: 'Positive' },
    negative: { cls: 'badge-negative', icon: '😞', label: 'Negative' },
    neutral:  { cls: 'badge-neutral',  icon: '😐', label: 'Neutral'  },
  };
  const s = sentiment.toLowerCase();
  const info = map[s] || map.neutral;
  return `<span class="badge ${info.cls}">${info.icon} ${info.label}</span>`;
}

// ── Claim Status Badge ──
function claimBadge(status) {
  if (!status) return '';
  const map = {
    approved: 'badge-approved',
    rejected: 'badge-rejected',
    delayed:  'badge-delayed',
  };
  const cls = map[status.toLowerCase()] || '';
  return `<span class="badge ${cls}">${status}</span>`;
}

// ── Verified Badge ──
function verifiedBadge(verified) {
  return verified
    ? `<span class="badge badge-verified">✔ Verified</span>`
    : `<span class="badge badge-unverified">⊘ Unverified</span>`;
}

// ── Show Alert ──
function showAlert(containerId, type, message) {
  const el = document.getElementById(containerId);
  if (!el) return;
  el.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
  setTimeout(() => { el.innerHTML = ''; }, 5000);
}

// ── Show/Hide Spinner on Button ──
function setButtonLoading(btn, loading, originalText) {
  if (loading) {
    btn.disabled = true;
    btn.innerHTML = `<span class="spinner"></span> Loading…`;
  } else {
    btn.disabled = false;
    btn.innerHTML = originalText;
  }
}

// ── Truncate Text ──
function truncate(str, n) {
  return str.length > n ? str.slice(0, n) + '…' : str;
}

// ── Insurance Company List ──
const INSURANCE_COMPANIES = [
  'LIC (Life Insurance Corporation)',
  'Star Health Insurance',
  'HDFC ERGO',
  'Bajaj Allianz',
  'New India Assurance',
  'ICICI Lombard',
  'Niva Bupa (Max Bupa)',
  'Reliance General Insurance',
  'United India Insurance',
  'Oriental Insurance',
  'SBI General Insurance',
  'Tata AIG',
  'Future Generali',
  'Digit Insurance',
  'Acko Insurance',
  'Care Health Insurance',
  'Other'
];

// ── Policy Types ──
const POLICY_TYPES = [
  'Health Insurance',
  'Life Insurance',
  'Term Insurance',
  'Vehicle / Motor Insurance',
  'Home Insurance',
  'Travel Insurance',
  'Crop / Agriculture Insurance',
  'Critical Illness Plan',
  'Personal Accident',
  'Group Insurance',
  'Other'
];

// ── Populate Select Options ──
function populateSelect(selectId, options, placeholder = 'Select…') {
  const el = document.getElementById(selectId);
  if (!el) return;
  el.innerHTML = `<option value="" disabled selected>${placeholder}</option>`;
  options.forEach(opt => {
    const o = document.createElement('option');
    o.value = opt; o.textContent = opt;
    el.appendChild(o);
  });
}

// ── Hamburger menu ──
document.addEventListener('DOMContentLoaded', () => {
  const ham = document.getElementById('hamburger');
  const nav = document.getElementById('navLinks');
  if (ham && nav) {
    ham.addEventListener('click', () => {
      nav.classList.toggle('open');
    });
  }
});
