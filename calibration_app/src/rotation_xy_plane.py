import pyransac3d as pyrsc
import numpy as np
import pandas as pd
import open3d as o3d
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import glob
from copy import deepcopy
import json
import math
import os

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


def rotate_pcd(pcd, rot_grade):
        RD = math.radians(rot_grade)
        RMATRIX = np.matrix([[math.cos(RD), -math.sin(RD), 0],
                         [math.sin(RD), math.cos(RD), 0],
                         [0, 0, 1]])
        x=0.063
        y=-0.972
        pcd['X'] += x
        pcd['Y'] += y
        pcd[['X', 'Y', 'Z']] = RMATRIX.dot(pcd[['X', 'Y', 'Z']].T).T
        return pcd

def filter_and_promediate_pcd(pcd, nb_neighbors, std_ratio):

    pcd = pcd.groupby(['azimuth', 'laser_id']).mean()
    pcd = pcd.reset_index()
    xyz = np.zeros((len(pcd['X']), 3))
    xyz[:, 0] = pcd['X']
    xyz[:, 1] = pcd['Y']
    xyz[:, 2] = pcd['Z']

    o3d_pcd = o3d.geometry.PointCloud()
    o3d_pcd.points = o3d.utility.Vector3dVector(xyz)
    cl, ind = o3d_pcd.remove_statistical_outlier(
        nb_neighbors=nb_neighbors, std_ratio=std_ratio)
    return cl


def plane_calibration(folder_path, save_folder_path, y_limit, z_limit):
    
    files = glob.glob(folder_path + '*.csv')
    for i, fname in enumerate(files):
        if i:
            pcd_frame = pd.concat(
                [pcd_frame, read_pcd(fname, y_limit, z_limit)])
        else:
            pcd_frame = read_pcd(fname, y_limit, z_limit)
    while True:
        cl = filter_and_promediate_pcd(
            pcd_frame, nb_neighbors=15, std_ratio=0.1)
        xyz_numpy = np.asarray(cl.points)
        plane1 = pyrsc.Plane()
        best_eq, best_inliers = plane1.fit(
            xyz_numpy, thresh=0.01, minPoints=10000, maxIteration=1000)

        a = best_eq[0]
        b = best_eq[1]
        c = best_eq[2]
        v = np.array([a, b, c])
        norm_V = np.linalg.norm(v)

        v2 = np.array([a, b])
        norm_V2 = np.linalg.norm(v2)

        cos = c / norm_V
        u1 = b / norm_V2
        u2 = - a / norm_V2
        sin = ((a**2 + b**2) / (a ** 2 + b ** 2 + c ** 2)) ** 0.5

        ucos = 1 - cos
        u1u2 = u1 * u2

        green = [0, 0.706, 0]
        blue = [0, 0, 0.929]
        red = [1, 0, 0]

        cl1 = deepcopy(cl.paint_uniform_color(red))
        pcds = [cl1]

        R = np.matrix([[cos + (u1**2 * ucos), u1u2 * ucos, u2 * sin, 0],
                       [u1u2 * ucos, cos + (u2 ** 2 * ucos), -u1 * sin, 0],
                       [-u2 * sin, u1 * sin, cos, 0],
                       [0, 0, 0, 1]])

        cl_pre = np.sign(np.asarray(cl.points)[0])
        cl.transform(R)
        pcds.append(cl.paint_uniform_color(green))
        cl_post = np.sign(np.asarray(cl.points)[0])

        if all(cl_pre == cl_post):
            break
    print("best_eq:", best_eq)
    
    R_save = np.delete(R, -1, axis=1)
    R_save = np.delete(R_save, -1, axis=0)
    print("R:", R_save)
    pcds.append(o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.2))
    o3d.visualization.draw_geometries(pcds)

    dictionary = {
        "R": R_save.tolist()
    }

    
  
    # Writing to sample.json
    save_path_file = f"{save_folder_path}/geometric_calibration.json"
    if os.path.isfile(save_path_file):
        with open(save_path_file, "r+") as outfile:
            js_data = json.load(outfile) 
            js_data["R"] = dictionary["R"]
            json_object = json.dumps(js_data, indent = 4)
            outfile.seek(0)
            outfile.write(json_object)
            outfile.truncate()
    else:
        json_object = json.dumps(dictionary, indent = 4)
        with open(save_path_file, "w") as outfile:
            outfile.write(json_object)

if __name__ == "__main__":
    y_limit = (0.7, 1.2)
    z_limit = (-0.5, 1.8)
    folder_path = "/Users/manuelgarciarincon/Downloads/nueva_calibracion/calibracion_plano/"
    save_folder_path = "/Users/manuelgarciarincon/Downloads/nueva_calibracion"
    plane_calibration(folder_path, save_folder_path, y_limit, z_limit)
