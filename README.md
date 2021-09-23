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
