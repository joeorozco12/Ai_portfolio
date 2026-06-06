"""Generate synthetic digitizer portfolio artifacts."""

from __future__ import annotations

from pathlib import Path

from led_digitizer.exports import (
    safe_name,
    write_export_package,
    write_markdown_report,
    write_matlab_lookup,
    write_metadata_json,
    write_overlay_png,
    write_points_csv,
    write_python_lookup,
)
from led_digitizer.sample_project import SAMPLE_METADATA, load_sample_points


PROJECT_ROOT = Path(__file__).resolve().parent
DATA_PATH = PROJECT_ROOT / "data" / "synthetic_manual_points.csv"
OUTPUT_ROOT = PROJECT_ROOT / "outputs"
EXPORT_PACKAGE_ROOT = PROJECT_ROOT / "exports" / "demo_export_package"


def main() -> None:
    points = load_sample_points(DATA_PATH)
    curve_slug = safe_name(SAMPLE_METADATA["curve_name"])
    function_name = f"lookup_{curve_slug}"

    csv_path = OUTPUT_ROOT / "digitized_curve_points.csv"
    json_path = OUTPUT_ROOT / "curve_metadata.json"
    overlay_path = OUTPUT_ROOT / "overlay_forward_voltage_vs_current.png"
    python_path = OUTPUT_ROOT / "python" / f"{function_name}.py"
    matlab_path = OUTPUT_ROOT / "matlab" / f"{function_name}.m"
    report_path = OUTPUT_ROOT / "extraction_report.md"

    write_points_csv(csv_path, SAMPLE_METADATA, points)
    write_metadata_json(json_path, SAMPLE_METADATA)
    write_overlay_png(overlay_path, points)
    write_python_lookup(python_path, function_name, SAMPLE_METADATA, points)
    write_matlab_lookup(matlab_path, function_name, SAMPLE_METADATA, points)
    write_markdown_report(
        report_path,
        SAMPLE_METADATA,
        points,
        overlay_path="outputs/overlay_forward_voltage_vs_current.png",
        csv_path="outputs/digitized_curve_points.csv",
        json_path="outputs/curve_metadata.json",
        python_path=f"outputs/python/{function_name}.py",
        matlab_path=f"outputs/matlab/{function_name}.m",
    )
    package_paths = write_export_package(EXPORT_PACKAGE_ROOT, SAMPLE_METADATA, points)

    print(f"Generated {len(points)} digitized points")
    print(f"Wrote {csv_path.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {json_path.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {overlay_path.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {python_path.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {matlab_path.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {report_path.relative_to(PROJECT_ROOT)}")
    for path in package_paths.values():
        print(f"Wrote {path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
