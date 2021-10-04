# Scope
This repo should provide some tools to automate Moldflow data creation.

# What are the requirements?
- Python >=3.7
  - pymadcad
  - numpy-stl
  - pyyaml
- Autodesk Moldflow 2021

# How is it supposed to work?
A variety of 3D geometries is created using pymadcad and saved as STL files. An Autodesk Moldflow model is created for each of these files and multiple studies are generated for each geometry. Here, injection locations and molding parameters are varied. Finally, the results are saved.

# How do I generate data?
Define models in the models.yaml file:

```
<model_name>:
  thickness: <plate thickness>
  plate: [<length>, <width>]
  holes:
    - [<pos_x>, <pos_y>, <radius>]
    - ...
  injection_locations:
    - [[<pos_x>, <pos_y>, <pos_z>],[<dir_x>, <dir_y>, <dir_z>]]\
    - ...
```

Then run the simulations:

```
python run.py
```

This generates a directory for each model named *model* in the *data* directory. The directory contains
- ** *model*.stl:** CAD model.
- ** *model*\_*X*\_*Y*\_study.log:** Simulation log file.
- ** *model*\_*X*\_*Y*\_study.pat:** Mesh in Patran format.
- ** *model*\_*X*\_*Y*\_study.png:** Preview image.
- ** *model*\_*X*\_*Y*\_study.sdy:** Moldflow study file setting up the simulation case.
- ** *model*\_*X*\_*Y*\_study.of1:** Binary filling results except weld lines and air traps.
- ** *model*\_*X*\_*Y*\_study.of2:** Binary weld lines and air trap results.
- ** *model*\_*X*\_*Y*\_study_fill_time.xml:** Fill time of each node.
- ** *model*\_*X*\_*Y*\_study_weld_surface.xml:** Nodes of the weld surface.
- ** *model*\_*X*\_*Y*\_study_weld_line.xml:** Nodes of the weld line.

for each pair of injection locations (*X*, *Y*).
