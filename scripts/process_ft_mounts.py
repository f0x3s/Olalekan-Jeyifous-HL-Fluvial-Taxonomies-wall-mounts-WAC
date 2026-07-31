from pathlib import Path
import subprocess
import tempfile

# Requires stl_cmd
# https://github.com/AllwineDesigns/stl_cmd

scad_label_file = Path("./scripts/generate_label.scad")
scad_thermal_expansion_ring_file = Path("./scripts/thermal_expansion_ring.scad")

folder = Path("./3d-files/isolated-mount-export")
output_folder = Path("ready-for-print")
output_folder.mkdir(exist_ok=True)

input_stl = list(folder.glob("*.stl"))

with tempfile.TemporaryDirectory() as temp_dir:

    temp_folder = Path(temp_dir)

    # Center the STL files and export to a a temporary folder
    for stl in input_stl:
        output_stl = temp_folder / f"{stl.stem}_centered.stl{stl.suffix}"

        # Center the STL file using the stl_zero command from stl_cmd
        subprocess.run([
            "stl_zero",
            "-base",
            str(stl),
            str(output_stl)
        ], check = True)

        print(f"Centered {stl.name}")

    for stl in temp_folder.glob("*_centered.stl"):

        label = temp_folder / f"{stl.stem}_label.stl"
        output_stl = temp_folder / f"{stl.stem}_tagged.stl{stl.suffix}"

        output_stl = output_folder / stl.name

        # Generate a label STL file using OpenSCAD and the generate_label.scad script
        subprocess.run([
            "openscad",
            "--export-format", "binstl",
            "-o", str(label),
            "-D", f'label_text="{stl.stem.replace("_centered", "")}"',
            str(scad_label_file),
        ], check=True)

        # Perform a boolean union operation to combine the label with the centered STL file using stl_cmd
        subprocess.run([
            "stl_boolean",
            "-a", str(stl),
            "-b", str(label),
            "-u", str(output_stl),
        ], check=True)
        
        print(f"Labeled {stl.name}")

        # generate a thermal expansion compensation ring STL file using OpenSCAD and the thermal_expansion_ring.scad script
        # this fixes issue where print bulges at at transition between density regions
        cut_tool_stl = Path(temp_dir) / "cut_tool.stl"

        subprocess.run([
                "openscad",
                "--export-format", "binstl",
                "-o", str(cut_tool_stl),
                str(scad_thermal_expansion_ring_file),
            ], check=True)

        for stl in folder.glob("*_tagged.stl"):
            output_stl = output_folder / stl.name
    
            subprocess.run([
                "stl_boolean",
                "-a", str(stl),
                "-b", str(cut_tool_stl),
                "-d",
                str(output_stl)
            ], check=True)
    
            print(f"thermally compensated STL: {output_stl}")
