from pathlib import Path
import subprocess
import tempfile

folder = Path("./labeled-stls")
scad_file = Path(__file__).resolve().parent / "thermal_expansion_ring.scad"
output_folder = Path(f"ready-for-print")

output_folder.mkdir(exist_ok=True)

with tempfile.TemporaryDirectory() as temp_dir:
    cut_tool_stl = Path(temp_dir) / "cut_tool.stl"

    subprocess.run([
        "openscad",
        "--export-format", "binstl",
        "-o", str(cut_tool_stl),
        str(scad_file),
    ], check=True)

    for stl in folder.glob("*.stl"):
        output_stl = output_folder / stl.name

        subprocess.run([
            "stl_boolean",
            "-a", str(stl),
            "-b", str(cut_tool_stl),
            "-d",
            str(output_stl)
        ], check=True)

        print(f"thermally compensated STL: {output_stl}")

