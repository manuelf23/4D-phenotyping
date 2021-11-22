import pandas as pd
import numpy as np
import open3d as o3d
import glob


def filter_and_promediate_pcd(pcd, nb_neighbors, std_ratio):

    pcd = pcd.groupby(['azimuth', 'laser_id']).mean()
    pcd = pcd.reset_index()
    # print(df.head())
    xyz = np.zeros((len(pcd['X']), 3))
    xyz[:, 0] = pcd['X']
    xyz[:, 1] = pcd['Y']
    xyz[:, 2] = pcd['Z']

    o3d_pcd = o3d.geometry.PointCloud()
    o3d_pcd.points = o3d.utility.Vector3dVector(xyz)
    cl, ind = o3d_pcd.remove_statistical_outlier(
        nb_neighbors=nb_neighbors, std_ratio=std_ratio)
    pcd2 = pcd.loc[ind]
    # print(pcd2)
    # xyz = np.asarray(cl.points)
    # pcd_dict = {'X': xyz[:, 0], 'Y': xyz[:, 1], 'Z': xyz[:, 2]}
    # pcd = pd.DataFrame(pcd_dict)
    # xyz = np.asarray(cl.points)
    # # print(xyz.shape)
    # pcd_dict = {'X': xyz[:, 0], 'Y': xyz[:, 1], 'Z': xyz[:, 2]}
    # pcd = pd.DataFrame(pcd_dict)
    return cl
    # return pcd2


def rotate_pcd(pcd, rot_grade, x_center, y_center):
    RD = math.radians(rot_grade)
    RMATRIX = np.matrix([[math.cos(RD), -math.sin(RD), 0],
                         [math.sin(RD), math.cos(RD), 0],
                         [0, 0, 1]])
    pcd['X'] += x_center
    pcd['Y'] += y_center
    pcd[['X', 'Y', 'Z']] = RMATRIX.dot(pcd[['X', 'Y', 'Z']].T).T
    return pcd


def get_o3d_pcd(pcd):
    xyz = np.zeros((len(pcd['X']), 3))
    xyz[:, 0] = pcd['X']
    xyz[:, 1] = pcd['Y']
    xyz[:, 2] = pcd['Z']

    o3d_pcd = o3d.geometry.PointCloud()
    o3d_pcd.points = o3d.utility.Vector3dVector(xyz)
    return o3d_pcd


def get_o3d_pcd_rgb(pcd):
    xyz = np.zeros((len(pcd['X']), 3))
    xyz_colors = np.zeros((len(pcd['X']), 3))
    xyz[:, 0] = pcd['X']
    xyz[:, 1] = pcd['Y']
    xyz[:, 2] = pcd['Z']
    xyz_colors[:, 0] = pcd['r']
    xyz_colors[:, 1] = pcd['g']
    xyz_colors[:, 2] = pcd['b']

    o3d_pcd = o3d.geometry.PointCloud()
    o3d_pcd.points = o3d.utility.Vector3dVector(xyz)
    o3d_pcd.colors = o3d.utility.Vector3dVector(xyz_colors)
    return o3d_pcd


def read_pcd(dir, y_limit, z_limit):
    pcd = pd.read_csv(dir)
    pcd = pcd.rename(
        columns={'X': 'Z', 'Z': 'X'})
    pcd['X'] *= -1
    pcd = pcd[(pcd.Y >= y_limit[0])]  # 5
    pcd = pcd[(pcd.Y <= y_limit[1])]  # 5
    pcd = pcd[(pcd.Z >= z_limit[0])]  # 5
    pcd = pcd[(pcd.Z <= z_limit[1])]  # 5'

    return pcd
