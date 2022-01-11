"""Build models and run Moldflow simulations.

There is a 'models.yaml' configuration file to define models. These are created and
mold filling simulations are performed.
"""
import os
import subprocess

import madcad
import pythoncom
import win32com.client
import yaml

import geometry

# Load the configuration file
yaml_file = open("random_models.yaml", "r")
config = yaml.safe_load(yaml_file)

# Path to Autodesk Moldflow
MF = os.path.join("C:/", "Program Files", "Autodesk", "Moldflow Insight 2021.1", "bin")

# Define outputs
OUT = {
    "1610": "fill_time",
    "1653": "weld_surface",
    "1722": "weld_line",
}

for name, props in config.items():
    # Print current model name
    print(f"Running model '{name}'.")

    # Create workdir
    path = os.path.abspath(os.path.join("data", name))
    os.mkdir(path)

    # Build geometry
    h = props["thickness"]
    part = geometry.build_plate(*props["plate"], h)
    for hole in props["holes"]:
        cylinder = geometry.build_cylinder(hole[0], hole[1], h, hole[2])
        part = madcad.difference(part, cylinder)

    # Export part (needs numpy-stl)
    geo_name = f"{name}.stl"
    madcad.write(part, os.path.join(path, geo_name))

    # Connect to Moldflow Synergy
    Synergy = win32com.client.Dispatch("synergy.Synergy")
    Synergy.SetUnits("Metric")

    # Create project
    Synergy.NewProject(name, path)

    # Loop through injection locations
    for location, direction in props["injection_locations"]:
        print(f" - Injection location {location}...")
        # Import stl file
        ImpOpts = Synergy.ImportOptions
        ImpOpts.MeshType = "3D"
        ImpOpts.Units = "mm"
        Synergy.ImportFile(f"{name}.stl", ImpOpts, False)

        # Rename study
        study_name = f"{name}_{int(location[0])}_{int(location[1])}_study"
        Project = Synergy.Project
        Project.RenameItemByName(f"{name}_study", "Study", study_name)

        # Set injection location
        BoundaryConditions = Synergy.BoundaryConditions
        Direction = Synergy.CreateVector
        Direction.SetXYZ(*direction)
        Location = Synergy.CreateVector
        Location.SetXYZ(*location)
        EntList = BoundaryConditions.CreateNDBCAtXYZ(
            Location, Direction, 40000, pythoncom.Nothing
        )

        # Build mesh
        MeshGenerator = Synergy.MeshGenerator
        MeshGenerator.EdgeLength = 2.5
        MeshGenerator.Generate

        # Set number of intermediate results
        PropEd = Synergy.PropertyEditor
        Prop = PropEd.FindProperty(10080, 1)
        DVec = Synergy.CreateDoubleArray
        DVec.AddDouble(50)
        Prop.FieldValues(910, DVec)
        PropEd.CommitChanges("Process Conditions")

        # Save the sdy files
        StudyDoc = Synergy.StudyDoc
        StudyDoc.Save

        # Save mesh as Patran file
        Project = Synergy.Project
        Project.ExportModel(os.path.join(path, study_name + ".pat"))

        # Run the simulation
        p = subprocess.Popen(
            [os.path.join(MF, "runstudy.exe"), study_name + ".sdy",],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=path,
        )
        (output, err) = p.communicate()
        with open(os.path.join(path, study_name + ".log"), "w") as file:
            file.write(output.decode("windows-1252").strip())

        for key, value in OUT.items():
            p = subprocess.Popen(
                [os.path.join(MF, "studyrlt.exe"), study_name + ".sdy", "-xml", key,],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd=path,
            )
            (output, err) = p.communicate()
            temp_name = os.path.join(path, f"{study_name}.xml")
            os.rename(temp_name, temp_name.replace(".xml", f"_{value}.xml"))

        print("          ...done.")
