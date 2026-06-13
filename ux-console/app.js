(function () {
  "use strict";

  const payload = window.PORTFOLIO_WORKFLOWS || {
    projects: [],
    portfolio_metrics: [],
    synthetic_label: "[SYNTHETIC — FOR DEMONSTRATION ONLY]",
    human_review_note:
      "Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.",
    publication_classification: "Needs review",
  };

  let activeTab = "Dashboard";
  let activeFilter = "All";
  let requirementsOutput = null;
  let requirementsError = "";
  let selectedFeasibilityCaseId = "SYN-LGT-001";
  let feasibilityResult = null;
  let feasibilityError = "";

  const reviewStorageKey = "aiPortfolioUxConsoleReviewStates";

  const icons = {
    Dashboard: "dashboard",
    "Review Queue": "queue",
    Artifacts: "artifact",
    "Publish Gate": "gate",
  };

  const sampleRequirementCsv = `Requirement_ID,Source_Type,Requirement_Text,Subsystem,Requirement_Type,Verification_Method,Risk_Level,Assumptions,Ambiguity_Flag,Proposed_Test,Human_Review_Status
SYN-REQ-001,Synthetic spec,The lighting module shall operate from 9.0 V to 16.0 V input without loss of commanded function.,Power Input,Electrical,Test,Medium,Nominal 12 V vehicle supply; transient events excluded from this demo,No,Bench input voltage sweep at low/nominal/high values,Needs review
SYN-REQ-002,Synthetic spec,Low beam output shall remain enabled when commanded ON and input voltage is within the normal operating range.,Low Beam,Functional,Test,Medium,Optical performance values are not included in this demo,No,Command low beam ON across voltage cases and log output state,Needs review
SYN-REQ-003,Synthetic spec,High beam output shall remain disabled unless the high beam command is active.,High Beam,Functional,Test,Low,Command source is simulated,No,Command truth-table test for high beam enable/disable,Needs review
SYN-REQ-004,Synthetic notes,The DRL mode shall command reduced current relative to full-intensity operation.,DRL,Functional,Analysis + Test,Medium,Reduction target is synthetic and must be configured per demo case,Yes,Compare commanded current in full and DRL modes,Needs review
SYN-REQ-005,Synthetic spec,The output report shall separate assumptions from verified facts.,Documentation,Process,Inspection,Medium,Facts in demo are generated synthetic values,No,Inspect report sections for assumption and fact separation,Needs review`;

  const feasibilityCases = [
    {
      Case_ID: "SYN-LGT-001",
      Load_Name: "Synthetic two-LED DRL segment",
      Driver_Topology: "Buck LED Driver",
      LED_Count: 2,
      LED_Forward_Voltage_Nom_V: 3.0,
      LED_VF_Tol_pct: 5,
      LED_Current_Nom_A: 0.35,
      Current_Tol_pct: 5,
      Duty_Cycle: 0.8,
      VSupply_Min_V: 9.0,
      VSupply_Max_V: 16.0,
      Driver_Dropout_V: 1.0,
      Driver_Efficiency: 0.9,
      Efficiency_Tol_pct: 3,
      Max_Input_Current_A: 1.2,
      Max_Input_Voltage_V: 40,
      Max_Output_Power_W: 8,
      Board_Thermal_Resistance_C_per_W: 18,
      Max_Driver_Case_Temp_C: 125,
      LED_Thermal_Resistance_C_per_W: 25,
      Max_LED_Junction_Temp_C: 135,
      Ambient_Temp_C: 85,
      Max_Boost_Duty_Cycle: 0.85,
    },
    {
      Case_ID: "SYN-LGT-002",
      Load_Name: "Synthetic three-LED signature",
      Driver_Topology: "Buck LED Driver",
      LED_Count: 3,
      LED_Forward_Voltage_Nom_V: 2.7,
      LED_VF_Tol_pct: 5,
      LED_Current_Nom_A: 0.25,
      Current_Tol_pct: 5,
      Duty_Cycle: 1,
      VSupply_Min_V: 9,
      VSupply_Max_V: 16,
      Driver_Dropout_V: 0.3,
      Driver_Efficiency: 0.9,
      Efficiency_Tol_pct: 3,
      Max_Input_Current_A: 0.8,
      Max_Input_Voltage_V: 40,
      Max_Output_Power_W: 4,
      Board_Thermal_Resistance_C_per_W: 18,
      Max_Driver_Case_Temp_C: 125,
      LED_Thermal_Resistance_C_per_W: 20,
      Max_LED_Junction_Temp_C: 135,
      Ambient_Temp_C: 85,
      Max_Boost_Duty_Cycle: 0.85,
    },
    {
      Case_ID: "SYN-LGT-003",
      Load_Name: "Synthetic long-string signal",
      Driver_Topology: "Boost LED Driver",
      LED_Count: 7,
      LED_Forward_Voltage_Nom_V: 3,
      LED_VF_Tol_pct: 5,
      LED_Current_Nom_A: 0.5,
      Current_Tol_pct: 5,
      Duty_Cycle: 1,
      VSupply_Min_V: 9,
      VSupply_Max_V: 16,
      Driver_Dropout_V: 0,
      Driver_Efficiency: 0.85,
      Efficiency_Tol_pct: 5,
      Max_Input_Current_A: 1.6,
      Max_Input_Voltage_V: 40,
      Max_Output_Power_W: 13,
      Board_Thermal_Resistance_C_per_W: 10,
      Max_Driver_Case_Temp_C: 125,
      LED_Thermal_Resistance_C_per_W: 20,
      Max_LED_Junction_Temp_C: 135,
      Ambient_Temp_C: 95,
      Max_Boost_Duty_Cycle: 0.62,
    },
  ];

  function escapeHtml(value) {
    return String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function slug(value) {
    return String(value || "neutral")
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-|-$/g, "");
  }

  function icon(name, className = "") {
    return `<span class="${className}" aria-hidden="true"><svg><use href="#icon-${name}"></use></svg></span>`;
  }

  function routeProject() {
    const hash = window.location.hash || "";
    return payload.projects.find((project) => project.route === hash) || null;
  }

  function currentToolRoute() {
    const hash = window.location.hash || "";
    if (!hash.startsWith("#tools")) {
      return "";
    }
    return hash.slice(1);
  }

  function artifactHref(path) {
    const safePath = String(path || "").replace(/^\/+/, "");
    const encodedPath = encodeURI(safePath).replace(/#/g, "%23");
    if (safePath.startsWith("ux-console/")) {
      return encodedPath.replace(/^ux-console\//, "");
    }
    return `https://github.com/joeorozco12/Ai_portfolio/blob/main/${encodedPath}`;
  }

  function getReviewStates() {
    try {
      return JSON.parse(localStorage.getItem(reviewStorageKey) || "{}");
    } catch (_) {
      return {};
    }
  }

  function setReviewState(objectId, state) {
    const states = getReviewStates();
    states[objectId] = {
      state,
      run_marker: new Date().toISOString(),
      review_note: state === "Blocked" ? "Demo item blocked for follow-up." : "Demo disposition only.",
    };
    localStorage.setItem(reviewStorageKey, JSON.stringify(states));
  }

  function resetReviewStates() {
    localStorage.removeItem(reviewStorageKey);
  }

  function numeric(value) {
    const parsed = Number(value);
    return Number.isFinite(parsed) ? parsed : 0;
  }

  function pct(value) {
    return numeric(value) / 100;
  }

  function isBoost(topology) {
    return String(topology).toLowerCase().includes("boost");
  }

  function isLinear(topology) {
    return String(topology).toLowerCase().includes("linear");
  }

  function safeRatio(value, limit) {
    const limitValue = numeric(limit);
    if (!limitValue) return null;
    return numeric(value) / limitValue;
  }

  function maxKnown(values) {
    const known = values.filter((value) => value !== null && Number.isFinite(value));
    return known.length ? Math.max(...known) : null;
  }

  function calculateFeasibilityCase(input) {
    const ledStringNom = numeric(input.LED_Count) * numeric(input.LED_Forward_Voltage_Nom_V);
    const ledVfLow = ledStringNom * (1 - pct(input.LED_VF_Tol_pct));
    const ledVfHigh = ledStringNom * (1 + pct(input.LED_VF_Tol_pct));
    const ledCurrentHigh = numeric(input.LED_Current_Nom_A) * (1 + pct(input.Current_Tol_pct));
    const outputPower = ledVfHigh * ledCurrentHigh * numeric(input.Duty_Cycle);
    const efficiencyLow = numeric(input.Driver_Efficiency) * (1 - pct(input.Efficiency_Tol_pct));
    let inputPower;
    let inputCurrentMin;
    let driverLoss;

    if (isLinear(input.Driver_Topology)) {
      inputCurrentMin = ledCurrentHigh * numeric(input.Duty_Cycle);
      driverLoss = Math.max(numeric(input.VSupply_Max_V) - ledVfLow, 0) * inputCurrentMin;
      inputPower = outputPower + driverLoss;
    } else {
      inputPower = outputPower / efficiencyLow;
      inputCurrentMin = inputPower / numeric(input.VSupply_Min_V);
      driverLoss = Math.max(inputPower - outputPower, 0);
    }

    const driverCaseTemp = numeric(input.Ambient_Temp_C) + driverLoss * numeric(input.Board_Thermal_Resistance_C_per_W);
    const ledJunctionTemp = numeric(input.Ambient_Temp_C) + (outputPower / numeric(input.LED_Count)) * numeric(input.LED_Thermal_Resistance_C_per_W);
    const voltageHeadroom = isBoost(input.Driver_Topology)
      ? null
      : numeric(input.VSupply_Min_V) - ledVfHigh - numeric(input.Driver_Dropout_V);
    const boostDuty = isBoost(input.Driver_Topology)
      ? Math.max(0, 1 - (numeric(input.VSupply_Min_V) * efficiencyLow) / ledVfHigh)
      : null;
    const ratios = {
      "input current": safeRatio(inputCurrentMin, input.Max_Input_Current_A),
      "input voltage": safeRatio(input.VSupply_Max_V, input.Max_Input_Voltage_V),
      "output power": safeRatio(outputPower, input.Max_Output_Power_W),
      "driver case temperature": safeRatio(driverCaseTemp, input.Max_Driver_Case_Temp_C),
      "LED junction temperature": safeRatio(ledJunctionTemp, input.Max_LED_Junction_Temp_C),
    };
    const maxRatio = maxKnown(Object.values(ratios));
    const driverTempMargin = numeric(input.Max_Driver_Case_Temp_C) - driverCaseTemp;
    const ledTempMargin = numeric(input.Max_LED_Junction_Temp_C) - ledJunctionTemp;
    const reasons = [];

    for (const [label, ratio] of Object.entries(ratios)) {
      if (ratio !== null && ratio > 1) reasons.push(`${label} ratio ${ratio.toFixed(2)} exceeds synthetic limit`);
    }
    if (voltageHeadroom !== null && voltageHeadroom < 0) reasons.push(`voltage headroom ${voltageHeadroom.toFixed(2)} V is below 0 V`);
    if (boostDuty !== null && boostDuty > numeric(input.Max_Boost_Duty_Cycle)) reasons.push(`boost duty ${boostDuty.toFixed(2)} exceeds synthetic max ${numeric(input.Max_Boost_Duty_Cycle).toFixed(2)}`);
    if (driverTempMargin < 0) reasons.push(`driver temperature margin ${driverTempMargin.toFixed(1)} C is below 0 C`);
    if (ledTempMargin < 0) reasons.push(`LED junction margin ${ledTempMargin.toFixed(1)} C is below 0 C`);

    let status = "Pass";
    if (reasons.length) {
      status = "Fail";
    } else {
      for (const [label, ratio] of Object.entries(ratios)) {
        if (ratio !== null && ratio >= 0.85) reasons.push(`${label} ratio ${ratio.toFixed(2)} is at or above 0.85`);
      }
      if (voltageHeadroom !== null && voltageHeadroom <= 0.75) reasons.push(`voltage headroom ${voltageHeadroom.toFixed(2)} V is 0.75 V or less`);
      if (boostDuty !== null && boostDuty >= 0.85 * numeric(input.Max_Boost_Duty_Cycle)) reasons.push(`boost duty ${boostDuty.toFixed(2)} is near synthetic max`);
      if (driverTempMargin <= 10) reasons.push(`driver temperature margin ${driverTempMargin.toFixed(1)} C is 10 C or less`);
      if (ledTempMargin <= 10) reasons.push(`LED junction margin ${ledTempMargin.toFixed(1)} C is 10 C or less`);
      status = reasons.length ? "Marginal" : "Pass";
    }

    return {
      case_id: input.Case_ID,
      load_name: input.Load_Name,
      topology: input.Driver_Topology,
      output_power_w: outputPower,
      input_current_at_min_v_a: inputCurrentMin,
      voltage_headroom_v: voltageHeadroom,
      boost_duty_cycle: boostDuty,
      driver_case_temp_c: driverCaseTemp,
      led_junction_temp_c: ledJunctionTemp,
      max_ratio: maxRatio,
      driver_temp_margin_c: driverTempMargin,
      led_temp_margin_c: ledTempMargin,
      status,
      reason: reasons.length ? reasons.join("; ") : "All deterministic synthetic feasibility checks are below marginal limits.",
    };
  }

  function parseCsv(text) {
    const rows = [];
    let row = [];
    let value = "";
    let quoted = false;
    for (let i = 0; i < text.length; i += 1) {
      const char = text[i];
      const next = text[i + 1];
      if (char === '"' && quoted && next === '"') {
        value += '"';
        i += 1;
      } else if (char === '"') {
        quoted = !quoted;
      } else if (char === "," && !quoted) {
        row.push(value);
        value = "";
      } else if ((char === "\n" || char === "\r") && !quoted) {
        if (char === "\r" && next === "\n") i += 1;
        row.push(value);
        if (row.some((cell) => cell.trim())) rows.push(row);
        row = [];
        value = "";
      } else {
        value += char;
      }
    }
    row.push(value);
    if (row.some((cell) => cell.trim())) rows.push(row);
    const headers = rows.shift()?.map((header) => header.trim()) || [];
    return rows.map((cells) =>
      Object.fromEntries(headers.map((header, index) => [header, (cells[index] || "").trim()])),
    );
  }

  function generateRequirementsReview(rows) {
    const ambiguity = [];
    const trace = [];
    const assumptions = [];
    const required = [
      "Requirement_ID",
      "Requirement_Text",
      "Subsystem",
      "Requirement_Type",
      "Verification_Method",
      "Assumptions",
      "Ambiguity_Flag",
      "Proposed_Test",
      "Human_Review_Status",
    ];
    if (!rows.length) throw new Error("No requirement rows found.");
    const missing = required.filter((field) => !(field in rows[0]));
    if (missing.length) throw new Error(`Missing required columns: ${missing.join(", ")}`);

    const unitPattern = /\d+(?:\.\d+)?\s*(?:v|volt|volts|a|amp|amps|c|degc|w|watt|watts|%|percent|ms|s)\b/i;
    const numericNeedPattern = /\b(voltage|range|current|temperature|thermal|threshold|reduce|reduced|intensity|limit|minimum|maximum|min|max|exceeds|operate|operating)\b/i;
    const weakTerms = ["adequate", "sufficient", "robust", "minimize", "optimize", "as needed", "TBD", "should", "where appropriate"];
    const methods = ["inspection", "analysis", "test", "demonstration", "review"];

    function addFinding(row, type, explanation, severity = "Medium") {
      ambiguity.push({
        id: `${row.Requirement_ID}-${type}`,
        requirement_id: row.Requirement_ID,
        issue_type: type,
        explanation,
        severity,
        status: "Needs review",
      });
    }

    rows.forEach((row, index) => {
      const text = row.Requirement_Text || "";
      const methodRaw = (row.Verification_Method || "").toLowerCase();
      const recognized = methods.filter((method) => methodRaw.includes(method));
      weakTerms.forEach((term) => {
        if (text.toLowerCase().includes(term.toLowerCase())) addFinding(row, "Weak language", `Contains wording that can be interpreted differently: ${term}.`);
      });
      if (numericNeedPattern.test(text) && !unitPattern.test(text)) addFinding(row, "Missing numeric limits", "Measurable behavior appears without a numeric limit and unit.");
      if (!recognized.length) addFinding(row, "Missing verification method", "No recognized method found.", "High");
      if ((row.Ambiguity_Flag || "").toLowerCase() === "yes") addFinding(row, "Source ambiguity flag", "Source row is marked ambiguous.");
      addFinding(row, "Unclear owner", "No qualified reviewer or owner field is present.", "Low");

      trace.push({
        requirement_id: row.Requirement_ID,
        text: text.slice(0, 110),
        domain: `${row.Subsystem || "Review"} / ${row.Requirement_Type || "Process"}`,
        method: recognized.join(" + ") || "review",
        evidence: row.Proposed_Test ? `${row.Proposed_Test} using synthetic data.` : "Qualified engineer review record.",
        status: "Needs review",
      });
      if (row.Assumptions) {
        assumptions.push({
          id: `SYN-ASM-${String(index + 1).padStart(3, "0")}`,
          requirement_id: row.Requirement_ID,
          statement: row.Assumptions,
          status: "Needs review",
        });
      }
    });

    return {
      rows,
      trace,
      ambiguity,
      assumptions,
      checklist: [
        { area: "Traceability", status: trace.length === rows.length ? "Ready for review" : "Needs review" },
        { area: "Ambiguity", status: ambiguity.length ? "Needs review" : "Ready for review" },
        { area: "Assumptions", status: assumptions.length ? "Needs review" : "Ready for review" },
        { area: "Human review signoff", status: "Needs review" },
      ],
    };
  }

  function downloadJson(filename, value) {
    const blob = new Blob([JSON.stringify(value, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    link.click();
    URL.revokeObjectURL(url);
  }

  function setGlobalLabels(project) {
    document.getElementById("syntheticLabel").textContent =
      project?.synthetic_label || payload.synthetic_label;
    document.getElementById("humanReviewNote").textContent =
      project?.human_review_note || payload.human_review_note;
    document.getElementById("publicationState").textContent =
      project?.publication_classification || payload.publication_classification;
  }

  function renderNav(project) {
    const nav = document.getElementById("projectNav");
    const toolRoute = currentToolRoute();
    const overviewActive = project || toolRoute ? "" : " active";
    const toolsActive = toolRoute === "tools" ? " active" : "";
    const requirementsActive = toolRoute === "tools/requirements" ? " active" : "";
    const feasibilityActive = toolRoute === "tools/feasibility" ? " active" : "";
    const evidenceActive = toolRoute.startsWith("tools/") && !requirementsActive && !feasibilityActive ? " active" : "";
    const links = [
      `<a class="nav-link${toolsActive}" href="#tools">
        ${icon("dashboard", "nav-icon")}
        <span class="nav-title">QR Tools</span>
        <span class="nav-status">public demo</span>
      </a>`,
      `<a class="nav-link${feasibilityActive}" href="#tools/feasibility">
        ${icon("project", "nav-icon")}
        <span class="nav-title">Feasibility Demo</span>
        <span class="nav-status">live</span>
      </a>`,
      `<a class="nav-link${requirementsActive}" href="#tools/requirements">
        ${icon("project", "nav-icon")}
        <span class="nav-title">Req Demo</span>
        <span class="nav-status">live</span>
      </a>`,
      `<a class="nav-link${evidenceActive}" href="#tools/evidence">
        ${icon("artifact", "nav-icon")}
        <span class="nav-title">Evidence</span>
        <span class="nav-status">dashboards</span>
      </a>`,
      `<a class="nav-link${overviewActive}" href="#">
        ${icon("dashboard", "nav-icon")}
        <span class="nav-title">Portfolio Overview</span>
        <span class="nav-status">4 tools</span>
      </a>`,
      ...payload.projects.map((item) => {
        const active = project?.project_id === item.project_id ? " active" : "";
        return `<a class="nav-link${active}" href="${escapeHtml(item.route)}">
          ${icon("project", "nav-icon")}
          <span class="nav-title">${escapeHtml(item.short_title)}</span>
          <span class="nav-status">${escapeHtml(item.publication_classification)}</span>
        </a>`;
      }),
    ];
    nav.innerHTML = links.join("");
  }

  function renderStatusStrip(metrics) {
    const strip = document.getElementById("statusStrip");
    strip.innerHTML = metrics
      .map(
        (item) => `<div class="metric-box ${escapeHtml(item.tone || "")}">
          <span class="metric-label">${escapeHtml(item.label)}</span>
          <span class="metric-value">${escapeHtml(item.value)}</span>
        </div>`,
      )
      .join("");
  }

  function renderTabs(project) {
    const tabBar = document.getElementById("tabBar");
    if (!project) {
      tabBar.innerHTML = "";
      return;
    }
    tabBar.innerHTML = project.screen_tabs
      .map((tab) => {
        const active = activeTab === tab ? " active" : "";
        return `<button class="tab-button${active}" type="button" data-tab="${escapeHtml(tab)}" role="tab" aria-selected="${active ? "true" : "false"}">
          ${icon(icons[tab] || "dashboard", "tab-icon")}
          <span>${escapeHtml(tab)}</span>
        </button>`;
      })
      .join("");
  }

  function renderGateStack(project) {
    const stack = document.getElementById("gateStack");
    const checks = project?.safe_to_publish_checks || [
      { label: "Synthetic/demo label visible", state: "Present" },
      { label: "Human-review note visible", state: "Present" },
      { label: "Project publication review", state: "Needs review" },
    ];
    stack.innerHTML = checks
      .map(
        (check) => `<div class="gate-item">
          <span>${escapeHtml(check.label)}</span>
          ${statePill(check.state)}
        </div>`,
      )
      .join("");
  }

  function statePill(state) {
    return `<span class="state-pill ${slug(state)}">${escapeHtml(state || "Needs review")}</span>`;
  }

  function metric(label, value, tone = "neutral") {
    return { label, value, tone };
  }

  function renderMetricGrid(metrics) {
    return `<div class="metric-grid">
      ${metrics
        .map(
          (item) => `<div class="metric-box ${escapeHtml(item.tone || "")}">
            <span class="metric-label">${escapeHtml(item.label)}</span>
            <span class="metric-value">${escapeHtml(item.value)}</span>
          </div>`,
        )
        .join("")}
    </div>`;
  }

  function renderReviewTable(items) {
    if (!items.length) {
      return `<div class="empty-state">No review items are surfaced for the current filter.</div>`;
    }
    return `<div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Type</th>
            <th>State</th>
            <th>Severity</th>
            <th>Review Work</th>
            <th>Next Action</th>
          </tr>
        </thead>
        <tbody>
          ${items
            .map(
              (item) => `<tr>
                <td><strong>${escapeHtml(item.id)}</strong><small class="review-source">${escapeHtml(item.source)}</small></td>
                <td>${escapeHtml(item.type)}</td>
                <td>${statePill(item.state)}</td>
                <td>${escapeHtml(item.severity)}</td>
                <td>${escapeHtml(item.summary)}</td>
                <td>${escapeHtml(item.recommended_action)}</td>
              </tr>`,
            )
            .join("")}
        </tbody>
      </table>
    </div>`;
  }

  function renderDashboard(project) {
    const previewItems = project.review_items.slice(0, 5);
    return `<div class="dashboard-grid">
      <section class="section-block">
        <div class="section-heading">
          <h2>Workflow Status</h2>
          <span>${escapeHtml(project.publication_classification)}</span>
        </div>
        ${renderMetricGrid(project.metrics)}
      </section>

      <section class="section-block">
        <div class="section-heading">
          <h2>Proof Screens</h2>
          <span>${escapeHtml(project.proof_screens.length)} screens</span>
        </div>
        <div class="proof-list">
          ${project.proof_screens
            .map((screen) => `<div class="proof-item"><span>${escapeHtml(screen)}</span>${statePill("Needs review")}</div>`)
            .join("")}
        </div>
      </section>
    </div>

    <section class="section-block" style="margin-top: 14px;">
      <div class="section-heading">
        <h2>Review Queue Preview</h2>
        <span>${escapeHtml(previewItems.length)} shown</span>
      </div>
      ${renderReviewTable(previewItems)}
    </section>`;
  }

  function renderReviewQueue(project) {
    const filters = [
      "All",
      ...Array.from(new Set(project.review_items.flatMap((item) => [item.type, item.state]))).filter(Boolean),
    ];
    const filtered =
      activeFilter === "All"
        ? project.review_items
        : project.review_items.filter((item) => item.type === activeFilter || item.state === activeFilter);

    return `${renderFilters(filters)}
      ${renderReviewTable(filtered)}`;
  }

  function renderFilters(filters) {
    return `<div class="filter-row" aria-label="Review queue filters">
      ${filters
        .map((filter) => {
          const active = filter === activeFilter ? " active" : "";
          return `<button class="filter-button${active}" type="button" data-filter="${escapeHtml(filter)}">
            ${filter === "All" ? icon("filter", "utility-icon") : ""}
            <span>${escapeHtml(filter)}</span>
          </button>`;
        })
        .join("")}
    </div>`;
  }

  function renderArtifacts(project) {
    return `<div class="artifact-grid">
      ${project.artifacts
        .map(
          (item) => `<a class="artifact-row" href="${artifactHref(item.path)}">
            <span>
              <strong>${escapeHtml(item.label)}</strong>
              <small>${escapeHtml(item.path)}</small>
            </span>
            <span>
              ${statePill(item.status)}
            </span>
          </a>`,
        )
        .join("")}
    </div>`;
  }

  function renderPublishGate(project) {
    const statusRows = Object.entries(project.status_counts || {}).sort((a, b) => b[1] - a[1]);
    return `<div class="publish-grid">
      <section class="section-block">
        <div class="section-heading">
          <h2>Publication Gate</h2>
          <span>${escapeHtml(project.publication_classification)}</span>
        </div>
        <p class="notice">Safe-to-publish remains blocked until synthetic-data, human-review, restricted-detail, and AI-approval wording checks are complete.</p>
        <div class="proof-list">
          ${project.safe_to_publish_checks
            .map((check) => `<div class="proof-item"><span>${escapeHtml(check.label)}</span>${statePill(check.state)}</div>`)
            .join("")}
        </div>
      </section>

      <section class="section-block">
        <div class="section-heading">
          <h2>Source And State Counts</h2>
          <span>${escapeHtml(project.source_paths.length)} inputs</span>
        </div>
        <div class="proof-list">
          ${project.source_paths
            .map((path) => `<div class="source-item"><span>${escapeHtml(path)}</span>${statePill("Present")}</div>`)
            .join("")}
          ${statusRows
            .map(([state, count]) => `<div class="source-item"><span>${escapeHtml(state)}</span><strong>${escapeHtml(count)}</strong></div>`)
            .join("")}
        </div>
      </section>
    </div>`;
  }

  function renderToolsLanding() {
    document.getElementById("pageTitle").textContent = "QR Tools For Interview Review";
    document.getElementById("pageSummary").textContent =
      "Browser-based synthetic demos for selected engineering workflow tools. No login, backend, AI API, or real company data is required.";
    document.getElementById("boundaryText").textContent =
      "The QR route is designed for interview use: all examples are synthetic and every result remains decision-support only.";
    renderStatusStrip([
      metric("Live browser demos", 2),
      metric("Evidence dashboards", 4),
      metric("Backend required", "No"),
      metric("Publication status", "Needs review", "warning"),
    ]);
    renderGateStack(null);
    document.getElementById("tabBar").innerHTML = "";
    document.getElementById("mainPanel").innerHTML = `<div class="tool-grid">
      ${renderToolCard("Lighting Feasibility Simulator", "Edit synthetic LED-driver inputs and recalculate first-pass feasibility status in the browser.", "#tools/feasibility", "Live demo")}
      ${renderToolCard("Requirements-to-Verification", "Paste or load synthetic requirement rows and generate trace, ambiguity, assumption, and checklist summaries.", "#tools/requirements", "Live demo")}
      ${renderToolCard("WCCA Prep Evidence", "Review synthetic WCCA prep outputs, warnings, plots, and review gates.", "#tools/wcca", "Evidence dashboard")}
      ${renderToolCard("Design Review Readiness", "Inspect risk, validation-gap, mode-to-test, and diagnostic evidence generated from synthetic notes.", "#tools/design-review", "Evidence dashboard")}
      ${renderToolCard("Portfolio Evidence", "Open the unified evidence console with screenshots, review states, and publish-gate context.", "#tools/evidence", "Evidence dashboard")}
    </div>
    <section class="section-block" style="margin-top: 14px;">
      <div class="section-heading"><h2>QR Landing Guidance</h2><span>public demo</span></div>
      <div class="proof-list">
        <div class="proof-item"><span>Use one printed QR URL that points to this page after deployment.</span>${statePill("Needs review")}</div>
        <div class="proof-item"><span>Do not paste real employer, customer, supplier, program, part, validation, or internal document data.</span>${statePill("Present")}</div>
        <div class="proof-item"><span>These demos show workflow acceleration only; engineers own final judgment.</span>${statePill("Present")}</div>
      </div>
    </section>`;
  }

  function renderToolCard(title, text, href, label) {
    return `<a class="tool-card" href="${href}">
      <span>${statePill(label)}</span>
      <strong>${escapeHtml(title)}</strong>
      <small>${escapeHtml(text)}</small>
    </a>`;
  }

  function renderFeasibilityTool() {
    const selected = feasibilityCases.find((item) => item.Case_ID === selectedFeasibilityCaseId) || feasibilityCases[0];
    const currentResult = feasibilityResult || calculateFeasibilityCase(selected);
    document.getElementById("pageTitle").textContent = "Lighting Feasibility Simulator";
    document.getElementById("pageSummary").textContent =
      "Edit synthetic load-case inputs and recalculate first-pass electrical and thermal feasibility status in-browser.";
    document.getElementById("boundaryText").textContent =
      "Pass means first-pass screen only. This browser demo does not approve engineering decisions or replace detailed analysis.";
    renderStatusStrip([
      metric("Status", currentResult.status, currentResult.status === "Pass" ? "success" : "warning"),
      metric("Output power W", currentResult.output_power_w.toFixed(2)),
      metric("Input current A", currentResult.input_current_at_min_v_a.toFixed(2)),
      metric("Max ratio", currentResult.max_ratio?.toFixed(2) || "N/A"),
      metric("LED temp C", currentResult.led_junction_temp_c.toFixed(1)),
    ]);
    renderGateStack(payload.projects.find((project) => project.project_id === "lighting-feasibility"));
    document.getElementById("tabBar").innerHTML = "";
    document.getElementById("mainPanel").innerHTML = `<div class="tool-layout">
      <section class="section-block">
        <div class="section-heading"><h2>Synthetic Case Inputs</h2><span>${escapeHtml(selected.Case_ID)}</span></div>
        <form id="feasibilityForm" class="input-grid">
          <label>Case<select name="Case_ID">${feasibilityCases.map((item) => `<option value="${item.Case_ID}" ${item.Case_ID === selected.Case_ID ? "selected" : ""}>${item.Case_ID} - ${escapeHtml(item.Load_Name)}</option>`).join("")}</select></label>
          ${renderNumericInput("LED_Count", selected.LED_Count, "LED count")}
          ${renderNumericInput("LED_Forward_Voltage_Nom_V", selected.LED_Forward_Voltage_Nom_V, "LED VF nom V")}
          ${renderNumericInput("LED_Current_Nom_A", selected.LED_Current_Nom_A, "LED current A")}
          ${renderNumericInput("Duty_Cycle", selected.Duty_Cycle, "Duty cycle")}
          ${renderNumericInput("VSupply_Min_V", selected.VSupply_Min_V, "Min supply V")}
          ${renderNumericInput("Driver_Efficiency", selected.Driver_Efficiency, "Efficiency")}
          ${renderNumericInput("Ambient_Temp_C", selected.Ambient_Temp_C, "Ambient C")}
          ${renderNumericInput("Max_Output_Power_W", selected.Max_Output_Power_W, "Max output W")}
          ${renderNumericInput("Max_LED_Junction_Temp_C", selected.Max_LED_Junction_Temp_C, "Max LED TJ C")}
          <input type="hidden" name="Load_Name" value="${escapeHtml(selected.Load_Name)}">
          <input type="hidden" name="Driver_Topology" value="${escapeHtml(selected.Driver_Topology)}">
          ${hiddenFeasibilityFields(selected)}
        </form>
        <div class="button-row">
          <button class="action-link" type="button" data-action="run-feasibility">Run screening</button>
          <button class="action-link" type="button" data-action="download-feasibility">Download JSON</button>
        </div>
        ${feasibilityError ? `<p class="notice">${escapeHtml(feasibilityError)}</p>` : ""}
      </section>
      <section class="section-block">
        <div class="section-heading"><h2>Screening Result</h2>${statePill(currentResult.status)}</div>
        <div class="proof-list">
          <div class="proof-item"><span>Reason</span><strong>${escapeHtml(currentResult.reason)}</strong></div>
          <div class="proof-item"><span>Voltage headroom</span><strong>${currentResult.voltage_headroom_v === null ? "N/A" : `${currentResult.voltage_headroom_v.toFixed(2)} V`}</strong></div>
          <div class="proof-item"><span>Boost duty</span><strong>${currentResult.boost_duty_cycle === null ? "N/A" : currentResult.boost_duty_cycle.toFixed(2)}</strong></div>
          <div class="proof-item"><span>Driver temp margin</span><strong>${currentResult.driver_temp_margin_c.toFixed(1)} C</strong></div>
          <div class="proof-item"><span>LED temp margin</span><strong>${currentResult.led_temp_margin_c.toFixed(1)} C</strong></div>
        </div>
      </section>
    </div>`;
  }

  function renderNumericInput(name, value, label) {
    return `<label>${escapeHtml(label)}<input type="number" step="any" name="${escapeHtml(name)}" value="${escapeHtml(value)}"></label>`;
  }

  function hiddenFeasibilityFields(selected) {
    const visible = new Set(["Case_ID", "Load_Name", "Driver_Topology", "LED_Count", "LED_Forward_Voltage_Nom_V", "LED_Current_Nom_A", "Duty_Cycle", "VSupply_Min_V", "Driver_Efficiency", "Ambient_Temp_C", "Max_Output_Power_W", "Max_LED_Junction_Temp_C"]);
    return Object.entries(selected)
      .filter(([key]) => !visible.has(key))
      .map(([key, value]) => `<input type="hidden" name="${escapeHtml(key)}" value="${escapeHtml(value)}">`)
      .join("");
  }

  function formToFeasibilityCase() {
    const form = document.getElementById("feasibilityForm");
    const data = Object.fromEntries(new FormData(form).entries());
    selectedFeasibilityCaseId = data.Case_ID;
    const selected = feasibilityCases.find((item) => item.Case_ID === selectedFeasibilityCaseId) || feasibilityCases[0];
    return { ...selected, ...data };
  }

  function renderRequirementsTool() {
    document.getElementById("pageTitle").textContent = "Requirements-to-Verification Demo";
    document.getElementById("pageSummary").textContent =
      "Paste synthetic CSV rows and generate trace, ambiguity, assumption, and review-checklist summaries in the browser.";
    document.getElementById("boundaryText").textContent =
      "This browser demo rejects real company data by policy; use only synthetic/demo-safe rows.";
    renderStatusStrip([
      metric("Rows", requirementsOutput?.rows.length || 0),
      metric("Trace rows", requirementsOutput?.trace.length || 0),
      metric("Ambiguity findings", requirementsOutput?.ambiguity.length || 0, requirementsOutput?.ambiguity.length ? "warning" : "neutral"),
      metric("Assumptions", requirementsOutput?.assumptions.length || 0, requirementsOutput?.assumptions.length ? "warning" : "neutral"),
      metric("Publication", "Needs review", "warning"),
    ]);
    renderGateStack(payload.projects.find((project) => project.project_id === "requirements-to-verification"));
    document.getElementById("tabBar").innerHTML = "";
    document.getElementById("mainPanel").innerHTML = `<div class="tool-layout">
      <section class="section-block">
        <div class="section-heading"><h2>Synthetic CSV Input</h2><span>browser only</span></div>
        <div class="form-stack">
          <textarea id="requirementsCsv" rows="12">${escapeHtml(document.getElementById("requirementsCsv")?.value || sampleRequirementCsv)}</textarea>
          <label class="check-row"><input id="syntheticConfirm" type="checkbox" checked> I confirm this is synthetic/demo-safe input.</label>
          <div class="button-row">
            <button class="action-link" type="button" data-action="run-requirements">Generate review package</button>
            <button class="action-link" type="button" data-action="reset-requirements">Reset sample</button>
            <button class="action-link" type="button" data-action="download-requirements">Download JSON</button>
          </div>
          ${requirementsError ? `<p class="notice">${escapeHtml(requirementsError)}</p>` : ""}
        </div>
      </section>
      <section class="section-block">
        <div class="section-heading"><h2>Generated Summary</h2>${statePill("Needs review")}</div>
        ${requirementsOutput ? renderRequirementsOutput(requirementsOutput) : `<div class="empty-state">Run the synthetic CSV demo to generate review artifacts.</div>`}
      </section>
    </div>`;
  }

  function renderRequirementsOutput(output) {
    return `<div class="proof-list">
      <div class="proof-item"><span>Trace rows</span><strong>${output.trace.length}</strong></div>
      <div class="proof-item"><span>Ambiguity findings</span><strong>${output.ambiguity.length}</strong></div>
      <div class="proof-item"><span>Assumptions</span><strong>${output.assumptions.length}</strong></div>
      <div class="proof-item"><span>Checklist items</span><strong>${output.checklist.length}</strong></div>
    </div>
    ${renderReviewTable(output.ambiguity.slice(0, 6).map((item) => ({
      id: item.id,
      type: item.issue_type,
      source: item.requirement_id,
      state: item.status,
      severity: item.severity,
      summary: item.explanation,
      recommended_action: "Record reviewer disposition before export.",
    })))}`;
  }

  function renderEvidenceTool(projectId = "") {
    const project = projectId ? payload.projects.find((item) => item.project_id === projectId) : null;
    if (project) {
      renderProject(project);
      return;
    }
    document.getElementById("pageTitle").textContent = "Portfolio Evidence Dashboards";
    document.getElementById("pageSummary").textContent =
      "Guided evidence dashboards for WCCA prep, design-review readiness, screenshots, and local reviewer-demo state.";
    document.getElementById("boundaryText").textContent =
      "Reviewer-demo decisions are stored only in this browser. They do not modify generated artifacts.";
    renderStatusStrip(payload.portfolio_metrics);
    renderGateStack(null);
    document.getElementById("tabBar").innerHTML = "";
    const states = getReviewStates();
    const reviewItems = payload.projects.flatMap((projectItem) =>
      projectItem.review_items.slice(0, 3).map((item) => ({ ...item, project_id: projectItem.project_id })),
    );
    document.getElementById("mainPanel").innerHTML = `<div class="tool-grid">
      ${renderToolCard("Open WCCA Evidence", "Filter synthetic WCCA rows, warnings, artifacts, and gates.", "#tools/wcca", "Evidence dashboard")}
      ${renderToolCard("Open Design Review Evidence", "Inspect risk and readiness artifacts from synthetic notes.", "#tools/design-review", "Evidence dashboard")}
      ${renderToolCard("Open Full Console", "Review all four project evidence routes.", "#", "Evidence dashboard")}
    </div>
    <section class="section-block" style="margin-top: 14px;">
      <div class="section-heading"><h2>Local Reviewer Demo State</h2><button class="action-link" type="button" data-action="reset-review-state">Reset local state</button></div>
      <div class="table-wrap"><table><thead><tr><th>Item</th><th>Project</th><th>State</th><th>Demo Actions</th></tr></thead><tbody>
        ${reviewItems.map((item) => {
          const current = states[item.id]?.state || item.state;
          return `<tr><td><strong>${escapeHtml(item.id)}</strong><small class="review-source">${escapeHtml(item.summary)}</small></td><td>${escapeHtml(item.project_id)}</td><td>${statePill(current)}</td><td><div class="button-row compact"><button class="action-link" data-review-id="${escapeHtml(item.id)}" data-review-state="Needs review">Needs review</button><button class="action-link" data-review-id="${escapeHtml(item.id)}" data-review-state="Reviewed demo">Reviewed demo</button><button class="action-link" data-review-id="${escapeHtml(item.id)}" data-review-state="Blocked">Blocked</button></div></td></tr>`;
        }).join("")}
      </tbody></table></div>
    </section>`;
  }

  function renderOverview() {
    document.getElementById("pageTitle").textContent = "Engineering Workflow Portfolio Console";
    document.getElementById("pageSummary").textContent =
      "A unified local shell for four synthetic automotive-lighting workflow tools, centered on generated evidence, review queues, export readiness, and publication gates.";
    document.getElementById("boundaryText").textContent = payload.review_log_policy;
    renderStatusStrip(payload.portfolio_metrics);
    renderGateStack(null);

    const projectRows = payload.projects
      .map(
        (project) => `<tr>
          <td><a href="${escapeHtml(project.route)}"><strong>${escapeHtml(project.title)}</strong></a></td>
          <td>${escapeHtml(project.workflow_summary)}</td>
          <td>${escapeHtml(project.review_items.length)}</td>
          <td>${escapeHtml(project.artifacts.length)}</td>
          <td>${statePill(project.publication_classification)}</td>
        </tr>`,
      )
      .join("");

    document.getElementById("mainPanel").innerHTML = `<section class="section-block">
      <div class="section-heading">
        <h2>Project Workflows</h2>
        <span>${escapeHtml(payload.projects.length)} projects</span>
      </div>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Project</th>
              <th>Workflow</th>
              <th>Review Items</th>
              <th>Artifacts</th>
              <th>Publication</th>
            </tr>
          </thead>
          <tbody>${projectRows}</tbody>
        </table>
      </div>
    </section>`;
  }

  function renderProject(project) {
    document.getElementById("pageTitle").textContent = project.title;
    document.getElementById("pageSummary").textContent = project.workflow_summary;
    document.getElementById("boundaryText").textContent = project.project_boundary;
    renderStatusStrip(project.metrics);
    renderGateStack(project);

    const panel = document.getElementById("mainPanel");
    if (activeTab === "Review Queue") {
      panel.innerHTML = renderReviewQueue(project);
    } else if (activeTab === "Artifacts") {
      panel.innerHTML = renderArtifacts(project);
    } else if (activeTab === "Publish Gate") {
      panel.innerHTML = renderPublishGate(project);
    } else {
      panel.innerHTML = renderDashboard(project);
    }
  }

  function render() {
    const project = routeProject();
    const toolRoute = currentToolRoute();
    setGlobalLabels(project);
    renderNav(project);
    renderTabs(project);
    if (toolRoute === "tools") {
      renderToolsLanding();
    } else if (toolRoute === "tools/feasibility") {
      renderFeasibilityTool();
    } else if (toolRoute === "tools/requirements") {
      renderRequirementsTool();
    } else if (toolRoute === "tools/wcca") {
      renderEvidenceTool("wcca-prep");
    } else if (toolRoute === "tools/design-review") {
      renderEvidenceTool("design-review-readiness");
    } else if (toolRoute === "tools/evidence") {
      renderEvidenceTool();
    } else if (project) {
      renderProject(project);
    } else {
      renderOverview();
    }
  }

  document.addEventListener("click", (event) => {
    const actionButton = event.target.closest("[data-action]");
    if (actionButton) {
      const action = actionButton.dataset.action;
      if (action === "run-feasibility") {
        try {
          feasibilityError = "";
          feasibilityResult = calculateFeasibilityCase(formToFeasibilityCase());
        } catch (error) {
          feasibilityError = error.message;
        }
        render();
      } else if (action === "download-feasibility") {
        const result = feasibilityResult || calculateFeasibilityCase(formToFeasibilityCase());
        downloadJson("synthetic-feasibility-demo.json", {
          synthetic_label: payload.synthetic_label,
          human_review_note: payload.human_review_note,
          publication_classification: "Needs review",
          result,
        });
      } else if (action === "run-requirements") {
        const confirmed = document.getElementById("syntheticConfirm")?.checked;
        if (!confirmed) {
          requirementsError = "Confirm the input is synthetic/demo-safe before processing.";
          requirementsOutput = null;
        } else {
          try {
            requirementsError = "";
            requirementsOutput = generateRequirementsReview(parseCsv(document.getElementById("requirementsCsv").value));
          } catch (error) {
            requirementsError = error.message;
            requirementsOutput = null;
          }
        }
        render();
      } else if (action === "reset-requirements") {
        requirementsError = "";
        requirementsOutput = null;
        const textarea = document.getElementById("requirementsCsv");
        if (textarea) textarea.value = sampleRequirementCsv;
        render();
      } else if (action === "download-requirements") {
        if (requirementsOutput) {
          downloadJson("synthetic-requirements-review-demo.json", {
            synthetic_label: payload.synthetic_label,
            human_review_note: payload.human_review_note,
            publication_classification: "Needs review",
            ...requirementsOutput,
          });
        }
      } else if (action === "reset-review-state") {
        resetReviewStates();
        render();
      }
      return;
    }

    const reviewButton = event.target.closest("[data-review-id]");
    if (reviewButton) {
      setReviewState(reviewButton.dataset.reviewId, reviewButton.dataset.reviewState);
      render();
      return;
    }

    const tabButton = event.target.closest("[data-tab]");
    if (tabButton) {
      activeTab = tabButton.dataset.tab;
      activeFilter = "All";
      render();
      return;
    }

    const filterButton = event.target.closest("[data-filter]");
    if (filterButton) {
      activeFilter = filterButton.dataset.filter;
      render();
    }
  });

  document.addEventListener("change", (event) => {
    const caseSelect = event.target.closest('select[name="Case_ID"]');
    if (caseSelect) {
      selectedFeasibilityCaseId = caseSelect.value;
      feasibilityResult = null;
      feasibilityError = "";
      render();
    }
  });

  window.addEventListener("hashchange", () => {
    activeTab = "Dashboard";
    activeFilter = "All";
    render();
  });

  render();
})();
