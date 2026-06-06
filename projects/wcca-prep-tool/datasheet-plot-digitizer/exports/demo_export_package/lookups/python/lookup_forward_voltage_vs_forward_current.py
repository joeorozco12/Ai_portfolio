"""Synthetic LED curve lookup generated from digitized plot points."""

SYNTHETIC_LABEL = "[SYNTHETIC — FOR DEMONSTRATION ONLY]"
HUMAN_REVIEW_REQUIRED = "Human Review Required: AI-generated outputs are decision-support artifacts only. A qualified engineer owns final review and approval."
CURVE_METADATA = {
    "axis_calibration": {
        "x_pixel_high": 560.0,
        "x_pixel_low": 80.0,
        "x_value_high": 4.5,
        "x_value_low": 2.5,
        "y_pixel_high": 60.0,
        "y_pixel_low": 420.0,
        "y_value_high": 4000.0,
        "y_value_low": 0.0
    },
    "crop_region_px": {
        "height": 410,
        "left": 60,
        "top": 40,
        "width": 540
    },
    "curve_name": "forward_voltage_vs_forward_current",
    "datasheet_source": "synthetic_datasheet_style_plot",
    "digitization_method": "manual_calibration_plus_manual_curve_pick",
    "engineering_note": "Reference-only synthetic plot data. Not guaranteed by a manufacturer. Engineer review is required before use as WCCA or feasibility input.",
    "fit_model": "pchip_shape_preserving_interpolation",
    "manufacturer": "Synthetic LED Supplier",
    "part_number": "SYN-LED-170",
    "publication_classification": "Needs review",
    "review_status": "draft_extraction",
    "source_page": "synthetic_page_20",
    "source_section": "synthetic_forward_current_characteristics",
    "x_axis": {
        "label": "Forward Voltage",
        "scale": "linear",
        "unit": "V"
    },
    "y_axis": {
        "label": "Forward Current",
        "scale": "linear",
        "unit": "mA"
    }
}
DOWNSTREAM_USE_WARNINGS = [
    "Do not use this export for WCCA, feasibility simulation, thermal derating, luminous-flux prediction, design review, or design decisions until a qualified engineer reviews and accepts it.",
    "Lookup functions clamp outside the digitized x-range; they are not validated extrapolation models.",
    "Curve-fit coefficients must be checked against the raw points and overlay image before downstream use.",
    "Synthetic demo identifiers are not real device, supplier, customer, program, schematic, BOM, harness, cost, validation, ticket, repository, or internal-document references."
]
PCHIP_SEGMENTS = [
    [
        2.8,
        2.95,
        50.0,
        99.99999999999555,
        5513.513513513533,
        -11571.571571571618
    ],
    [
        2.95,
        3.1,
        150.0,
        972.9729729729719,
        6650.556438791783,
        -7580.286168521614
    ],
    [
        3.1,
        3.25,
        420.00000000000017,
        2456.4705882352964,
        16385.947712418278,
        -46564.27015250537
    ],
    [
        3.25,
        3.4,
        1000.0,
        4229.166666666669,
        3759.2592592592723,
        -5617.283950617362
    ],
    [
        3.4,
        3.55,
        1700.0,
        4977.777777777781,
        4740.740740740799,
        -15802.469135802856
    ],
    [
        3.55,
        3.7,
        2500.0,
        5333.333333333329,
        5079.365079364877,
        -33862.433862432874
    ],
    [
        3.7,
        3.85,
        3300.0,
        4571.428571428568,
        -3174.603174603155,
        -4232.804232804124
    ]
]


def lookup_forward_voltage_vs_forward_current(x_value):
    """Return interpolated y-value using draft PCHIP coefficients.

    Endpoint clamping is used outside the digitized range. This lookup is a
    review artifact and must not be used for engineering decisions until a
    qualified engineer accepts the export package.
    """

    segments = PCHIP_SEGMENTS
    if x_value <= segments[0][0]:
        return segments[0][2]
    last = segments[-1]
    if x_value >= last[1]:
        t = last[1] - last[0]
        return last[2] + last[3] * t + last[4] * t * t + last[5] * t * t * t

    for x0, x1, a, b, c, d in segments:
        if x0 <= x_value <= x1:
            t = x_value - x0
            return a + b * t + c * t * t + d * t * t * t
    raise ValueError("Input value is outside interpolation intervals.")
