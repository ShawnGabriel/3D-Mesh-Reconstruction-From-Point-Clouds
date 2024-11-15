# prior to running the code below make sure to run
# pip install ninja git+https://github.com/NVIDIAGameWorks/kaolin

import numpy as np
import pyvista as pv
from scipy.spatial.distance import cdist

def load_ply(file_path):
    """
    Load point cloud from .ply file using pyvista
    """
    mesh = pv.read(file_path)
    # Assuming the point cloud is stored as the mesh points (vertices)
    return mesh.points

def load_npz(file_path):
    """
    Load point cloud from .npz file.
    Assumes that the file contains a key 'points' for the point cloud data
    """
    with np.load(file_path) as data:
        x_array = data['x']
        y_array = data['y']
        z_array = data['z']
        return np.column_stack((x_array, y_array, z_array))  # Adjust if your npz contains a different key

# Example usage
ply_file = "/content/drive/MyDrive/DarkVision/testing/meshes/scan_001.ply"   # Path to .ply file
npz_file = "/content/drive/MyDrive/DarkVision/results/scan_001.npz"  # Path to .npz file containing 'points'

# Load the point clouds from both files
pointcloud_01 = load_ply(ply_file)
pointcloud_02 = load_npz(npz_file)

import torch
from kaolin.metrics.pointcloud import f_score

# Convert both point clouds to the same type, e.g., float32
pointcloud_01 = torch.tensor(pointcloud_01[np.newaxis, :, :]).to('cuda:0').float()
pointcloud_02 = torch.tensor(pointcloud_02[np.newaxis, :, :]).to('cuda:0').float()

# Now, compute the F-score
print(f_score(pointcloud_01, pointcloud_01, radius=0.1, eps=1e-08))
print(f_score(pointcloud_01, pointcloud_02, radius=0.1, eps=1e-08))
print(f_score(pointcloud_01, pointcloud_02, radius=0.5, eps=1e-08))
print(f_score(pointcloud_01, pointcloud_02, radius=1.0, eps=1e-08))


from scipy.spatial.distance import directed_hausdorff

# Move tensors to CPU, convert to NumPy arrays, and remove extra dimension
pointcloud_01_np = pointcloud_01.cpu().numpy().squeeze()
pointcloud_02_np = pointcloud_02.cpu().numpy().squeeze()

# Compute the Hausdorff distance
d, _, _ = directed_hausdorff(pointcloud_01_np, pointcloud_01_np)
print("Hausdorff distance between PC1 and itself:", d)

d, _, _ = directed_hausdorff(pointcloud_01_np, pointcloud_02_np)
print("Hausdorff distance between PC1 and PC2:", d)

import torch
from kaolin.metrics.pointcloud import chamfer_distance

# Compute Chamfer distance
print(chamfer_distance(pointcloud_01, pointcloud_01))
print(chamfer_distance(pointcloud_01, pointcloud_02))

from kaolin.metrics.pointcloud import sided_distance
import torch

def mean_surface_distance(p1: torch.Tensor, p2: torch.Tensor) -> float:
    msd = torch.sum(sided_distance(p1, p2)[0]).detach().cpu().numpy() + torch.sum(sided_distance(p2, p1)[0]).detach().cpu().numpy()
    msd /= p1.size()[0] + p2.size()[0]  # Adjust indexing based on the point count dimension
    return msd

# Ensure both point clouds are 3-dimensional and on the correct device
pointcloud_01_cuda = torch.tensor(pointcloud_01).to('cuda:0').float()
pointcloud_02_cuda = torch.tensor(pointcloud_02).to('cuda:0').float()

print(mean_surface_distance(pointcloud_01_cuda, pointcloud_01_cuda))
print(mean_surface_distance(pointcloud_01_cuda, pointcloud_02_cuda))


from kaolin.metrics.pointcloud import sided_distance
import torch

def residual_mean_surface_distance(p1: torch.Tensor, p2: torch.Tensor) -> float:
    rmsd = torch.sum(torch.square(sided_distance(p1, p2)[0])).detach().cpu().numpy() + torch.sum(torch.square(sided_distance(p2, p1)[0])).detach().cpu().numpy()
    rmsd /= p1.size(0) + p2.size(0)  # Use the correct dimension for point count
    return rmsd

# Ensure both point clouds are on the same device and have the same type
pointcloud_01_cuda = torch.tensor(pointcloud_01).to('cuda:0').float()
pointcloud_02_cuda = torch.tensor(pointcloud_02).to('cuda:0').float()

# Compute the Residual Mean Surface Distance
print(residual_mean_surface_distance(pointcloud_01_cuda, pointcloud_01_cuda))
print(residual_mean_surface_distance(pointcloud_01_cuda, pointcloud_02_cuda))
