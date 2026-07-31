from pathlib import Path
import subprocess
import tempfile
import pymeshfix

# Requires stl_cmd
# https://github.com/AllwineDesigns/stl_cmd

scad_label_file = Path("./scripts/generate_label.scad")
scad_thermal_expansion_ring_file = Path("./scripts/thermal_expansion_ring.scad")

folder = Path("./3d-files/isolated-mount-export")
output_folder = Path("./ready-for-print")
output_folder.mkdir(parents=True, exist_ok=True)

input_stls = list(folder.glob("*.stl"))

# center, label, and thermally compensate the STL files
with tempfile.TemporaryDirectory() as temp_dir:

    temp_folder = Path(temp_dir)

    # generate a thermal expansion compensation ring STL file using OpenSCAD and the thermal_expansion_ring.scad script
    # this fixes issue where print bulges at at transition between density regions
    cut_tool_stl = temp_folder / "cut_tool.stl"

    subprocess.run([
            "openscad",
            "--export-format", "binstl",
            "-o", str(cut_tool_stl),
            str(scad_thermal_expansion_ring_file),
        ], check=True)

    # Center the STL files and export to a a temporary folder
    for input_stl in input_stls:
        centered_stl = temp_folder / f"{input_stl.stem}_centered.stl"
        label_stl = temp_folder / f"{input_stl.stem}_label.stl"
        tagged_stl = temp_folder / f"{input_stl.stem}_tagged.stl"
        output_stl = output_folder / f"{input_stl.stem}_for-print.stl"
        
        # Center the STL file and place its base at z=0 using the stl_zero command from stl_cmd
        subprocess.run([
            "stl_zero",
            "-base",
            str(input_stl),
            str(centered_stl)
        ], check = True)

        print(f"Centered {input_stl.name}")

        # Generate a label STL file from input filename using OpenSCAD and the generate_label.scad script
        subprocess.run([
            "openscad",
            "--export-format", "binstl",
            "-o", str(label_stl),
            "-D", f'label_text="{input_stl.stem}"',
            str(scad_label_file),
        ], check=True)

        # Perform a boolean union operation to combine the label with the centered STL file using stl_cmd
        subprocess.run([
            "stl_boolean",
            "-a", str(centered_stl),
            "-b", str(label_stl),
            "-u", str(tagged_stl),
        ], check=True)
        
        print(f"Labeled {input_stl.name}")

        # subtract the ring from the tagged STL file using stl_cmd to create a thermally compensated STL file
        subprocess.run([
            "stl_boolean",
            "-a", str(tagged_stl),
            "-b", str(cut_tool_stl),
            "-d", str(output_stl)
        ], check=True)

        print(f"thermally compensated STL: {output_stl}")

# Repair completed output STL files
for output_stl in sorted(output_folder.glob("*_for-print.stl")):

    repaired_stl = output_stl.with_suffix(".repairing.stl")

    try:
        pymeshfix.clean_from_file(
            str(output_stl),
            str(repaired_stl),
            verbose=True,
            joincomp=True,
        )

        if not repaired_stl.exists() or repaired_stl.stat().st_size == 0:
            raise RuntimeError(f"Repair failed for {output_stl.name}, no output file generated.")

        repaired_stl.replace(output_stl)

        print(f"Repaired {output_stl.name}")

    except Exception as e:
        repaired_stl.unlink(missing_ok=True)

        print(f"Error repairing {output_stl.name}: {e}\n")
