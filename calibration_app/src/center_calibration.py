import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import open3d as o3d
from matplotlib.widgets import Cursor
import json
import matplotlib.cm
import os


def filter_and_promediate_pcd(pcd, nb_neighbors=5, std_ratio=0.9):

    # pcd = pcd.groupby(['azimuth', 'laser_id']).mean()
    pcd = pcd.reset_index()
    xyz = np.zeros((len(pcd['X']), 3))
    xyz[:, 0] = pcd['X']
    xyz[:, 1] = pcd['Y']
    xyz[:, 2] = pcd['Z']

    o3d_pcd = o3d.geometry.PointCloud()
    o3d_pcd.points = o3d.utility.Vector3dVector(xyz)
    cl, ind = o3d_pcd.remove_statistical_outlier(
        nb_neighbors=nb_neighbors, std_ratio=std_ratio)
    new_pcd = pd.DataFrame(columns=['X','Y','Z'])
    cl_points = np.asarray(cl.points)
    new_pcd['X'] = cl_points[:, 0]
    new_pcd['Y'] = cl_points[:, 1]
    new_pcd['Z'] = cl_points[:, 2]
    return new_pcd

def rotacion_xy(pd_X, pd_y, pd_Z, R):
    xyz2 = np.zeros((len(pd_X), 3))
    xyz2[:, 0] = pd_X
    xyz2[:, 1] = pd_y
    xyz2[:, 2] = pd_Z
    R = np.matrix([[0.99948284,  0.00112413, - 0.03213697],
                   [0.00112413,  0.99755653,  0.06985494],
                   [0.03213697, - 0.06985494,  0.99703937]])
    a_rotados = []
    b_rotados = []
    c_rotados = []
    for punto in xyz2:
        punto_rotado = ((R*np.asmatrix(punto).T).T)

        a_rotados.append(punto_rotado[0, 0])
        b_rotados.append(punto_rotado[0, 1])
        c_rotados.append(punto_rotado[0, 2])

    return a_rotados, b_rotados, c_rotados


def find_center(center_pcd_path, save_folder_path, show_graph, y_limit=(0.7, 1.2), z_limit=(-0.55, 1.8)):
    pcd_frame = pd.read_csv(center_pcd_path)
    pcd_frame = pcd_frame.drop(
        columns=['Points_m_XYZ:0',
                    'Points_m_XYZ:1',
                    'Points_m_XYZ:2',
                    'azimuth',
                    'distance_m',
                    'adjustedtime',
                    'timestamp',])
    pcd_frame = pcd_frame.rename(
        columns={'X': 'Z', 'Z': 'X'})

    calib_file = f"{save_folder_path}/geometric_calibration.json"
    with open(calib_file, "r+") as outfile:
        js_data = json.load(outfile)
        R = js_data["R"]

    pcd_frame['X'], pcd_frame['Y'], pcd_frame['Z'] = rotacion_xy(
        pcd_frame['X'], pcd_frame['Y'], pcd_frame['Z'], R)


    ################# FILTER PCD POINTS BY DISTANCE #################
    pcd_frame = pcd_frame[(pcd_frame.Y >= y_limit[0])]  # 5
    pcd_frame = pcd_frame[(pcd_frame.Y <= y_limit[1])]  # 5
    pcd_frame = pcd_frame[(pcd_frame.Z >= z_limit[0])]  # 5
    pcd_frame = pcd_frame[(pcd_frame.Z <= z_limit[1])]  # 5'
    
    # pcd_frame = pcd_frame[(pcd_frame.Z >= -0.173)]  # 5'
    ################# FILTER PCD POINTS BY DISTANCE #################
    laser_filter=pcd_frame['laser_id'][pcd_frame['Z'].idxmax()]

    ################# FILTER PCD POINTS BY LASER_ID #################
    centro_pcd = pcd_frame[(pcd_frame.laser_id == laser_filter)]  # 5
    ################# FILTER PCD POINTS BY LASER_ID #################
    list_idx= (centro_pcd.Z >= -0.48)
    target_pcd = centro_pcd[list_idx]  # 5'
    target_pcd = filter_and_promediate_pcd(target_pcd)

    print('centro X:', target_pcd['X'].mean())
    print('centro Y:', target_pcd['Y'].mean())
    dictionary = {
        "x_center": target_pcd['X'].mean(),
        "y_center": target_pcd['Y'].mean()
        }
    # Writing to sample.json
    save_path_file = f"{save_folder_path}/geometric_calibration.json"
    if os.path.isfile(save_path_file):
        with open(save_path_file, "r+") as outfile:
            js_data = json.load(outfile) 
            js_data["x_center"] = dictionary["x_center"]
            js_data["y_center"] = dictionary["y_center"]
            json_object = json.dumps(js_data, indent = 4)
            outfile.seek(0)
            outfile.write(json_object)
            outfile.truncate()
    else:
        json_object = json.dumps(dictionary, indent = 4)
        with open(save_path_file, "w") as outfile:
            outfile.write(json_object)
    # print(target_pcd)

    ax = plt.axes(projection='3d')

    ax.scatter(pcd_frame['X'], pcd_frame['Y'], pcd_frame['Z'], linewidth=0.01)
    ax.scatter(centro_pcd['X'], centro_pcd['Y'], centro_pcd['Z'], linewidth=2, color='red')
    ax.scatter(target_pcd['X'], target_pcd['Y'],
            target_pcd['Z'], linewidth=6, color='green')

    ax.set_xlabel('x [m]')
    ax.set_ylabel('y [m]')
    ax.set_zlabel('z [m]')

    cursor = Cursor(ax, useblit=True, color='red', linewidth=2)
    if show_graph:
        plt.show()
