window.PORTFOLIO_WORKFLOWS = {
  "generated_from": "tools/generate_ux_console_data.py",
  "synthetic_label": "[SYNTHETIC — FOR DEMONSTRATION ONLY]",
  "human_review_note": "Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.",
  "publication_classification": "Needs review",
  "review_log_policy": "Reviewer decisions are stored separately from generated deterministic outputs.",
  "projects": [
    {
      "project_id": "requirements-to-verification",
      "title": "Requirements-to-Verification Tool",
      "short_title": "Req to Verification",
      "route": "#requirements-to-verification",
      "synthetic_label": "[SYNTHETIC — FOR DEMONSTRATION ONLY]",
      "human_review_note": "Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.",
      "publication_classification": "Needs review",
      "workflow_summary": "Turns synthetic requirement rows into trace matrices, ambiguity findings, assumptions, and review checklists.",
      "project_boundary": "Generated mappings are decision-support only; reviewer dispositions remain separate from source outputs.",
      "source_paths": [
        "Synthetic Requirements Sample.csv"
      ],
      "proof_screens": [
        "Reviewer dashboard",
        "Ambiguity triage",
        "Requirement detail",
        "Trace matrix review",
        "Export package summary"
      ],
      "metrics": [
        {
          "label": "Requirements processed",
          "value": 25,
          "tone": "neutral"
        },
        {
          "label": "Open ambiguity findings",
          "value": 41,
          "tone": "warning"
        },
        {
          "label": "Unresolved assumptions",
          "value": 37,
          "tone": "warning"
        },
        {
          "label": "Verification mapping gaps",
          "value": 25,
          "tone": "warning"
        },
        {
          "label": "Checklist items needing review",
          "value": 4,
          "tone": "warning"
        },
        {
          "label": "Export-ready rows",
          "value": 0,
          "tone": "neutral"
        }
      ],
      "review_items": [
        {
          "id": "SYN-REQ-001-Unclear owner",
          "type": "Ambiguity",
          "source": "SYN-REQ-001",
          "summary": "Unclear owner: Source row does not identify the qualified reviewer or owner.",
          "state": "Needs review",
          "severity": "Low",
          "recommended_action": "Assign a reviewer before using the generated package."
        },
        {
          "id": "SYN-REQ-002-Missing numeric limits",
          "type": "Ambiguity",
          "source": "SYN-REQ-002",
          "summary": "Missing numeric limits: Requirement refers to a measurable behavior but no numeric limit with unit was detected.",
          "state": "Needs review",
          "severity": "Medium",
          "recommended_action": "Add a public-safe synthetic limit or keep the requirement open."
        },
        {
          "id": "SYN-REQ-002-Unclear owner",
          "type": "Ambiguity",
          "source": "SYN-REQ-002",
          "summary": "Unclear owner: Source row does not identify the qualified reviewer or owner.",
          "state": "Needs review",
          "severity": "Low",
          "recommended_action": "Assign a reviewer before using the generated package."
        },
        {
          "id": "SYN-REQ-003-Unclear owner",
          "type": "Ambiguity",
          "source": "SYN-REQ-003",
          "summary": "Unclear owner: Source row does not identify the qualified reviewer or owner.",
          "state": "Needs review",
          "severity": "Low",
          "recommended_action": "Assign a reviewer before using the generated package."
        },
        {
          "id": "SYN-REQ-004-Missing numeric limits",
          "type": "Ambiguity",
          "source": "SYN-REQ-004",
          "summary": "Missing numeric limits: Requirement refers to a measurable behavior but no numeric limit with unit was detected.",
          "state": "Needs review",
          "severity": "Medium",
          "recommended_action": "Add a public-safe synthetic limit or keep the requirement open."
        },
        {
          "id": "SYN-ASM-001",
          "type": "Assumption",
          "source": "SYN-REQ-001",
          "summary": "Nominal 12 V vehicle supply; transient events excluded from this demo",
          "state": "Needs review",
          "severity": "Medium",
          "recommended_action": "Accept for demo, revise, reject, escalate, or block export."
        },
        {
          "id": "SYN-ASM-002",
          "type": "Assumption",
          "source": "SYN-REQ-002",
          "summary": "Optical performance values are not included in this demo",
          "state": "Needs review",
          "severity": "Medium",
          "recommended_action": "Accept for demo, revise, reject, escalate, or block export."
        },
        {
          "id": "SYN-ASM-003",
          "type": "Assumption",
          "source": "SYN-REQ-002",
          "summary": "A reviewer-defined synthetic numeric limit will be added before final verification planning.",
          "state": "Needs review",
          "severity": "Medium",
          "recommended_action": "Accept for demo, revise, reject, escalate, or block export."
        },
        {
          "id": "SYN-ASM-004",
          "type": "Assumption",
          "source": "SYN-REQ-003",
          "summary": "Command source is simulated",
          "state": "Needs review",
          "severity": "Medium",
          "recommended_action": "Accept for demo, revise, reject, escalate, or block export."
        }
      ],
      "artifacts": [
        {
          "label": "Trace matrix",
          "path": "projects/requirements-to-verification/generated_outputs/trace_matrix.csv",
          "kind": "CSV",
          "status": "Needs review"
        },
        {
          "label": "Ambiguity report",
          "path": "projects/requirements-to-verification/generated_outputs/ambiguity_report.csv",
          "kind": "CSV",
          "status": "Needs review"
        },
        {
          "label": "Assumptions register",
          "path": "projects/requirements-to-verification/generated_outputs/assumptions_register.csv",
          "kind": "CSV",
          "status": "Needs review"
        },
        {
          "label": "Review checklist",
          "path": "projects/requirements-to-verification/generated_outputs/review_checklist.csv",
          "kind": "CSV",
          "status": "Needs review"
        },
        {
          "label": "Run summary",
          "path": "projects/requirements-to-verification/generated_outputs/run_summary.md",
          "kind": "Markdown",
          "status": "Needs review"
        }
      ],
      "screen_tabs": [
        "Dashboard",
        "Review Queue",
        "Artifacts",
        "Publish Gate"
      ],
      "status_counts": {
        "Needs review": 78
      },
      "safe_to_publish_checks": [
        {
          "label": "Synthetic/demo label visible",
          "state": "Present"
        },
        {
          "label": "Human-review note visible",
          "state": "Present"
        },
        {
          "label": "Restricted identifier screen",
          "state": "Needs review"
        },
        {
          "label": "AI-approval wording check",
          "state": "Needs review"
        },
        {
          "label": "Qualified publication review",
          "state": "Needs review"
        }
      ]
    },
    {
      "project_id": "wcca-prep",
      "title": "AI-Assisted WCCA Prep Tool",
      "short_title": "WCCA Prep",
      "route": "#wcca-prep",
      "synthetic_label": "[SYNTHETIC — FOR DEMONSTRATION ONLY]",
      "human_review_note": "Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.",
      "publication_classification": "Needs review",
      "workflow_summary": "Prepares synthetic WCCA inputs, calculation rows, warning reports, plots, and equation-review evidence.",
      "project_boundary": "This workflow prepares WCCA review artifacts; it is not a final WCCA approval tool.",
      "source_paths": [
        "projects/wcca-prep-tool/data/synthetic_wcca_cases.csv",
        "projects/wcca-prep-tool/data/operating_conditions.csv"
      ],
      "proof_screens": [
        "Parameter audit table",
        "Missing-data warnings",
        "WCCA result table",
        "Plot gallery",
        "Equation review checklist"
      ],
      "metrics": [
        {
          "label": "Calculation rows",
          "value": 60,
          "tone": "neutral"
        },
        {
          "label": "Rows requiring review",
          "value": 48,
          "tone": "warning"
        },
        {
          "label": "Missing-data warning markers",
          "value": 2,
          "tone": "warning"
        },
        {
          "label": "Plot artifacts",
          "value": 5,
          "tone": "neutral"
        },
        {
          "label": "Export-ready rows",
          "value": 0,
          "tone": "neutral"
        }
      ],
      "review_items": [
        {
          "id": "SYN-WCCA-001-SYN-OC-LOWLINE-HOT",
          "type": "WCCA result",
          "source": "SYN-WCCA-001",
          "summary": "At least one stress ratio is at or above 0.80.",
          "state": "Review required",
          "severity": "Medium",
          "recommended_action": "Verify formulas, assumptions, thresholds, and missing-data warnings."
        },
        {
          "id": "SYN-WCCA-001-SYN-OC-HIGHLINE-HOT",
          "type": "WCCA result",
          "source": "SYN-WCCA-001",
          "summary": "At least one stress ratio is at or above 0.80.",
          "state": "Review required",
          "severity": "Medium",
          "recommended_action": "Verify formulas, assumptions, thresholds, and missing-data warnings."
        },
        {
          "id": "SYN-WCCA-001-SYN-OC-HIGHLOAD-HOT",
          "type": "WCCA result",
          "source": "SYN-WCCA-001",
          "summary": "At least one stress ratio is at or above 0.80.",
          "state": "Review required",
          "severity": "Medium",
          "recommended_action": "Verify formulas, assumptions, thresholds, and missing-data warnings."
        },
        {
          "id": "SYN-WCCA-002-SYN-OC-LOWLINE-HOT",
          "type": "WCCA result",
          "source": "SYN-WCCA-002",
          "summary": "At least one stress ratio is at or above 0.80.",
          "state": "Review required",
          "severity": "Medium",
          "recommended_action": "Verify formulas, assumptions, thresholds, and missing-data warnings."
        },
        {
          "id": "SYN-WCCA-002-SYN-OC-HIGHLINE-HOT",
          "type": "WCCA result",
          "source": "SYN-WCCA-002",
          "summary": "At least one stress ratio is at or above 0.80.",
          "state": "Review required",
          "severity": "Medium",
          "recommended_action": "Verify formulas, assumptions, thresholds, and missing-data warnings."
        },
        {
          "id": "SYN-WCCA-002-SYN-OC-HIGHLOAD-HOT",
          "type": "WCCA result",
          "source": "SYN-WCCA-002",
          "summary": "At least one stress ratio is at or above 0.80.",
          "state": "Review required",
          "severity": "Medium",
          "recommended_action": "Verify formulas, assumptions, thresholds, and missing-data warnings."
        },
        {
          "id": "SYN-WCCA-003-SYN-OC-LOWLINE-HOT",
          "type": "WCCA result",
          "source": "SYN-WCCA-003",
          "summary": "At least one stress ratio exceeds 1.00.",
          "state": "Over synthetic limit",
          "severity": "Low",
          "recommended_action": "Verify formulas, assumptions, thresholds, and missing-data warnings."
        },
        {
          "id": "SYN-WCCA-003-SYN-OC-NOMINAL",
          "type": "WCCA result",
          "source": "SYN-WCCA-003",
          "summary": "At least one stress ratio is at or above 0.80.",
          "state": "Review required",
          "severity": "Medium",
          "recommended_action": "Verify formulas, assumptions, thresholds, and missing-data warnings."
        }
      ],
      "artifacts": [
        {
          "label": "WCCA summary",
          "path": "projects/wcca-prep-tool/outputs/synthetic_wcca_summary.csv",
          "kind": "CSV",
          "status": "Needs review"
        },
        {
          "label": "WCCA report",
          "path": "projects/wcca-prep-tool/outputs/synthetic_wcca_report.md",
          "kind": "Markdown",
          "status": "Needs review"
        },
        {
          "label": "Missing-data warnings",
          "path": "projects/wcca-prep-tool/outputs/missing_data_warnings.md",
          "kind": "Markdown",
          "status": "Needs review"
        },
        {
          "label": "Equation review checklist",
          "path": "projects/wcca-prep-tool/docs/equation_review_checklist.md",
          "kind": "Markdown",
          "status": "Needs review"
        },
        {
          "label": "Margin By Case",
          "path": "projects/wcca-prep-tool/outputs/plots/margin_by_case.png",
          "kind": "PNG",
          "status": "Needs review"
        },
        {
          "label": "Pass Fail Distribution",
          "path": "projects/wcca-prep-tool/outputs/plots/pass_fail_distribution.png",
          "kind": "PNG",
          "status": "Needs review"
        },
        {
          "label": "Thermal Temperature Sensitivity",
          "path": "projects/wcca-prep-tool/outputs/plots/thermal_temperature_sensitivity.png",
          "kind": "PNG",
          "status": "Needs review"
        },
        {
          "label": "Voltage Sensitivity",
          "path": "projects/wcca-prep-tool/outputs/plots/voltage_sensitivity.png",
          "kind": "PNG",
          "status": "Needs review"
        },
        {
          "label": "Worst Case Result By Condition",
          "path": "projects/wcca-prep-tool/outputs/plots/worst_case_result_by_condition.png",
          "kind": "PNG",
          "status": "Needs review"
        }
      ],
      "screen_tabs": [
        "Dashboard",
        "Review Queue",
        "Artifacts",
        "Publish Gate"
      ],
      "status_counts": {
        "Review required": 26,
        "Within synthetic prep limit": 12,
        "Over synthetic limit": 22
      },
      "safe_to_publish_checks": [
        {
          "label": "Synthetic/demo label visible",
          "state": "Present"
        },
        {
          "label": "Human-review note visible",
          "state": "Present"
        },
        {
          "label": "Restricted identifier screen",
          "state": "Needs review"
        },
        {
          "label": "AI-approval wording check",
          "state": "Needs review"
        },
        {
          "label": "Qualified publication review",
          "state": "Needs review"
        }
      ]
    },
    {
      "project_id": "design-review-readiness",
      "title": "Design Review Readiness Assistant",
      "short_title": "Design Review",
      "route": "#design-review-readiness",
      "synthetic_label": "[SYNTHETIC — FOR DEMONSTRATION ONLY]",
      "human_review_note": "Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.",
      "publication_classification": "Needs review",
      "workflow_summary": "Converts synthetic review notes into risks, assumptions, validation gaps, mode matrices, diagnostic tables, and review packets.",
      "project_boundary": "Readiness means organized preparation context; it does not approve design release or validation strategy.",
      "source_paths": [
        "projects/design-review-readiness-assistant/inputs/synthetic_lighting_review_notes.md"
      ],
      "proof_screens": [
        "Readiness dashboard",
        "Risk register",
        "Validation gaps",
        "Mode-to-test matrix",
        "Diagnostic response table",
        "Review packet preview"
      ],
      "metrics": [
        {
          "label": "Risk rows",
          "value": 8,
          "tone": "neutral"
        },
        {
          "label": "Open review risks",
          "value": 8,
          "tone": "warning"
        },
        {
          "label": "Mode-to-test rows",
          "value": 7,
          "tone": "neutral"
        },
        {
          "label": "Diagnostic rows",
          "value": 8,
          "tone": "neutral"
        },
        {
          "label": "Screenshot artifacts",
          "value": 5,
          "tone": "neutral"
        },
        {
          "label": "Export-ready rows",
          "value": 0,
          "tone": "neutral"
        }
      ],
      "review_items": [
        {
          "id": "SYN-DRR-R001",
          "type": "Risk",
          "source": "Operating-mode traceability",
          "summary": "Operating-mode behavior may stay fragmented across low beam, high beam, and DRL notes.",
          "state": "Open",
          "severity": "Medium",
          "recommended_action": "Create one synthetic operating-mode trace table before review."
        },
        {
          "id": "SYN-DRR-R002",
          "type": "Risk",
          "source": "Input-voltage behavior",
          "summary": "Start-up and low-voltage behavior may be underprepared for review.",
          "state": "Needs review",
          "severity": "Medium",
          "recommended_action": "Draft synthetic start-up, nominal, low-voltage, and recovery test cases."
        },
        {
          "id": "SYN-DRR-R003",
          "type": "Risk",
          "source": "DRL reduced-current behavior",
          "summary": "DRL reduced-current behavior may remain qualitative without a reviewable synthetic target.",
          "state": "Mitigation proposed",
          "severity": "Medium",
          "recommended_action": "Define a public-safe synthetic reduction target or keep the item open."
        },
        {
          "id": "SYN-DRR-R004",
          "type": "Risk",
          "source": "Thermal evidence",
          "summary": "Thermal review trigger may be discussed without supporting synthetic plot evidence.",
          "state": "Mitigation proposed",
          "severity": "Medium",
          "recommended_action": "Generate a synthetic thermal trend plot and label the threshold as demo-only."
        },
        {
          "id": "SYN-DRR-R005",
          "type": "Risk",
          "source": "Diagnostic behavior",
          "summary": "Diagnostic response coverage may be incomplete for open-load and short-to-ground review topics.",
          "state": "Open",
          "severity": "Medium",
          "recommended_action": "Add a synthetic diagnostic response table and fault injection checklist."
        },
        {
          "id": "SYN-DRR-R006",
          "type": "Risk",
          "source": "WCCA readiness",
          "summary": "WCCA readiness may be referenced without parameter maturity or tolerance-source status.",
          "state": "Needs review",
          "severity": "Medium",
          "recommended_action": "Separate missing, draft, and reviewed WCCA preparation evidence."
        },
        {
          "id": "SYN-DRR-R007",
          "type": "Risk",
          "source": "Evidence package",
          "summary": "The public workflow may lack visible proof if screenshots and synthetic evidence remain placeholders.",
          "state": "Mitigation proposed",
          "severity": "High",
          "recommended_action": "Generate public-safe synthetic screenshots for the dashboard, packet preview, and risk export."
        },
        {
          "id": "SYN-DRR-R008",
          "type": "Risk",
          "source": "Human review boundary",
          "summary": "Readers may misinterpret a preparation packet as an engineering approval artifact.",
          "state": "Needs review",
          "severity": "High",
          "recommended_action": "Repeat the human-review boundary and draft status in every generated artifact."
        }
      ],
      "artifacts": [
        {
          "label": "Design review packet",
          "path": "projects/design-review-readiness-assistant/outputs/design_review_packet.md",
          "kind": "Markdown",
          "status": "Needs review"
        },
        {
          "label": "Risk register",
          "path": "projects/design-review-readiness-assistant/outputs/risk_register.csv",
          "kind": "CSV",
          "status": "Needs review"
        },
        {
          "label": "Validation gaps",
          "path": "projects/design-review-readiness-assistant/outputs/validation_test_gaps.md",
          "kind": "Markdown",
          "status": "Needs review"
        },
        {
          "label": "Mode-to-test matrix",
          "path": "projects/design-review-readiness-assistant/outputs/mode_to_test_matrix.csv",
          "kind": "CSV",
          "status": "Needs review"
        },
        {
          "label": "Diagnostic response table",
          "path": "projects/design-review-readiness-assistant/outputs/diagnostic_response_table.csv",
          "kind": "CSV",
          "status": "Needs review"
        },
        {
          "label": "Dashboard Overview",
          "path": "projects/design-review-readiness-assistant/screenshots/dashboard_overview.png",
          "kind": "PNG",
          "status": "Needs review"
        },
        {
          "label": "Diagnostic Response Table",
          "path": "projects/design-review-readiness-assistant/screenshots/diagnostic_response_table.png",
          "kind": "PNG",
          "status": "Needs review"
        },
        {
          "label": "Mode To Test Matrix",
          "path": "projects/design-review-readiness-assistant/screenshots/mode_to_test_matrix.png",
          "kind": "PNG",
          "status": "Needs review"
        },
        {
          "label": "Review Packet Preview",
          "path": "projects/design-review-readiness-assistant/screenshots/review_packet_preview.png",
          "kind": "PNG",
          "status": "Needs review"
        },
        {
          "label": "Risk Register Export",
          "path": "projects/design-review-readiness-assistant/screenshots/risk_register_export.png",
          "kind": "PNG",
          "status": "Needs review"
        }
      ],
      "screen_tabs": [
        "Dashboard",
        "Review Queue",
        "Artifacts",
        "Publish Gate"
      ],
      "status_counts": {
        "Open": 2,
        "Needs review": 3,
        "Mitigation proposed": 3
      },
      "safe_to_publish_checks": [
        {
          "label": "Synthetic/demo label visible",
          "state": "Present"
        },
        {
          "label": "Human-review note visible",
          "state": "Present"
        },
        {
          "label": "Restricted identifier screen",
          "state": "Needs review"
        },
        {
          "label": "AI-approval wording check",
          "state": "Needs review"
        },
        {
          "label": "Qualified publication review",
          "state": "Needs review"
        }
      ]
    },
    {
      "project_id": "lighting-feasibility",
      "title": "Lighting Feasibility Mini-Simulator",
      "short_title": "Feasibility",
      "route": "#lighting-feasibility",
      "synthetic_label": "[SYNTHETIC — FOR DEMONSTRATION ONLY]",
      "human_review_note": "Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval.",
      "publication_classification": "Needs review",
      "workflow_summary": "Runs first-pass deterministic screening for synthetic lighting loads, margins, status reasons, and sensitivity sweeps.",
      "project_boundary": "Pass means first-pass screening only; every formula, threshold, and assumption remains review-owned.",
      "source_paths": [
        "projects/lighting-feasibility-mini-simulator/data/synthetic_lighting_cases.csv"
      ],
      "proof_screens": [
        "Case input table",
        "Feasibility status summary",
        "Margin plots",
        "Sensitivity sweep explorer",
        "Risk flag summary",
        "Export summary"
      ],
      "metrics": [
        {
          "label": "Feasibility cases",
          "value": 5,
          "tone": "neutral"
        },
        {
          "label": "Marginal or fail cases",
          "value": 4,
          "tone": "warning"
        },
        {
          "label": "Sensitivity rows",
          "value": 100,
          "tone": "neutral"
        },
        {
          "label": "Plot artifacts",
          "value": 7,
          "tone": "neutral"
        },
        {
          "label": "Export-ready rows",
          "value": 0,
          "tone": "neutral"
        }
      ],
      "review_items": [
        {
          "id": "SYN-LGT-002",
          "type": "Feasibility case",
          "source": "Synthetic three-LED signature",
          "summary": "voltage headroom 0.19 V is 0.75 V or less",
          "state": "Marginal",
          "severity": "Medium",
          "recommended_action": "Run sensitivity sweep and review thermal/electrical margins."
        },
        {
          "id": "SYN-LGT-003",
          "type": "Feasibility case",
          "source": "Synthetic long-string signal",
          "summary": "boost duty 0.67 exceeds synthetic max 0.62",
          "state": "Fail",
          "severity": "High",
          "recommended_action": "Revise topology, LED count, current, thermal path, or ratings before deeper analysis."
        },
        {
          "id": "SYN-LGT-004",
          "type": "Feasibility case",
          "source": "Synthetic hot-compartment marker",
          "summary": "driver case temperature ratio 0.90 is at or above 0.85; LED junction temperature ratio 0.93 is at or above 0.85; LED junction margin 9.2 C is 10 C or less",
          "state": "Marginal",
          "severity": "Medium",
          "recommended_action": "Run sensitivity sweep and review thermal/electrical margins."
        },
        {
          "id": "SYN-LGT-005",
          "type": "Feasibility case",
          "source": "Synthetic linear accent channel",
          "summary": "driver case temperature ratio 1.08 exceeds 1.00; voltage headroom -0.32 V is below 0 V; driver thermal margin -10.3 C is below 0 C",
          "state": "Fail",
          "severity": "High",
          "recommended_action": "Revise topology, LED count, current, thermal path, or ratings before deeper analysis."
        }
      ],
      "artifacts": [
        {
          "label": "Feasibility summary",
          "path": "projects/lighting-feasibility-mini-simulator/outputs/feasibility_summary.csv",
          "kind": "CSV",
          "status": "Needs review"
        },
        {
          "label": "Feasibility report",
          "path": "projects/lighting-feasibility-mini-simulator/outputs/feasibility_summary.md",
          "kind": "Markdown",
          "status": "Needs review"
        },
        {
          "label": "Sensitivity summary",
          "path": "projects/lighting-feasibility-mini-simulator/outputs/sensitivity/sensitivity_summary.csv",
          "kind": "CSV",
          "status": "Needs review"
        },
        {
          "label": "Portfolio capture summary",
          "path": "projects/lighting-feasibility-mini-simulator/outputs/screenshots/portfolio_capture_summary.md",
          "kind": "Markdown",
          "status": "Needs review"
        },
        {
          "label": "Current Margin By Case",
          "path": "projects/lighting-feasibility-mini-simulator/outputs/plots/current_margin_by_case.png",
          "kind": "PNG",
          "status": "Needs review"
        },
        {
          "label": "Feasibility Status Count",
          "path": "projects/lighting-feasibility-mini-simulator/outputs/plots/feasibility_status_count.png",
          "kind": "PNG",
          "status": "Needs review"
        },
        {
          "label": "Thermal Margin By Case",
          "path": "projects/lighting-feasibility-mini-simulator/outputs/plots/thermal_margin_by_case.png",
          "kind": "PNG",
          "status": "Needs review"
        },
        {
          "label": "Ambient Temperature Sweep",
          "path": "projects/lighting-feasibility-mini-simulator/outputs/sensitivity/plots/ambient_temperature_sweep.png",
          "kind": "PNG",
          "status": "Needs review"
        },
        {
          "label": "Led Current Sweep",
          "path": "projects/lighting-feasibility-mini-simulator/outputs/sensitivity/plots/led_current_sweep.png",
          "kind": "PNG",
          "status": "Needs review"
        },
        {
          "label": "Optical Efficiency Sweep",
          "path": "projects/lighting-feasibility-mini-simulator/outputs/sensitivity/plots/optical_efficiency_sweep.png",
          "kind": "PNG",
          "status": "Needs review"
        },
        {
          "label": "Thermal Resistance Sweep",
          "path": "projects/lighting-feasibility-mini-simulator/outputs/sensitivity/plots/thermal_resistance_sweep.png",
          "kind": "PNG",
          "status": "Needs review"
        }
      ],
      "screen_tabs": [
        "Dashboard",
        "Review Queue",
        "Artifacts",
        "Publish Gate"
      ],
      "status_counts": {
        "Pass": 1,
        "Marginal": 2,
        "Fail": 2
      },
      "safe_to_publish_checks": [
        {
          "label": "Synthetic/demo label visible",
          "state": "Present"
        },
        {
          "label": "Human-review note visible",
          "state": "Present"
        },
        {
          "label": "Restricted identifier screen",
          "state": "Needs review"
        },
        {
          "label": "AI-approval wording check",
          "state": "Needs review"
        },
        {
          "label": "Qualified publication review",
          "state": "Needs review"
        }
      ]
    }
  ],
  "portfolio_metrics": [
    {
      "label": "Projects in console",
      "value": 4,
      "tone": "neutral"
    },
    {
      "label": "Review items surfaced",
      "value": 29,
      "tone": "warning"
    },
    {
      "label": "Artifacts indexed",
      "value": 35,
      "tone": "neutral"
    },
    {
      "label": "Safe-to-publish status",
      "value": "Needs review",
      "tone": "warning"
    }
  ]
};
