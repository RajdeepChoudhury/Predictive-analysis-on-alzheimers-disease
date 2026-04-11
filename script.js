const form = document.getElementById('diagnosisForm');
const submitBtn = document.getElementById('submitBtn');
const resultBox = document.getElementById('result');
const errorMsg = document.getElementById('errorMsg');
document.getElementById('mmse').addEventListener('input', function () {
    document.getElementById('mmseVal').textContent = this.value;
    updateRangeColor('mmse', this.value, 0, 30);
});
document.getElementById('adl').addEventListener('input', function () {
    document.getElementById('adlVal').textContent = this.value;
    updateRangeColor('adl', this.value, 0, 10);
});
function updateRangeColor(id, val, min, max) {
    const el = document.getElementById(id);
    const pct = ((val - min) / (max - min)) * 100;
    el.style.background = `linear-gradient(to right, var(--accent) ${pct}%, var(--border) ${pct}%)`;
}
updateRangeColor('mmse', 15, 0, 30);
updateRangeColor('adl', 5, 0, 10);
form.addEventListener('submit', async function (e) {
    e.preventDefault();
    hideResult();
    hideError();

    const payload = {
        patient_id: document.getElementById('patient_id').value.trim(),
        age: parseInt(document.getElementById('age').value),
        systolic_bp: parseInt(document.getElementById('systolic_bp').value),
        cholesterol_ldl: parseFloat(document.getElementById('cholesterol_ldl').value),
        mmse: parseInt(document.getElementById('mmse').value),
        functional_assessment: parseFloat(document.getElementById('functional_assessment').value),
        adl: parseInt(document.getElementById('adl').value)
    };

    setLoading(true);

    try {
        const res = await fetch('/api/diagnose', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await res.json();

        if (!res.ok) {
            showError(data.error || 'An unknown error occurred.');
        } else {
            showResult(data);
        }
    } catch (err) {
        showError('Could not connect to the server. Please make sure both servers are running.');
    } finally {
        setLoading(false);
    }
});

function setLoading(state) {
    submitBtn.disabled = state;
    submitBtn.innerHTML = state
        ? '<span class="spinner"></span>Analyzing...'
        : 'Run Diagnosis';
}

function showResult(data) {
    const isPositive = !data.has_alzheimer;
    resultBox.className = `result show ${isPositive ? 'positive' : 'negative'}`;

    document.getElementById('res-icon').textContent = isPositive ? '✓' : '⚠';
    document.getElementById('res-title').textContent = data.diagnosis;
    document.getElementById('res-patient').textContent = `Patient ID: ${data.patient_id}`;

    document.getElementById('stat-mmse').textContent = data.mmse;
    document.getElementById('stat-adl').textContent = data.adl;
    document.getElementById('stat-fa').textContent = data.functional_assessment;

    const riskEl = document.getElementById('risk-badge');
    riskEl.textContent = `● ${data.risk_level} Risk`;
    riskEl.className = `risk-badge ${data.risk_level.toLowerCase()}`;

    const criteriaEl = document.getElementById('criteria-chips');
    criteriaEl.innerHTML = `
        <span class="criteria-chip ${data.criteria_met.mmse_flag ? 'met' : 'not-met'}">
            MMSE ≤ 24: ${data.criteria_met.mmse_flag ? '✗ YES' : '✓ NO'}
        </span>
        <span class="criteria-chip ${data.criteria_met.adl_flag ? 'met' : 'not-met'}">
            ADL ≤ 5: ${data.criteria_met.adl_flag ? '✗ YES' : '✓ NO'}
        </span>
    `;

    resultBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function hideResult() {
    resultBox.className = 'result';
}

function showError(msg) {
    errorMsg.className = 'error-msg show';
    errorMsg.innerHTML = `<span>⚠</span> ${msg}`;
}

function hideError() {
    errorMsg.className = 'error-msg';
}
