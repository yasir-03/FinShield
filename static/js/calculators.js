// FinShield AI — Financial Calculators
// All formulas use standard financial math. Currency is formatted as INR (₹).

function formatINR(amount) {
    if (!isFinite(amount)) return "0";
    return Number(amount).toLocaleString("en-IN", { maximumFractionDigits: 2, minimumFractionDigits: 2 });
}

function renderResult(elementId, rows, highlight) {
    const el = document.getElementById(elementId);
    if (!el) return;
    let html = '<h6 class="text-uppercase small mb-3" style="color:rgba(255,255,255,0.6)">Result</h6>';
    if (highlight) {
        html += `<div class="fs-result-highlight">₹ ${highlight}</div>`;
    }
    rows.forEach(([label, value]) => {
        html += `<div class="fs-result-row"><span class="label">${label}</span><span class="value">${value}</span></div>`;
    });
    el.innerHTML = html;
}

function getVal(id) {
    const el = document.getElementById(id);
    const v = parseFloat(el ? el.value : 0);
    return isNaN(v) ? 0 : v;
}

// ---------------------------------------------------------------------------
// Simple Interest: SI = P * R * T / 100
// ---------------------------------------------------------------------------
function calcSimpleInterest() {
    const p = getVal("si_principal");
    const r = getVal("si_rate");
    const t = getVal("si_time");

    const interest = (p * r * t) / 100;
    const total = p + interest;

    renderResult("si_result", [
        ["Principal Amount", "₹ " + formatINR(p)],
        ["Interest Earned", "₹ " + formatINR(interest)],
        ["Total Amount", "₹ " + formatINR(total)],
    ], formatINR(total));
}

// ---------------------------------------------------------------------------
// Compound Interest: A = P (1 + r/n)^(n*t)
// ---------------------------------------------------------------------------
function calcCompoundInterest() {
    const p = getVal("ci_principal");
    const r = getVal("ci_rate") / 100;
    const t = getVal("ci_time");
    const n = getVal("ci_freq") || 1;

    const amount = p * Math.pow(1 + r / n, n * t);
    const interest = amount - p;

    renderResult("ci_result", [
        ["Principal Amount", "₹ " + formatINR(p)],
        ["Interest Earned", "₹ " + formatINR(interest)],
        ["Maturity Amount", "₹ " + formatINR(amount)],
    ], formatINR(amount));
}

// ---------------------------------------------------------------------------
// EMI: EMI = P * r * (1+r)^n / ((1+r)^n - 1)
// ---------------------------------------------------------------------------
function calcEMI() {
    const p = getVal("emi_principal");
    const annualRate = getVal("emi_rate");
    const years = getVal("emi_years");

    const r = annualRate / 12 / 100;
    const n = years * 12;

    let emi;
    if (r === 0) {
        emi = p / n;
    } else {
        emi = (p * r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);
    }
    const totalPayment = emi * n;
    const totalInterest = totalPayment - p;

    renderResult("emi_result", [
        ["Loan Amount", "₹ " + formatINR(p)],
        ["Total Interest Payable", "₹ " + formatINR(totalInterest)],
        ["Total Payment", "₹ " + formatINR(totalPayment)],
    ], formatINR(emi) + " /month");
}

// ---------------------------------------------------------------------------
// SIP Future Value: FV = P * [((1+i)^n - 1) / i] * (1+i)
// ---------------------------------------------------------------------------
function calcSIP() {
    const monthlyAmount = getVal("sip_amount");
    const annualRate = getVal("sip_rate");
    const years = getVal("sip_years");

    const i = annualRate / 12 / 100;
    const n = years * 12;

    let futureValue;
    if (i === 0) {
        futureValue = monthlyAmount * n;
    } else {
        futureValue = monthlyAmount * ((Math.pow(1 + i, n) - 1) / i) * (1 + i);
    }
    const investedAmount = monthlyAmount * n;
    const gains = futureValue - investedAmount;

    renderResult("sip_result", [
        ["Total Invested", "₹ " + formatINR(investedAmount)],
        ["Estimated Gains", "₹ " + formatINR(gains)],
        ["Maturity Value", "₹ " + formatINR(futureValue)],
    ], formatINR(futureValue));
}

// ---------------------------------------------------------------------------
// Savings Goal: required monthly SIP to reach a target future value
// P = FV / ([((1+i)^n - 1) / i] * (1+i))
// ---------------------------------------------------------------------------
function calcSavingsGoal() {
    const target = getVal("goal_target");
    const years = getVal("goal_years");
    const annualRate = getVal("goal_rate");

    const i = annualRate / 12 / 100;
    const n = years * 12;

    let requiredMonthly;
    if (i === 0) {
        requiredMonthly = n > 0 ? target / n : 0;
    } else {
        const factor = ((Math.pow(1 + i, n) - 1) / i) * (1 + i);
        requiredMonthly = factor > 0 ? target / factor : 0;
    }
    const totalContribution = requiredMonthly * n;

    renderResult("goal_result", [
        ["Target Amount", "₹ " + formatINR(target)],
        ["Total Contribution", "₹ " + formatINR(totalContribution)],
        ["Est. Growth", "₹ " + formatINR(target - totalContribution)],
    ], formatINR(requiredMonthly) + " /month");
}

// ---------------------------------------------------------------------------
// Budget Planner: 50% Needs / 30% Wants / 20% Savings
// ---------------------------------------------------------------------------
function calcBudget() {
    const income = getVal("budget_income");

    const needs = income * 0.5;
    const wants = income * 0.3;
    const savings = income * 0.2;

    renderResult("budget_result", [
        ["Needs (50%)", "₹ " + formatINR(needs)],
        ["Wants (30%)", "₹ " + formatINR(wants)],
        ["Savings & Debt (20%)", "₹ " + formatINR(savings)],
    ], formatINR(income) + " /month");
}
