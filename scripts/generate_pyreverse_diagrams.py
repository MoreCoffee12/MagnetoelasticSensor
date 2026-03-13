from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


PACKAGE_NAME = "magnetoelasticsensor"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "diagrams" / "pyreverse"
GEOMETRY_PERMEANCE_MODULES = [
    f"{PACKAGE_NAME}.geometry",
    f"{PACKAGE_NAME}.air_gap_permeance",
    f"{PACKAGE_NAME}.core_permeance",
    f"{PACKAGE_NAME}.cross_leakage_permeance",
    f"{PACKAGE_NAME}.target_permeance",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate pyreverse diagrams for the magnetoelasticsensor package. "
            "This creates a package diagram for the whole package and a class "
            "diagram focused on geometry and permeance modules."
        )
    )
    parser.add_argument(
        "--format",
        default="pdf",
        choices=("dot", "png", "svg", "pdf"),
        help="Diagram output format. Use 'dot' if Graphviz is not installed.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory where pyreverse output files will be written.",
    )
    parser.add_argument(
        "--skip-package-diagram",
        action="store_true",
        help="Do not generate the whole-package dependency diagram.",
    )
    parser.add_argument(
        "--skip-permeance-class-diagram",
        action="store_true",
        help="Do not generate the geometry/permeance class diagram.",
    )
    return parser.parse_args()


def resolve_pyreverse_command() -> list[str]:
    pyreverse_executable = shutil.which("pyreverse")
    if pyreverse_executable:
        return [pyreverse_executable]

    return [sys.executable, "-m", "pylint.pyreverse.main"]


def validate_environment(output_format: str) -> None:
    if shutil.which("dot") is None and output_format != "dot":
        raise RuntimeError(
            "Graphviz 'dot' was not found on PATH. Install Graphviz or rerun "
            "with --format dot."
        )


def run_pyreverse(arguments: list[str]) -> None:
    command = resolve_pyreverse_command() + arguments
    try:
        subprocess.run(
            command,
            cwd=PROJECT_ROOT,
            check=True,
        )
    except FileNotFoundError as exc:
        raise RuntimeError(
            "pyreverse was not found. Install pylint with 'pip install pylint'."
        ) from exc
    except subprocess.CalledProcessError as exc:
        formatted_command = " ".join(command)
        raise RuntimeError(
            f"pyreverse command failed with exit code {exc.returncode}: {formatted_command}"
        ) from exc


def build_package_diagram(output_dir: Path, output_format: str) -> list[Path]:
    run_pyreverse(
        [
            "-o",
            output_format,
            "-d",
            str(output_dir),
            "-p",
            PACKAGE_NAME,
            PACKAGE_NAME,
        ]
    )
    return [
        output_dir / f"packages_{PACKAGE_NAME}.{output_format}",
        output_dir / f"classes_{PACKAGE_NAME}.{output_format}",
    ]


def build_geometry_permeance_diagram(output_dir: Path, output_format: str) -> list[Path]:
    project_name = "geometry_permeance"
    run_pyreverse(
        [
            "-o",
            output_format,
            "-d",
            str(output_dir),
            "-p",
            project_name,
            *GEOMETRY_PERMEANCE_MODULES,
        ]
    )
    return [
        output_dir / f"classes_{project_name}.{output_format}",
        output_dir / f"packages_{project_name}.{output_format}",
    ]


def main() -> int:
    args = parse_args()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    validate_environment(args.format)

    generated_files: list[Path] = []

    if not args.skip_package_diagram:
        generated_files.extend(build_package_diagram(output_dir, args.format))

    if not args.skip_permeance_class_diagram:
        generated_files.extend(build_geometry_permeance_diagram(output_dir, args.format))

    print("Generated pyreverse outputs:")
    for path in generated_files:
        print(f" - {path}")

    print("\nPrimary files to use:")
    if not args.skip_package_diagram:
        print(f" - Whole-package diagram: {output_dir / ('packages_' + PACKAGE_NAME + '.' + args.format)}")
    if not args.skip_permeance_class_diagram:
        print(
            " - Geometry/permeance class diagram: "
            f"{output_dir / ('classes_geometry_permeance.' + args.format)}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())