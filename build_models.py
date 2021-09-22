import os
import subprocess
import win32com.client
import pythoncom

path = os.path.join(
    "C:\\Users",
    "ol4022",
    "Documents",
    "Repositories",
    "moldflow_automation",
    "data",
)

RUNSTUDY = os.path.join(
    "C:/",
    "Program Files",
    "Autodesk",
    "Moldflow Insight 2021",
    "bin",
    "runstudy.exe",
)

for subdir, dirs, files in os.walk(path):
    for file in files:
        if file.endswith((".stl")):
            print(f"Building Moldflow model for {file}")

            # Connect to Moldflow Synergy
            Synergy = win32com.client.Dispatch("synergy.Synergy")
            Synergy.SetUnits("Metric")

            # Create project
            Synergy.NewProject("plate", subdir)

            # Import stl file
            ImpOpts = Synergy.ImportOptions
            ImpOpts.MeshType = "3D"
            Synergy.ImportFile(file, ImpOpts, False)

            # Build mesh
            MeshGenerator = Synergy.MeshGenerator
            MeshGenerator.EdgeLength = 5
            StudyDoc = Synergy.StudyDoc
            StudyDoc.MeshNow(True)
            StudyDoc.Save

            # BoundaryConditions = Synergy.BoundaryConditions
            # Direction = Synergy.CreateVector
            # Direction.SetXYZ(0, 1, -0)
            # Location = Synergy.CreateVector
            # Location.SetXYZ(0.0, 0.0, 0.0)
            # EntList = BoundaryConditions.CreateNDBCAtXYZ(
            #     Location, Direction, 40000, pythoncom.Nothing
            # )

            # subprocess.Popen(
            #     [RUNSTUDY, name], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            # )
