import numpy as np
import cv2
import glob
import pandas as pd
import os
import sys
from pcd_3d_keypoin_extraction import get_3d_points_plane
from extract_2d_points_auto import get_board_corners
file_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(f"{file_path}/../../visualizer_app/src")
from ImgAnalyze import ImgAnalyze

key_p = {'HC': [], 'frame': [], 'u': [], 'v': [], 'x': [], 'y': [], 'z': []}
f_num = 0

def sort_array(points):
    p1 = [-1, -1]
    for i, point in enumerate(points):
        if i == 0:
            if point[1] > p1[1]:
                p1 = point
        else:
            if point[1] < p1[1]:
                p1 = point

    p2 = [-1, -1]
    for i, point in enumerate(points):
        if point[0] > p2[0]:
            p2 = point

    p3 = [-1, -1]
    for i, point in enumerate(points):
        if point[1] > p3[1]:
            p3 = point
            
    p4 = [-1, -1]
    for i, point in enumerate(points):
        if i == 0:
            if point[0] > p4[0]:
                p4 = point
        else:
            if point[0] < p4[0]:
                p4 = point
    return [p1, p2, p3, p4]




def sensory_fision_caloibration(f_path, s_f_path, calib_path_rgb, auto=False):
    global key_p, f_num

    def draw(event, x, y, flags, params):
        global key_p, f_num
        # Left Mouse Button Down Pressed
        if(event == 1):
            if len(key_p) < 400:
                key_p['frame'].append(f_num)
                key_p['HC'].append(1)
                key_p['u'].append(x-1)
                key_p['v'].append(y-2)
                cv2.circle(image_gray_color, (x-1, y-2), radius=0,
                        color=(0, 0, 255), thickness=5)
    
    folders = glob.glob(f'{f_path}/*/')
    folders.sort()
    
    ImgAnalyze.generate_RGB_image(calib_path_rgb, f_path)
    for ffolder in folders:
        f_num = ffolder.split('/')[-2]
        img_path = glob.glob(f'{ffolder}/*RGB.jpg')
        if not auto:
            
            
            image = cv2.imread(img_path[0], 0)
            image_gray_color = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            cv2.namedWindow(f_num)
            cv2.setMouseCallback(f_num, draw)
            while(True):
                cv2.imshow(f_num, image_gray_color)
                if cv2.waitKey(20) & 0xFF == ord('q'):
                    break
            cv2.destroyAllWindows()
        else:
            points_2d = get_board_corners(img_path[0])
            points_2d = sort_array(points_2d)
            for point in points_2d:
                key_p['frame'].append(f_num)
                key_p['HC'].append(1)
                key_p['u'].append(point[0])
                key_p['v'].append(point[1])
        xg, yg, zg = get_3d_points_plane(ffolder[:-1] + '.csv')
        key_p['x'] += xg
        key_p['y'] += yg
        key_p['z'] += zg
        
    pd.DataFrame(key_p).to_csv(
        f'{s_f_path}/sensory_fusion_calibration.csv', index=False)

if __name__ == "__main__";
    folder_path = "/Users/manuelgarciarincon/Desktop/nueva_calibracion/fusion_cured"
    folder_path = "/Users/manuelgarciarincon/Desktop/calibracion_6_mayo/fusion_cured"
    folder_path = "/Users/manuelgarciarincon/4D-phenotyping/data/guaiacum_officinale/calibration_data/calibration_data/sensory_fusion_automatic"
    calib = "/Users/manuelgarciarincon/4D-phenotyping/data/guaiacum_officinale/calibration_data/calibrations_results/multispectral_image_registration"

    sensory_fision_caloibration(folder_path, folder_path, calib, auto=True)