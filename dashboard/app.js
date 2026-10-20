/**
 * SoundPulse Analytics — Enterprise BI Operations Controller
 * High-performance, clean JavaScript engine for cohort telemetry,
 * dynamic Star Schema filters, Chart.js visuals, and pagination.
 */

// Application State
let activeRegion = "ALL";
let filteredData = [...MUSIC_DATA];
let chartInstances = {};
let currentPage = 1;
const PAGE_SIZE = 20;

// DOM Elements
const navItems = document.querySelectorAll(".nav-item");
const tabPanes = document.querySelectorAll(".tab-pane");
const pageTitle = document.getElementById("page-title");
const pageSubtitle = document.getElementById("page-subtitle");

const regionSegBtns = document.querySelectorAll(".seg-btn");
const selectPlan = document.getElementById("filter-plan");
const selectSegment = document.getElementById("filter-segment");
const selectChurn = document.getElementById("filter-churn");
const btnReset = document.getElementById("btn-reset");
const btnExport = document.getElementById("btn-export-csv");

const tableSearch = document.getElementById("table-search");
const btnPrevPage = document.getElementById("btn-prev-page");
const btnNextPage = document.getElementById("btn-next-page");
const pageIndicator = document.getElementById("page-num-indicator");
const tableShowingText = document.getElementById("table-showing-text");

// Tab title metadata
const TAB_TITLES = {
  "tab-overview": {
    title: "Executive Operations Overview",
    sub: "240-Respondent Operational Cohort • Unit Economics, Churn & Algorithmic Diagnostics"
  },
  "tab-business-value": {
    title: "Business Value & Decision Engine",
    sub: "Mandatory BL-4 Framework • 5 High-Impact Strategic Interventions & Quantified ROI"
  },
  "tab-star-schema": {
    title: "Data Warehouse Architecture (Star Schema)",
    sub: "Dimensional Model Specification, Conformed Dimensions, and DAX Library for Power BI"
  },
  "tab-cohort": {
    title: "Operational Cohort Telemetry",
    sub: "Granular Survey Profiles, Streaming Frequencies, Unit Margins & Risk Indicators"
  }
};

// Global Chart.js configuration
Chart.defaults.color = "#94a3b8";
Chart.defaults.borderColor = "#171f30";
Chart.defaults.font.family = "'Inter', -apple-system, sans-serif";
Chart.defaults.font.size = 11;

document.addEventListener("DOMContentLoaded", () => {
  setupNavigation();
  setupFilters();
  setupPagination();
  setupExport();
  initCharts();
  refreshDashboard();
});

// ==============================================================================
// Navigation Setup
// ==============================================================================
function setupNavigation() {
  navItems.forEach(item => {
    item.addEventListener("click", () => {
      const targetTab = item.getAttribute("data-tab");
      
      navItems.forEach(n => n.classList.remove("active"));
      tabPanes.forEach(p => p.classList.remove("active"));

      item.classList.add("active");
      const activePane = document.getElementById(targetTab);
      if (activePane) activePane.classList.add("active");

      // Update titles
      if (TAB_TITLES[targetTab]) {
        pageTitle.innerText = TAB_TITLES[targetTab].title;
        pageSubtitle.innerText = TAB_TITLES[targetTab].sub;
      }
    });
  });
}

// ==============================================================================
// Filters Setup
// ==============================================================================
function setupFilters() {
  // Region segmented pill buttons
  regionSegBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      regionSegBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      activeRegion = btn.getAttribute("data-region");
      applyFilters();
    });
  });

  selectPlan.addEventListener("change", applyFilters);
  selectSegment.addEventListener("change", applyFilters);
  selectChurn.addEventListener("change", applyFilters);

  btnReset.addEventListener("click", () => {
    activeRegion = "ALL";
    regionSegBtns.forEach(b => b.classList.toggle("active", b.getAttribute("data-region") === "ALL"));
    selectPlan.value = "ALL";
    selectSegment.value = "ALL";
    selectChurn.value = "ALL";
    if (tableSearch) tableSearch.value = "";
    applyFilters();
  });
}

function applyFilters() {
  const planVal = selectPlan.value;
  const segVal = selectSegment.value;
  const churnVal = selectChurn.value;

  filteredData = MUSIC_DATA.filter(row => {
    const matchReg = activeRegion === "ALL" || row.Location_Region === activeRegion;
    const matchPlan = planVal === "ALL" || row.Subscription_Tier === planVal;
    const matchSeg = segVal === "ALL" || row.User_Segment === segVal;
    const matchChurn = churnVal === "ALL" || row.Churn_Status === churnVal;
    return matchReg && matchPlan && matchSeg && matchChurn;
  });

  currentPage = 1;
  refreshDashboard();
}

function refreshDashboard() {
  updateMetrics();
  updateCharts();
  renderCohortTable();
}

// ==============================================================================
// KPI Metrics Update
// ==============================================================================
function updateMetrics() {
  const data = filteredData;
  const count = data.length;

  if (count === 0) {
    document.getElementById("kpi-revenue").innerText = "₹0.00";
    document.getElementById("kpi-arpu").innerText = "₹0.00 ARPU";
    document.getElementById("kpi-active-users").innerText = "0";
    document.getElementById("kpi-churn-rate").innerText = "0.0%";
    document.getElementById("kpi-margin").innerText = "₹0.00";
    document.getElementById("kpi-hours").innerHTML = `0.0 <span class="unit">hrs</span>`;
    document.getElementById("kpi-nps").innerText = "0";
    return;
  }

  // Revenue & ARPU
  const totalRev = data.reduce((acc, cur) => acc + (cur.Monthly_Total_Revenue_INR || 0), 0);
  const arpu = totalRev / count;
  document.getElementById("kpi-revenue").innerText = `₹${totalRev.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
  document.getElementById("kpi-arpu").innerText = `₹${arpu.toFixed(2)} ARPU`;

  // Active retention
  const activeCount = data.filter(d => d.Churn_Status === "No").length;
  const retentionPct = ((activeCount / count) * 100).toFixed(1);
  document.getElementById("kpi-active-users").innerText = activeCount.toLocaleString();
  document.getElementById("kpi-active-badge").innerText = `${retentionPct}%`;
  document.getElementById("kpi-active-sub").innerText = `${activeCount} Active of ${count} Users`;

  // Churn Rate
  const churnCount = count - activeCount;
  const churnPct = ((churnCount / count) * 100).toFixed(1);
  const churnEl = document.getElementById("kpi-churn-rate");
  churnEl.innerText = `${churnPct}%`;

  const churnBadge = document.getElementById("kpi-churn-badge");
  if (churnPct > 28) {
    churnBadge.className = "metric-badge trend-down";
    churnBadge.innerText = "High Risk";
  } else if (churnPct <= 18) {
    churnBadge.className = "metric-badge trend-up";
    churnBadge.innerText = "Healthy";
  } else {
    churnBadge.className = "metric-badge trend-neutral";
    churnBadge.innerText = "Moderate";
  }

  // Margin & Royalties
  const totalCost = data.reduce((acc, cur) => acc + (cur.Monthly_Licensing_Cost_INR || 0), 0);
  const totalMargin = data.reduce((acc, cur) => acc + (cur.Monthly_Gross_Margin_INR || 0), 0);
  const marginRatio = totalRev > 0 ? ((totalMargin / totalRev) * 100).toFixed(1) : "0.0";
  document.getElementById("kpi-margin").innerText = `₹${totalMargin.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
  document.getElementById("kpi-margin-ratio").innerText = `${marginRatio}%`;
  document.getElementById("kpi-margin-sub").innerText = `After ₹${Math.round(totalCost).toLocaleString('en-IN')} Royalties`;

  // Weekly hours
  const totalHours = data.reduce((acc, cur) => acc + cur.Weekly_Listening_Hours, 0);
  const avgHours = (totalHours / count).toFixed(1);
  document.getElementById("kpi-hours").innerHTML = `${avgHours} <span class="unit">hrs</span>`;
  
  const totalStreams = data.reduce((acc, cur) => acc + cur.Daily_Stream_Count, 0);
  document.getElementById("kpi-streams-meta").innerText = `~${(totalStreams / count).toFixed(1)} streams / day`;

  // Net Promoter Score
  const promoters = data.filter(d => d.NPS_Category === "Promoter").length;
  const detractors = data.filter(d => d.NPS_Category === "Detractor").length;
  const npsScore = Math.round(((promoters - detractors) / count) * 100);
  const npsEl = document.getElementById("kpi-nps");
  npsEl.innerText = npsScore > 0 ? `+${npsScore}` : `${npsScore}`;
  
  const npsBadge = document.getElementById("kpi-nps-badge");
  if (npsScore >= 20) {
    npsBadge.className = "metric-badge trend-up";
    npsBadge.innerText = "Promoter";
  } else if (npsScore < 0) {
    npsBadge.className = "metric-badge trend-down";
    npsBadge.innerText = "Detractor";
  } else {
    npsBadge.className = "metric-badge trend-neutral";
    npsBadge.innerText = "Neutral";
  }
}

// ==============================================================================
// Chart Initialization & Rendering
// ==============================================================================
function initCharts() {
  // Chart 1: Plan Financials (Grouped Bar)
  const ctx1 = document.getElementById("chartPlanFinancials").getContext("2d");
  chartInstances.planFinancials = new Chart(ctx1, {
    type: "bar",
    data: { labels: [], datasets: [] },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "#0d131f",
          borderColor: "#232f48",
          borderWidth: 1,
          padding: 10,
          callbacks: {
            label: (ctx) => ` ${ctx.dataset.label}: ₹${ctx.raw.toFixed(2)}`
          }
        }
      },
      scales: {
        x: { grid: { display: false } },
        y: {
          grid: { color: "#141c2c" },
          ticks: { callback: (val) => `₹${val}` }
        }
      }
    }
  });

  // Chart 2: Churn by Segment (Clean Bar)
  const ctx2 = document.getElementById("chartChurnSegment").getContext("2d");
  chartInstances.churnSegment = new Chart(ctx2, {
    type: "bar",
    data: { labels: [], datasets: [] },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "#0d131f",
          borderColor: "#232f48",
          borderWidth: 1,
          callbacks: {
            label: (ctx) => ` Churn Rate: ${ctx.raw.toFixed(1)}%`
          }
        }
      },
      scales: {
        x: { grid: { display: false } },
        y: {
          grid: { color: "#141c2c" },
          max: 60,
          ticks: { callback: (val) => `${val}%` }
        }
      }
    }
  });

  // Chart 3: Genre Economics (Bar + Line)
  const ctx3 = document.getElementById("chartGenreEconomics").getContext("2d");
  chartInstances.genreEconomics = new Chart(ctx3, {
    type: "bar",
    data: { labels: [], datasets: [] },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "#0d131f",
          borderColor: "#232f48",
          borderWidth: 1
        }
      },
      scales: {
        x: { grid: { display: false } },
        y: {
          type: "linear",
          position: "left",
          grid: { color: "#141c2c" },
          title: { display: true, text: "Avg Monthly Streams", font: { size: 10 } }
        },
        y1: {
          type: "linear",
          position: "right",
          grid: { display: false },
          max: 60,
          title: { display: true, text: "Avg Skip Rate (%)", font: { size: 10 } },
          ticks: { callback: (val) => `${val}%` }
        }
      }
    }
  });

  // Chart 4: Pain Points (Horizontal Bar)
  const ctx4 = document.getElementById("chartPainPoints").getContext("2d");
  chartInstances.painPoints = new Chart(ctx4, {
    type: "bar",
    data: { labels: [], datasets: [] },
    options: {
      indexAxis: "y",
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "#0d131f",
          borderColor: "#232f48",
          borderWidth: 1,
          callbacks: {
            label: (ctx) => ` ${ctx.raw} respondents (${((ctx.raw / (filteredData.length || 1)) * 100).toFixed(1)}%)`
          }
        }
      },
      scales: {
        x: { grid: { color: "#141c2c" } },
        y: { grid: { display: false } }
      }
    }
  });
}

function updateCharts() {
  const data = filteredData;

  // 1. Plan Financials
  const plans = ["Free (Ad-Supported)", "Student Premium", "Individual Premium", "Family Premium"];
  const revArr = [];
  const costArr = [];
  const marginArr = [];

  plans.forEach(plan => {
    const rows = data.filter(d => d.Subscription_Tier === plan);
    const r = rows.reduce((a, b) => a + (b.Monthly_Total_Revenue_INR || 0), 0);
    const c = rows.reduce((a, b) => a + (b.Monthly_Licensing_Cost_INR || 0), 0);
    const m = rows.reduce((a, b) => a + (b.Monthly_Gross_Margin_INR || 0), 0);
    revArr.push(r);
    costArr.push(c);
    marginArr.push(m);
  });

  chartInstances.planFinancials.data = {
    labels: ["Free (Ads)", "Student (₹399)", "Individual (₹879)", "Family (₹1,359)"],
    datasets: [
      { label: "Gross Revenue", data: revArr, backgroundColor: "#10b981", borderRadius: 3, maxBarThickness: 28 },
      { label: "Label Royalties", data: costArr, backgroundColor: "#f43f5e", borderRadius: 3, maxBarThickness: 28 },
      { label: "Net Margin", data: marginArr, backgroundColor: "#38bdf8", borderRadius: 3, maxBarThickness: 28 }
    ]
  };
  chartInstances.planFinancials.update();

  // 2. Churn by Segment
  const segs = ["Student", "Casual Listener", "Young Professional", "Tech Audiophile"];
  const churnArr = segs.map(seg => {
    const sRows = data.filter(d => d.User_Segment === seg);
    if (!sRows.length) return 0;
    const churns = sRows.filter(d => d.Churn_Status === "Yes").length;
    return (churns / sRows.length) * 100;
  });

  chartInstances.churnSegment.data = {
    labels: segs,
    datasets: [{
      data: churnArr,
      backgroundColor: ["#f59e0b", "#38bdf8", "#10b981", "#8b5cf6"],
      borderRadius: 4,
      maxBarThickness: 34
    }]
  };
  chartInstances.churnSegment.update();

  // 3. Genre Streams & Skips
  const genres = ["Pop", "Hip-Hop", "Rock", "Indie/Alternative", "Electronic/EDM", "R&B/Soul", "Classical/Jazz"];
  const streamsArr = [];
  const skipsArr = [];

  genres.forEach(g => {
    const gRows = data.filter(d => d.Favorite_Genre === g);
    if (!gRows.length) {
      streamsArr.push(0);
      skipsArr.push(0);
    } else {
      const avgStr = gRows.reduce((a, b) => a + b.Monthly_Estimated_Streams, 0) / gRows.length;
      const avgSk = gRows.reduce((a, b) => a + b.Skip_Rate_Pct, 0) / gRows.length;
      streamsArr.push(Math.round(avgStr));
      skipsArr.push(parseFloat(avgSk.toFixed(1)));
    }
  });

  chartInstances.genreEconomics.data = {
    labels: ["Pop", "Hip-Hop", "Rock", "Indie", "EDM", "R&B", "Class/Jazz"],
    datasets: [
      {
        type: "bar",
        label: "Avg Monthly Streams",
        data: streamsArr,
        backgroundColor: "rgba(56, 189, 248, 0.4)",
        borderColor: "#38bdf8",
        borderWidth: 1,
        borderRadius: 4,
        yAxisID: "y",
        maxBarThickness: 30
      },
      {
        type: "line",
        label: "Avg Skip Rate %",
        data: skipsArr,
        borderColor: "#f59e0b",
        backgroundColor: "#f59e0b",
        borderWidth: 2,
        pointRadius: 3.5,
        pointHoverRadius: 5,
        yAxisID: "y1"
      }
    ]
  };
  chartInstances.genreEconomics.update();

  // 4. Pain Points
  const painCounts = {};
  data.forEach(d => {
    painCounts[d.Primary_Pain_Point] = (painCounts[d.Primary_Pain_Point] || 0) + 1;
  });

  const sortedPains = Object.entries(painCounts).sort((a, b) => b[1] - a[1]);
  chartInstances.painPoints.data = {
    labels: sortedPains.map(p => p[0]),
    datasets: [{
      data: sortedPains.map(p => p[1]),
      backgroundColor: [
        "#f43f5e",
        "#f59e0b",
        "#fb923c",
        "#818cf8",
        "#38bdf8",
        "#10b981"
      ],
      borderRadius: 4,
      maxBarThickness: 20
    }]
  };
  chartInstances.painPoints.update();
}

// ==============================================================================
// Cohort Table & Pagination
// ==============================================================================
function setupPagination() {
  if (btnPrevPage) {
    btnPrevPage.addEventListener("click", () => {
      if (currentPage > 1) {
        currentPage--;
        renderCohortTable();
      }
    });
  }

  if (btnNextPage) {
    btnNextPage.addEventListener("click", () => {
      const maxPage = Math.ceil(getSearchedData().length / PAGE_SIZE) || 1;
      if (currentPage < maxPage) {
        currentPage++;
        renderCohortTable();
      }
    });
  }

  if (tableSearch) {
    tableSearch.addEventListener("input", () => {
      currentPage = 1;
      renderCohortTable();
    });
  }
}

function getSearchedData() {
  const term = (tableSearch ? tableSearch.value : "").toLowerCase().trim();
  if (!term) return filteredData;
  return filteredData.filter(d =>
    d.User_ID.toLowerCase().includes(term) ||
    d.Customer_Name.toLowerCase().includes(term) ||
    d.Favorite_Genre.toLowerCase().includes(term) ||
    d.Location_Region.toLowerCase().includes(term) ||
    d.Subscription_Tier.toLowerCase().includes(term)
  );
}

function renderCohortTable() {
  const tbody = document.getElementById("table-body");
  if (!tbody) return;

  const dataset = getSearchedData();
  const total = dataset.length;
  const totalPages = Math.ceil(total / PAGE_SIZE) || 1;

  if (currentPage > totalPages) currentPage = totalPages;

  const startIdx = (currentPage - 1) * PAGE_SIZE;
  const pageRows = dataset.slice(startIdx, startIdx + PAGE_SIZE);

  tbody.innerHTML = "";

  if (pageRows.length === 0) {
    tbody.innerHTML = `<tr><td colspan="12" style="text-align: center; color: var(--text-tertiary); padding: 30px;">No matching records found.</td></tr>`;
  } else {
    pageRows.forEach(row => {
      const tr = document.createElement("tr");
      const statusPill = row.Churn_Status === "Yes"
        ? `<span class="status-pill status-pill-churned"><span class="dot"></span>Churned</span>`
        : `<span class="status-pill status-pill-active"><span class="dot"></span>Active</span>`;

      const marginVal = row.Monthly_Gross_Margin_INR !== undefined ? row.Monthly_Gross_Margin_INR : 0;
      const revVal = row.Monthly_Total_Revenue_INR !== undefined ? row.Monthly_Total_Revenue_INR : 0;
      const marginColor = marginVal >= 0 ? "color: #34d399;" : "color: #fb7185;";

      tr.innerHTML = `
        <td class="user-id-code">${row.User_ID}</td>
        <td>${row.Customer_Name}</td>
        <td>${row.Location_Region}</td>
        <td>${row.User_Segment}</td>
        <td>${row.Subscription_Tier}</td>
        <td>${row.Favorite_Genre}</td>
        <td>${row.Weekly_Listening_Hours} hrs</td>
        <td>${row.Skip_Rate_Pct}%</td>
        <td>₹${revVal.toFixed(2)}</td>
        <td style="${marginColor}">₹${marginVal.toFixed(2)}</td>
        <td>${row.NPS_Score}/10</td>
        <td>${statusPill}</td>
      `;
      tbody.appendChild(tr);
    });
  }

  // Update indicators
  if (pageIndicator) pageIndicator.innerText = `Page ${currentPage} of ${totalPages}`;
  if (tableShowingText) {
    const endIdx = Math.min(startIdx + PAGE_SIZE, total);
    tableShowingText.innerText = total === 0 ? "0 records" : `Showing ${startIdx + 1}-${endIdx} of ${total} records`;
  }

  if (btnPrevPage) btnPrevPage.disabled = currentPage <= 1;
  if (btnNextPage) btnNextPage.disabled = currentPage >= totalPages;
}

// ==============================================================================
// Export CSV Functionality
// ==============================================================================
function setupExport() {
  if (!btnExport) return;
  btnExport.addEventListener("click", () => {
    const data = filteredData;
    if (!data.length) return;

    const headers = Object.keys(data[0]);
    let csv = headers.join(",") + "\n";

    data.forEach(row => {
      const values = headers.map(h => {
        const val = row[h];
        if (typeof val === "string" && val.includes(",")) return `"${val}"`;
        return val;
      });
      csv += values.join(",") + "\n";
    });

    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", `SoundPulse_Cohort_Filtered_${new Date().toISOString().slice(0, 10)}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  });
}
