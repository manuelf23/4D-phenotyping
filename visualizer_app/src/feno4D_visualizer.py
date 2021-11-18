import glob
import json
import re
import numpy as np
from PcdModel import PcdModel
from lidar_utils import read_pcd
import pandas as pd

from tqdm import tqdm


from custom_3d_plot import custom_draw_geometry
from custom_exceptions import EmptyMultispectralDataError

def natural_keys(text):
    def atoi(text):
        return int(text) if text.isdigit() else text
    return [atoi(c) for c in re.split('(\d+)', text)]


def visualizer(folder_path, key_point_calibration_path, geometric_calibration_path,
               y_limit, z_limit, divisor, data_step_angle):

    # Divisores con 6: [6, 12, 18, 24, 30, 36, 60, 72, 90, 120, 180, 360]
    # Divisores con 12: [12, 24, 36, 60, 72, 120, 180, 360]
    # Divisores con 24: [24, 36, 60, 72, 120, 180, 360]
    try:
        try:
            with open(geometric_calibration_path, 'r') as openfile:
                # Reading from json file
                json_object = json.load(openfile)
            R = np.matrix(json_object["R"])
            x_center = json_object["x_center"]
            y_center = json_object["y_center"]

        except json.decoder.JSONDecodeError:
            message = "Geometric calibration file must be a JSON file"
            print(message)
            return (-2, message)
        except KeyError:
            message = "Geometric calibration file with bad format"
            print(message)
            return (-3, message)
        key_point_calibration = key_point_calibration_path
        files = glob.glob(folder_path + '*.csv')
        if len(files) == 0:
            message = "PCD and images Folder does not have .csv files"
            print(message)
            return (-4, message)
        files.sort(key=natural_keys)
        f_flag = True

        for fname in tqdm(files, colour='green'):
            try:
                rot = int(fname.split('/')[-1].split('.')[0])
            except ValueError:
                message =  "csv files in pcd data have invalid names or format"
                print(message)
                return (-5, message)
            if (rot + data_step_angle) % divisor:
                continue
            print(rot + data_step_angle, divisor)
            img_name = folder_path + str(rot) + '/'
            pcd_frame = read_pcd(fname, y_limit, z_limit)
            try:
                if f_flag:
                    f_flag = False
                    my_pcd = PcdModel(pcd_frame, x_center=x_center,
                                    y_center=y_center, rotation_plane_mtx=R, rot_ini=rot, path_to_3d_2d_keypoints=key_point_calibration, method='linear', path_rgb_fusion_img=img_name)
                else:
                    my_pcd.add_pcd(pcd_frame, rot, path_rgb_fusion_img=img_name)
            except pd.errors.ParserError:
                message =  "Error in 4D calibration file"
                print(message)
                return (-1, message)

        if not f_flag:
            print("NDVI mean: ", my_pcd.get_ndvi_mean())
            # print("NDRE mean: ", my_pcd.get_ndre_mean())
            custom_draw_geometry(
                my_pcd.get_o3d_pcd_rgb(), my_pcd.get_pcd_model())
    except EmptyMultispectralDataError:
        message = "There is not multispectral pcd data in .pickle format"
        print(message)
        return (-6, message)

    except Exception as e:
        message= "Unknown error"
        print(message)
        print(e)
        return (0, message)
