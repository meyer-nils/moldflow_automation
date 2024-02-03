import os
import subprocess

import pythoncom
import win32com.client

MOLDFLOW_PATH = "C:/Program Files/Autodesk/Moldflow Insight 2023/bin"

# Connect to Moldflow Synergy
Synergy = win32com.client.Dispatch("synergy.Synergy")
Synergy.SetUnits("Metric")

# Import stl file
ImpOpts = Synergy.ImportOptions
ImpOpts.MeshType = "3D"
ImpOpts.Units = "mm"
Synergy.ImportFile("disk.stl", ImpOpts, False)

# Set injection location
BoundaryConditions = Synergy.BoundaryConditions
Direction = Synergy.CreateVector
Direction.SetXYZ(0, 0, 1)
Location = Synergy.CreateVector
Location.SetXYZ(0, 0, 0)
EntList = BoundaryConditions.CreateNDBCAtXYZ(
    Location, Direction, 40000, pythoncom.Nothing
)

# Build mesh
MeshGenerator = Synergy.MeshGenerator
MeshGenerator.EdgeLength = 0.5
MeshGenerator.Generate

# Save the sdy files
StudyDoc = Synergy.StudyDoc
StudyDoc.Save

# Run the simulation
p = subprocess.Popen(
    [os.path.join(MOLDFLOW_PATH, "runstudy.exe"), "disk_study.sdy"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
)
(output, err) = p.communicate()
with open("disk_study.log", "w") as file:
    file.write(output.decode("windows-1252").strip())
