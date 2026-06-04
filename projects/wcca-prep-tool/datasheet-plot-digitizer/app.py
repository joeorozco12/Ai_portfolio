"""Streamlit shell for the LED Datasheet Plot Digitizer."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from led_digitizer.calibration import AxisCalibration, CurveCalibration
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


def main() -> None:
    if st is None:
        print("Streamlit is not installed. Install requirements.txt and run:")
        print("streamlit run app.py")
        return

    st.set_page_config(page_title="LED Datasheet Plot Digitizer", layout="wide")
    st.title("LED Datasheet Plot Digitizer")
    st.caption(SYNTHETIC_LABEL)
    st.warning(HUMAN_REVIEW_NOTE)

    state = st.session_state
    state.setdefault("metadata", dict(SAMPLE_METADATA))
    state.setdefault("points", [])

    import_tab, calibration_tab, points_tab, export_tab = st.tabs(
        ["Import", "Calibration", "Curve Points", "Export"]
    )

    with import_tab:
        state["metadata"] = _metadata_panel()
        uploaded_file = st.file_uploader(
            "PDF or image", type=["pdf", "png", "jpg", "jpeg"]
        )
        if uploaded_file is not None:
            _render_upload_preview(uploaded_file)
        state["metadata"]["crop_region_px"] = _crop_panel()

    with calibration_tab:
        x_calibration, y_calibration = _calibration_panel(state["metadata"])
        state["metadata"]["axis_calibration"] = {
            "x_pixel_low": x_calibration.pixel_low,
            "x_pixel_high": x_calibration.pixel_high,
            "x_value_low": x_calibration.value_low,
            "x_value_high": x_calibration.value_high,
            "y_pixel_low": y_calibration.pixel_low,
            "y_pixel_high": y_calibration.pixel_high,
            "y_value_low": y_calibration.value_low,
            "y_value_high": y_calibration.value_high,
        }

    calibration = CurveCalibration(x_axis=x_calibration, y_axis=y_calibration)
    with points_tab:
        state["points"] = _points_panel(calibration)

    with export_tab:
        _export_panel(state["metadata"], state["points"])


def _metadata_panel() -> dict:
    st.subheader("Curve Metadata")
    left, right = st.columns(2)
    metadata = dict(SAMPLE_METADATA)
    with left:
        metadata["part_number"] = st.text_input("LED identifier", metadata["part_number"])
        metadata["manufacturer"] = st.text_input("Source label", metadata["manufacturer"])
        metadata["curve_name"] = st.text_input("Curve name", metadata["curve_name"])
        metadata["source_page"] = st.text_input("Source page", metadata["source_page"])
    with right:
        metadata["datasheet_source"] = st.text_input(
            "Datasheet source", metadata["datasheet_source"]
        )
        metadata["digitization_method"] = st.selectbox(
            "Digitization method",
            [
                "manual_calibration_plus_manual_curve_pick",
                "manual_calibration_plus_assisted_curve_pick",
            ],
        )
        metadata["review_status"] = st.selectbox(
            "Review status",
            ["draft_extraction", "engineer_reviewed_demo", "rejected_redo_calibration"],
        )
    return metadata


def _render_upload_preview(uploaded_file) -> None:
    suffix = Path(uploaded_file.name).suffix.lower()
    if suffix == ".pdf":
        if fitz is None:
            st.info("PDF rendering requires PyMuPDF from requirements.txt.")
            return
        document = fitz.open(stream=uploaded_file.getvalue(), filetype="pdf")
        page_index = st.number_input(
            "Page index", min_value=0, max_value=len(document) - 1, value=0, step=1
        )
        page = document[int(page_index)]
        pixmap = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
        st.image(pixmap.tobytes("png"))
    else:
        st.image(uploaded_file.getvalue())


def _crop_panel() -> dict:
    st.subheader("Crop Region")
    left, top, width, height = st.columns(4)
    with left:
        crop_left = st.number_input("Crop left px", value=60, min_value=0)
    with top:
        crop_top = st.number_input("Crop top px", value=40, min_value=0)
    with width:
        crop_width = st.number_input("Crop width px", value=540, min_value=1)
    with height:
        crop_height = st.number_input("Crop height px", value=410, min_value=1)
    return {
        "left": int(crop_left),
        "top": int(crop_top),
        "width": int(crop_width),
        "height": int(crop_height),
    }


def _calibration_panel(metadata: dict) -> tuple[AxisCalibration, AxisCalibration]:
    st.subheader("Axis Calibration")
    x_left, x_right, y_left, y_right = st.columns(4)
    with x_left:
        x_pixel_low = st.number_input("X low pixel", value=80.0)
        x_value_low = st.number_input("X low value", value=2.5)
    with x_right:
        x_pixel_high = st.number_input("X high pixel", value=560.0)
        x_value_high = st.number_input("X high value", value=4.5)
    with y_left:
        y_pixel_low = st.number_input("Y low pixel", value=420.0)
        y_value_low = st.number_input("Y low value", value=0.0)
    with y_right:
        y_pixel_high = st.number_input("Y high pixel", value=60.0)
        y_value_high = st.number_input("Y high value", value=4000.0)

    x_scale = st.selectbox("X scale", ["linear", "log"], index=0)
    y_scale = st.selectbox("Y scale", ["linear", "log"], index=0)
    return (
        AxisCalibration(
            pixel_low=x_pixel_low,
            pixel_high=x_pixel_high,
            value_low=x_value_low,
            value_high=x_value_high,
            scale=x_scale,
            label=metadata["x_axis"]["label"],
            unit=metadata["x_axis"]["unit"],
        ),
        AxisCalibration(
            pixel_low=y_pixel_low,
            pixel_high=y_pixel_high,
            value_low=y_value_low,
            value_high=y_value_high,
            scale=y_scale,
            label=metadata["y_axis"]["label"],
            unit=metadata["y_axis"]["unit"],
        ),
    )


def _points_panel(calibration: CurveCalibration):
    st.subheader("Curve Points")
    extraction_mode = st.radio("Extraction mode", ["Manual", "Assisted"], horizontal=True)
    if extraction_mode == "Assisted" and cv2 is None:
        st.info("Assisted extraction requires opencv-python-headless from requirements.txt.")
    seed_points = load_sample_points(SAMPLE_POINTS_PATH)
    rows = [
        {
            "point_id": point.point_id,
            "source_pixel_x": point.source_pixel_x,
            "source_pixel_y": point.source_pixel_y,
            "review_status": point.review_status,
            "notes": point.notes,
        }
        for point in seed_points
    ]
    edited = st.data_editor(rows, num_rows="dynamic", use_container_width=True)
    points = []
    for row in edited:
        try:
            points.append(
                calibration.pixel_to_engineering(
                    point_id=str(row["point_id"]),
                    source_pixel_x=float(row["source_pixel_x"]),
                    source_pixel_y=float(row["source_pixel_y"]),
                    review_status=str(row["review_status"]),
                    notes=str(row.get("notes", "")),
                )
            )
        except (KeyError, TypeError, ValueError):
            st.warning("One or more rows could not be converted.")
            return []

    st.dataframe(
        [
            {
                "point_id": point.point_id,
                "x": round(point.x, 6),
                "y": round(point.y, 6),
                "review_status": point.review_status,
            }
            for point in points
        ],
        use_container_width=True,
    )
    return points


def _export_panel(metadata: dict, points) -> None:
    st.subheader("Review And Export")
    engineer_review = st.checkbox("Engineer review completed for demo export")
    st.caption("Reference-only plot data. Not guaranteed by a manufacturer.")
    if st.button("Generate export package", disabled=not points or not engineer_review):
        with TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            package_paths = _write_export_package(temp_root, metadata, points)
            st.success("Export package generated for review.")
            st.image(str(package_paths["overlay"]))
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


def _write_export_package(root: Path, metadata: dict, points) -> dict[str, Path]:
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


if __name__ == "__main__":
    main()
