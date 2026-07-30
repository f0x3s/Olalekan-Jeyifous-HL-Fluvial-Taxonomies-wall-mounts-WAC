from pathlib import Path
import subprocess
import tempfile

folder = Path("./centered-stls")
scad_file = Path(__file__).resolve().parent / "add_label.scad"
output_folder = folder / "labeled-stls"

output_folder.mkdir(exist_ok=True)

with tempfile.TemporaryDirectory() as temp_dir:
    temp_folder = Path(temp_dir)

    for stl in folder.glob("*.stl"):
        labeled_stl = temp_folder / f"{stl.stem}_labeled.stl"
        output_stl = output_folder / stl.name

        subprocess.run([
            "openscad",
            "-o", str(labeled_stl),
            "-D", f'label_text="{stl.stem}"',
            str(scad_file),
        ], check=True)

        subprocess.run([
            "stl_boolean",
            "-a", str(stl),
            "-b", str(labeled_stl),
            "-u", str(output_stl),
        ], check=True)

        print(f"Labeled {stl.name} and saved to {output_stl}")

