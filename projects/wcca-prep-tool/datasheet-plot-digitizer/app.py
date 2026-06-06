"""Streamlit workflow shell for the LED Datasheet Plot Digitizer."""

from __future__ import annotations

import copy
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Sequence

from led_digitizer.calibration import (
    AxisCalibration,
    CurveCalibration,
    EngineeringPoint,
)
from led_digitizer.curve_fit import (
    build_pchip_segments,
    evaluate_pchip,
    sort_unique_points,
)
from led_digitizer.exports import (
    HUMAN_REVIEW_NOTE,
    SYNTHETIC_LABEL,
    safe_name,
    write_markdown_report,
    write_matlab_lookup,
    write_metadata_json,
    write_overlay_png,
    write_points_csv,
    write_python_lookup,
)
from led_digitizer.sample_project import SAMPLE_METADATA, load_sample_points

try:
    import streamlit as st
except ModuleNotFoundError:  # pragma: no cover - exercised only outside Streamlit.
    st = None

try:
    import fitz
except ModuleNotFoundError:  # pragma: no cover - optional runtime dependency.
    fitz = None

try:
    import cv2
except ModuleNotFoundError:  # pragma: no cover - optional runtime dependency.
    cv2 = None


PROJECT_ROOT = Path(__file__).resolve().parent
SAMPLE_POINTS_PATH = PROJECT_ROOT / "data" / "synthetic_manual_points.csv"
SAMPLE_OVERLAY_PATH = (
    PROJECT_ROOT / "outputs" / "overlay_forward_voltage_vs_current.png"
)

SOURCE_CATEGORIES = ["synthetic", "public"]
PUBLICATION_CLASSIFICATIONS = [
    "Needs review",
    "Safe to publish",
    "Internal only",
    "Do not publish",
]
REVIEW_STATUSES = [
    "draft_extraction",
    "pending_engineering_review",
    "engineer_reviewed_demo",
    "rejected_redo_calibration",
]
POINT_REVIEW_STATUSES = [
    "draft_extraction",
    "manual_point_reviewed",
    "rejected_redo_point",
]


def main() -> None:
    if st is None:
        print("Streamlit is not installed. Install requirements.txt and run:")
        print("streamlit run app.py")
        return

    st.set_page_config(page_title="LED Datasheet Curve Studio", layout="wide")
    _initialize_state()

    st.title("LED Datasheet Curve Studio")
    st.caption(SYNTHETIC_LABEL)
    st.warning(HUMAN_REVIEW_NOTE)
    st.info(
        "Local workflow only. Use synthetic or public LED plot sources; do not upload "
        "controlled employer, customer, supplier, program, schematic, BOM, harness, "
        "cost, internal requirement, validation, ticket, part-number, or file-path data."
    )

    state = st.session_state
    _sidebar_status(state)

    (
        setup_tab,
        source_tab,
        crop_tab,
        points_tab,
        validation_tab,
        review_tab,
        export_tab,
    ) = st.tabs(
        [
            "Project Setup",
            "Source Import",
            "Crop & Calibration",
            "Point Entry",
            "Fit Validation",
            "Review Checklist",
            "Export Review",
        ]
    )

    with setup_tab:
        state["metadata"] = _project_setup_panel(state["metadata"])

    with source_tab:
        state["metadata"] = _source_import_panel(state["metadata"])

    with crop_tab:
        state["metadata"] = _crop_metadata_panel(state["metadata"])
        calibration = _calibration_panel(state["metadata"])
        state["calibration_valid"] = calibration is not None

    with points_tab:
        points = _point_entry_panel(calibration)
        state["points"] = points

    validation = _build_fit_validation(state["points"])
    with validation_tab:
        _fit_validation_panel(validation, state["points"])

    with review_tab:
        state["review_checks"] = _review_checklist_panel(
            state["review_checks"],
            calibration_valid=state["calibration_valid"],
            has_points=bool(state["points"]),
            validation=validation,
        )

    with export_tab:
        _export_panel(
            state["metadata"],
            state["points"],
            calibration_valid=state["calibration_valid"],
            validation=validation,
            review_checks=state["review_checks"],
        )


def _initialize_state() -> None:
    state = st.session_state
    state.setdefault("metadata", _default_metadata())
    state.setdefault("point_rows", _sample_point_rows())
    state.setdefault("points", [])
    state.setdefault("calibration_valid", True)
    state.setdefault(
        "review_checks",
        {
            "source_public_safe": False,
            "crop_and_calibration_reviewed": False,
            "points_reviewed": False,
            "fit_validation_reviewed": False,
            "export_marked_review_only": False,
        },
    )


def _default_metadata() -> dict[str, Any]:
    metadata = copy.deepcopy(SAMPLE_METADATA)
    metadata.update(
        {
            "project_id": "synthetic-forward-current-demo",
            "project_name": "Synthetic Forward Current Curve",
            "created_by": "Jose Orozco",
            "intended_use": "reviewable_led_curve_data_prep",
            "description": "Synthetic LED datasheet-style curve project.",
            "source_category": "synthetic",
            "source_type": "datasheet_plot_image",
            "source_uri": "",
        }
    )
    return metadata


def _sample_point_rows() -> list[dict[str, Any]]:
    return [
        {
            "point_id": point.point_id,
            "source_pixel_x": point.source_pixel_x,
            "source_pixel_y": point.source_pixel_y,
            "review_status": point.review_status,
            "notes": point.notes,
        }
        for point in load_sample_points(SAMPLE_POINTS_PATH)
    ]


def _sidebar_status(state: dict[str, Any]) -> None:
    with st.sidebar:
        st.header("Workflow Status")
        st.write(f"Project: `{state['metadata'].get('project_id', 'not_set')}`")
        st.write(f"Source: `{state['metadata'].get('source_category', 'not_set')}`")
        st.write(f"Points: `{len(state.get('points', []))}`")
        st.write(
            "Fit validation: "
            + ("ready" if state.get("points") else "waiting for calibrated points")
        )
        st.divider()
        if st.button("Reset to synthetic demo defaults"):
            _reset_to_sample_defaults()
            st.rerun()


def _reset_to_sample_defaults() -> None:
    state = st.session_state
    state["metadata"] = _default_metadata()
    state["point_rows"] = _sample_point_rows()
    state["points"] = []
    state["calibration_valid"] = True
    state["review_checks"] = {
        "source_public_safe": False,
        "crop_and_calibration_reviewed": False,
        "points_reviewed": False,
        "fit_validation_reviewed": False,
        "export_marked_review_only": False,
    }
    for widget_key in [
        "point_rows_editor",
        "source_public_safe",
        "crop_and_calibration_reviewed",
        "points_reviewed",
        "fit_validation_reviewed",
        "export_marked_review_only",
        "engineer_review_acknowledgment",
    ]:
        if widget_key in state:
            del state[widget_key]


def _project_setup_panel(metadata: dict[str, Any]) -> dict[str, Any]:
    st.subheader("Project Setup")
    updated = copy.deepcopy(metadata)
    left, right = st.columns(2)

    with left:
        updated["project_id"] = st.text_input("Project ID", updated["project_id"])
        updated["project_name"] = st.text_input("Project name", updated["project_name"])
        updated["part_number"] = st.text_input(
            "Synthetic LED identifier", updated["part_number"]
        )
        updated["created_by"] = st.text_input("Prepared by", updated["created_by"])

    with right:
        updated["curve_name"] = st.text_input("Curve name", updated["curve_name"])
        updated["intended_use"] = st.text_input(
            "Intended use", updated["intended_use"]
        )
        updated["publication_classification"] = st.selectbox(
            "Publication classification",
            PUBLICATION_CLASSIFICATIONS,
            index=_index_or_zero(
                PUBLICATION_CLASSIFICATIONS,
                updated.get("publication_classification", "Needs review"),
            ),
        )
        updated["review_status"] = st.selectbox(
            "Project review status",
            REVIEW_STATUSES,
            index=_index_or_zero(REVIEW_STATUSES, updated["review_status"]),
        )

    updated["description"] = st.text_area(
        "Project description",
        updated["description"],
        height=80,
    )
    updated["engineering_note"] = st.text_area(
        "Engineering note",
        updated["engineering_note"],
        height=90,
    )
    return updated


def _source_import_panel(metadata: dict[str, Any]) -> dict[str, Any]:
    st.subheader("Source Import")
    updated = copy.deepcopy(metadata)
    left, right = st.columns([1, 1])

    with left:
        updated["source_category"] = st.selectbox(
            "Source category",
            SOURCE_CATEGORIES,
            index=_index_or_zero(
                SOURCE_CATEGORIES,
                updated.get("source_category", "synthetic"),
            ),
        )
        updated["datasheet_source"] = st.text_input(
            "Source label", updated["datasheet_source"]
        )
        updated["manufacturer"] = st.text_input(
            "Synthetic/public source owner label", updated["manufacturer"]
        )
        updated["source_page"] = st.text_input("Source page", updated["source_page"])
        updated["source_section"] = st.text_input(
            "Source section", updated.get("source_section", "")
        )
        updated["source_uri"] = st.text_input(
            "Public URL or synthetic source note", updated.get("source_uri", "")
        )

    with right:
        uploaded_file = st.file_uploader(
            "Synthetic/public PDF or image preview",
            type=["pdf", "png", "jpg", "jpeg"],
        )
        if uploaded_file is not None:
            _render_upload_preview(uploaded_file)
        elif SAMPLE_OVERLAY_PATH.exists():
            st.image(
                str(SAMPLE_OVERLAY_PATH),
                caption="Synthetic overlay placeholder from the generated demo package.",
            )
        else:
            st.info(
                "No source preview loaded. The synthetic sample rows remain available."
            )

    if updated["source_category"] == "public":
        st.warning(
            "Public source selection still requires manual publication review before "
            "captures or exports are used in portfolio material."
        )
    return updated


def _render_upload_preview(uploaded_file: Any) -> None:
    suffix = Path(uploaded_file.name).suffix.lower()
    if suffix == ".pdf":
        if fitz is None:
            st.info("PDF preview requires PyMuPDF from requirements.txt.")
            return
        try:
            document = fitz.open(stream=uploaded_file.getvalue(), filetype="pdf")
            try:
                page_index = st.number_input(
                    "PDF page index",
                    min_value=0,
                    max_value=max(len(document) - 1, 0),
                    value=0,
                    step=1,
                )
                page = document[int(page_index)]
                pixmap = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
                st.image(pixmap.tobytes("png"))
            finally:
                document.close()
        except Exception as exc:  # pragma: no cover - runtime preview guard.
            st.warning(f"PDF preview failed: {exc}")
        return

    try:
        st.image(uploaded_file.getvalue())
    except Exception as exc:  # pragma: no cover - runtime preview guard.
        st.warning(f"Image preview failed: {exc}")


def _crop_metadata_panel(metadata: dict[str, Any]) -> dict[str, Any]:
    st.subheader("Crop Metadata")
    updated = copy.deepcopy(metadata)
    crop = dict(updated.get("crop_region_px", {}))
    left, top, width, height = st.columns(4)
    with left:
        crop["left"] = int(
            st.number_input(
                "Crop left px",
                value=int(crop.get("left", 60)),
                min_value=0,
            )
        )
    with top:
        crop["top"] = int(
            st.number_input(
                "Crop top px",
                value=int(crop.get("top", 40)),
                min_value=0,
            )
        )
    with width:
        crop["width"] = int(
            st.number_input(
                "Crop width px",
                value=int(crop.get("width", 540)),
                min_value=1,
            )
        )
    with height:
        crop["height"] = int(
            st.number_input(
                "Crop height px",
                value=int(crop.get("height", 410)),
                min_value=1,
            )
        )
    updated["crop_region_px"] = crop
    return updated


def _calibration_panel(metadata: dict[str, Any]) -> CurveCalibration | None:
    st.subheader("Calibration Entry")
    axis_data = dict(metadata.get("axis_calibration", {}))
    x_axis = dict(metadata["x_axis"])
    y_axis = dict(metadata["y_axis"])

    label_left, label_right = st.columns(2)
    with label_left:
        x_axis["label"] = st.text_input("X-axis label", x_axis["label"])
        x_axis["unit"] = st.text_input("X-axis unit", x_axis["unit"])
        x_axis["scale"] = st.selectbox(
            "X-axis scale",
            ["linear", "log"],
            index=_index_or_zero(["linear", "log"], x_axis.get("scale", "linear")),
        )
    with label_right:
        y_axis["label"] = st.text_input("Y-axis label", y_axis["label"])
        y_axis["unit"] = st.text_input("Y-axis unit", y_axis["unit"])
        y_axis["scale"] = st.selectbox(
            "Y-axis scale",
            ["linear", "log"],
            index=_index_or_zero(["linear", "log"], y_axis.get("scale", "linear")),
        )

    x_low, x_high, y_low, y_high = st.columns(4)
    with x_low:
        x_pixel_low = st.number_input(
            "X low pixel", value=float(axis_data.get("x_pixel_low", 80.0))
        )
        x_value_low = st.number_input(
            "X low value", value=float(axis_data.get("x_value_low", 2.5))
        )
    with x_high:
        x_pixel_high = st.number_input(
            "X high pixel", value=float(axis_data.get("x_pixel_high", 560.0))
        )
        x_value_high = st.number_input(
            "X high value", value=float(axis_data.get("x_value_high", 4.5))
        )
    with y_low:
        y_pixel_low = st.number_input(
            "Y low pixel", value=float(axis_data.get("y_pixel_low", 420.0))
        )
        y_value_low = st.number_input(
            "Y low value", value=float(axis_data.get("y_value_low", 0.0))
        )
    with y_high:
        y_pixel_high = st.number_input(
            "Y high pixel", value=float(axis_data.get("y_pixel_high", 60.0))
        )
        y_value_high = st.number_input(
            "Y high value", value=float(axis_data.get("y_value_high", 4000.0))
        )

    metadata["x_axis"] = x_axis
    metadata["y_axis"] = y_axis
    metadata["axis_calibration"] = {
        "x_pixel_low": x_pixel_low,
        "x_pixel_high": x_pixel_high,
        "x_value_low": x_value_low,
        "x_value_high": x_value_high,
        "y_pixel_low": y_pixel_low,
        "y_pixel_high": y_pixel_high,
        "y_value_low": y_value_low,
        "y_value_high": y_value_high,
    }

    try:
        calibration = CurveCalibration(
            x_axis=AxisCalibration(
                pixel_low=x_pixel_low,
                pixel_high=x_pixel_high,
                value_low=x_value_low,
                value_high=x_value_high,
                scale=x_axis["scale"],
                label=x_axis["label"],
                unit=x_axis["unit"],
            ),
            y_axis=AxisCalibration(
                pixel_low=y_pixel_low,
                pixel_high=y_pixel_high,
                value_low=y_value_low,
                value_high=y_value_high,
                scale=y_axis["scale"],
                label=y_axis["label"],
                unit=y_axis["unit"],
            ),
        )
    except ValueError as exc:
        st.error(f"Calibration is not valid: {exc}")
        return None

    st.success("Calibration values are structurally valid.")
    return calibration


def _point_entry_panel(calibration: CurveCalibration | None) -> list[EngineeringPoint]:
    st.subheader("Point Entry")
    mode = st.radio(
        "Point entry mode",
        ["Manual pixel table", "Assisted extraction preview"],
        horizontal=True,
    )
    if mode == "Assisted extraction preview":
        if cv2 is None:
            st.info(
                "Assisted extraction requires opencv-python-headless from "
                "requirements.txt."
            )
        st.warning(
            "Assisted extraction remains a future Task 7 workflow. Manual points "
            "are used here."
        )

    edited_rows = st.data_editor(
        st.session_state["point_rows"],
        num_rows="dynamic",
        use_container_width=True,
        key="point_rows_editor",
        column_config={
            "point_id": st.column_config.TextColumn("Point ID", required=True),
            "source_pixel_x": st.column_config.NumberColumn(
                "Source pixel X",
                required=True,
            ),
            "source_pixel_y": st.column_config.NumberColumn(
                "Source pixel Y",
                required=True,
            ),
            "review_status": st.column_config.SelectboxColumn(
                "Point review status",
                options=POINT_REVIEW_STATUSES,
                required=True,
            ),
            "notes": st.column_config.TextColumn("Notes"),
        },
    )
    rows = _editor_rows(edited_rows)
    st.session_state["point_rows"] = rows

    if calibration is None:
        st.warning("Enter valid calibration values before converting points.")
        return []

    points: list[EngineeringPoint] = []
    conversion_errors = []
    for row_index, row in enumerate(rows, start=1):
        try:
            points.append(
                calibration.pixel_to_engineering(
                    point_id=str(row["point_id"]).strip(),
                    source_pixel_x=float(row["source_pixel_x"]),
                    source_pixel_y=float(row["source_pixel_y"]),
                    review_status=str(row.get("review_status", "draft_extraction")),
                    notes=str(row.get("notes", "")),
                )
            )
        except (KeyError, TypeError, ValueError) as exc:
            conversion_errors.append(f"Row {row_index}: {exc}")

    if conversion_errors:
        for message in conversion_errors[:3]:
            st.warning(message)
        if len(conversion_errors) > 3:
            st.warning(f"{len(conversion_errors) - 3} additional row errors hidden.")

    if points:
        st.dataframe(
            [
                {
                    "point_id": point.point_id,
                    "x": round(point.x, 6),
                    "y": round(point.y, 6),
                    "source_pixel_x": round(point.source_pixel_x, 3),
                    "source_pixel_y": round(point.source_pixel_y, 3),
                    "review_status": point.review_status,
                }
                for point in points
            ],
            use_container_width=True,
        )
    else:
        st.info("No valid converted points are available yet.")
    return points


def _build_fit_validation(points: Sequence[EngineeringPoint]) -> dict[str, Any]:
    if len(points) < 2:
        return {
            "valid": False,
            "message": "At least two valid points are required for curve-fit validation.",
        }

    try:
        sorted_points = sort_unique_points(points)
        segments = build_pchip_segments(sorted_points)
        residuals = [
            abs(evaluate_pchip(segments, point.x) - point.y)
            for point in sorted_points
        ]
    except ValueError as exc:
        return {"valid": False, "message": str(exc)}

    return {
        "valid": True,
        "message": "PCHIP fit can be built from the current points.",
        "point_count": len(sorted_points),
        "segment_count": len(segments),
        "x_min": sorted_points[0].x,
        "x_max": sorted_points[-1].x,
        "y_min": min(point.y for point in sorted_points),
        "y_max": max(point.y for point in sorted_points),
        "max_raw_point_residual": max(residuals),
    }


def _fit_validation_panel(
    validation: dict[str, Any],
    points: Sequence[EngineeringPoint],
) -> None:
    st.subheader("Fit Validation Display")
    st.caption("Interpolation health check only. This is not engineering approval.")
    if not validation["valid"]:
        st.error(validation["message"])
        return

    first, second, third, fourth = st.columns(4)
    first.metric("Valid points", validation["point_count"])
    second.metric("PCHIP segments", validation["segment_count"])
    third.metric(
        "X domain",
        f"{validation['x_min']:.4g} to {validation['x_max']:.4g}",
    )
    fourth.metric("Max raw residual", f"{validation['max_raw_point_residual']:.3g}")

    st.success(validation["message"])
    st.dataframe(
        [
            {
                "point_id": point.point_id,
                "x": round(point.x, 6),
                "y_raw": round(point.y, 6),
                "fit_y_at_raw_x": round(point.y, 6),
                "fit_model": "pchip_shape_preserving_interpolation",
                "review_status": point.review_status,
            }
            for point in sorted(points, key=lambda item: item.x)
        ],
        use_container_width=True,
    )


def _review_checklist_panel(
    review_checks: dict[str, bool],
    calibration_valid: bool,
    has_points: bool,
    validation: dict[str, Any],
) -> dict[str, bool]:
    st.subheader("Review Checklist")
    checks = dict(review_checks)
    checks["source_public_safe"] = st.checkbox(
        "Source is synthetic or public and contains no controlled details.",
        value=checks.get("source_public_safe", False),
        key="source_public_safe",
    )
    checks["crop_and_calibration_reviewed"] = st.checkbox(
        "Crop metadata and axis calibration entries are ready for engineering review.",
        value=checks.get("crop_and_calibration_reviewed", False),
        key="crop_and_calibration_reviewed",
        disabled=not calibration_valid,
    )
    checks["points_reviewed"] = st.checkbox(
        "Manual point table has been checked against the source preview.",
        value=checks.get("points_reviewed", False),
        key="points_reviewed",
        disabled=not has_points,
    )
    checks["fit_validation_reviewed"] = st.checkbox(
        "Fit validation display has been reviewed for obvious data-entry issues.",
        value=checks.get("fit_validation_reviewed", False),
        key="fit_validation_reviewed",
        disabled=not validation["valid"],
    )
    checks["export_marked_review_only"] = st.checkbox(
        "Export package is marked reference-only and human-review-required.",
        value=checks.get("export_marked_review_only", False),
        key="export_marked_review_only",
    )

    ready_count = sum(1 for value in checks.values() if value)
    st.progress(ready_count / len(checks))
    st.write(f"{ready_count} of {len(checks)} review checks complete.")
    return checks


def _export_panel(
    metadata: dict[str, Any],
    points: Sequence[EngineeringPoint],
    calibration_valid: bool,
    validation: dict[str, Any],
    review_checks: dict[str, bool],
) -> None:
    st.subheader("Export Review")
    st.caption("Exports are temporary Streamlit downloads for local review.")
    review_ready = all(review_checks.values())
    engineer_review_acknowledgment = st.checkbox(
        "Engineer-review acknowledgment: I understand this package is decision "
        "support only and requires qualified approval before downstream use.",
        key="engineer_review_acknowledgment",
    )
    export_ready = (
        bool(points)
        and calibration_valid
        and validation["valid"]
        and review_ready
        and engineer_review_acknowledgment
    )

    status_rows = [
        {
            "gate": "Valid calibration",
            "status": "ready" if calibration_valid else "blocked",
        },
        {"gate": "Converted points", "status": "ready" if points else "blocked"},
        {
            "gate": "Fit validation",
            "status": "ready" if validation["valid"] else "blocked",
        },
        {"gate": "Review checklist", "status": "ready" if review_ready else "blocked"},
        {
            "gate": "Engineer-review acknowledgment",
            "status": "ready" if engineer_review_acknowledgment else "blocked",
        },
    ]
    st.dataframe(status_rows, use_container_width=True, hide_index=True)
    st.caption("Reference-only plot data. Not guaranteed by a manufacturer.")

    if not export_ready:
        st.info("Complete the blocked export gates before generating downloads.")

    if st.button("Generate review export package", disabled=not export_ready):
        with TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            package_paths = _write_export_package(temp_root, metadata, points)
            st.success("Export package generated for local review.")
            st.image(
                str(package_paths["overlay"]),
                caption="Synthetic overlay review image",
            )
            _download_export_package(package_paths)


def _download_export_package(package_paths: dict[str, Path]) -> None:
    st.download_button(
        "Download overlay PNG",
        data=package_paths["overlay"].read_bytes(),
        file_name=package_paths["overlay"].name,
        mime="image/png",
    )
    for label, path, mime in [
        ("Download CSV", package_paths["csv"], "text/csv"),
        ("Download JSON", package_paths["json"], "application/json"),
        ("Download Python lookup", package_paths["python"], "text/x-python"),
        ("Download MATLAB lookup", package_paths["matlab"], "text/plain"),
        ("Download report", package_paths["report"], "text/markdown"),
    ]:
        st.download_button(
            label,
            data=path.read_text(encoding="utf-8"),
            file_name=path.name,
            mime=mime,
        )


def _write_export_package(
    root: Path,
    metadata: dict[str, Any],
    points: Sequence[EngineeringPoint],
) -> dict[str, Path]:
    function_name = f"lookup_{safe_name(metadata['curve_name'])}"
    csv_path = root / "digitized_curve_points.csv"
    json_path = root / "curve_metadata.json"
    overlay_path = root / "overlay_forward_voltage_vs_current.png"
    python_path = root / f"{function_name}.py"
    matlab_path = root / f"{function_name}.m"
    report_path = root / "extraction_report.md"

    write_points_csv(csv_path, metadata, points)
    write_metadata_json(json_path, metadata)
    write_overlay_png(overlay_path, points)
    write_python_lookup(python_path, function_name, metadata, points)
    write_matlab_lookup(matlab_path, function_name, metadata, points)
    write_markdown_report(
        report_path,
        metadata,
        points,
        overlay_path=overlay_path.name,
        csv_path=csv_path.name,
        json_path=json_path.name,
        python_path=python_path.name,
        matlab_path=matlab_path.name,
    )
    return {
        "csv": csv_path,
        "json": json_path,
        "overlay": overlay_path,
        "python": python_path,
        "matlab": matlab_path,
        "report": report_path,
    }


def _editor_rows(edited_rows: Any) -> list[dict[str, Any]]:
    if hasattr(edited_rows, "to_dict"):
        try:
            return [dict(row) for row in edited_rows.to_dict("records")]
        except TypeError:
            pass
    return [dict(row) for row in edited_rows]


def _index_or_zero(options: Sequence[str], value: str) -> int:
    try:
        return list(options).index(value)
    except ValueError:
        return 0


if __name__ == "__main__":
    main()
