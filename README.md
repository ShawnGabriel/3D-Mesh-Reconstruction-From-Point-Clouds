# 3D Mesh Reconstruction From Point Clouds
This repository is an implementation of SMRVIS architecture proposed in _SMRVIS: Point cloud extraction from 3-D ultrasound for non-destructive testing_;Tang, Lisa YW; arXiv 2023

---

## Dependencies
Necessary packages can be found above in `packages.txt`.

## Dataset
Acquired from DarkVision DeepView Competition with specifications below:
#### Training dataset:
* 89 raw volumetric ultrasound images
* 5 reference 3D meshes, corresponding to the volumetric scans 001-005


#### Testing dataset:
* 10 raw volumetric ultrasound images
* 10 reference 3D meshes


#### Raw Volumetric Image Meta Info (for visualization and mesh alignment):
* origin - (0, 0, 0)
* spacing: (0.49479, 0.49479, 0.3125)
* data type: unsigned short int
* volume dimension: (768, 768, 1280)


#### Data Visualization:
We recommend using ParaView 5.9.1 for visualization purposes.

---

## Instructions
> Note :
> * Make sure to change the directory of files where needed.
> * In our runs, we used an Nvidia L4 GPU (Through Google Colab Pro)
1. Clone this repository
2. If needed, `pip install -r packages.txt` to install the required packages
3. Adjust all the of filepaths on `c1load.py`, `c2.py`, and `test.py`.
4. Run python `test.py`.
5. Run python `metrics.py`.
