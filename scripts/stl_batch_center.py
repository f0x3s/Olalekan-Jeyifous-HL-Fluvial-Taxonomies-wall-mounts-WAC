from pathlib import Path
import subprocess

folder = Path(".")
output_folder = Path("centered-stls")

output_folder.mkdir(exist_ok=True)

input_stl = list(folder.glob("*.stl"))

for stl in input_stl:
    output_file = output_folder / f"{stl.stem}-centered.stl{stl.suffix}"

    subprocess.run(
        ["stl_zero", "-base", str(stl), str(output_file)],
        check = True
    )

print(f"Centered {len(input_stl)} STL files and saved to {output_folder}")