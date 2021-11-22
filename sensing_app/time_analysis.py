# coding=utf-8
import os
jetson_venv_dir = '/home/ubuntu/feno4d_venv/lib/python3.8/site-packages'
if os.path.isdir(jetson_venv_dir):
    os.sys.path.append(jetson_venv_dir)
    os.sys.path.append('')

from read_frames_lidar import save_lidar_csv_file
from take_parrot import take_photos_parrot

from datetime import datetime
import argparse
from ardu_motor import Turntable
import time
from configure_lidar import *

parser = argparse.ArgumentParser()
parser.add_argument("interface", help="Interfaz de la red a la cua está conectado el LiDAR", type=str)
parser.add_argument("min", help="Minutes between samplrs", type=int)
args = parser.parse_args()

now = datetime.now()
dt_string = f'timeA--{now.strftime("%d-%m-%Y--%H-%M-%S")}'
base_path = './' + dt_string

num_psckets = 10
# net_interface = 'en6'
net_interface = args.interface
wmin = args.min


try:
    os.mkdir(base_path)
except OSError:
    print ("Creation of the directory %s failed" % base_path)
else:
    print ("Successfully created the directory %s " % base_path)



init = time.time()
frame_num = 0
first_flag = True
while(1):
    
    first_flag = False
    datet = str(time.time()).split('.')[0]
    fileName = f'{base_path}/{datet}_{frame_num}'
    r = 0
    print(f'\t\tInicio captura de Datos en frame: {frame_num}\n')
    print(f'\tINICIO CAPTURA PARROT')
    while not r:
        r = take_photos_parrot(fileName)
    print('\tPARROT frames saved (yes)\n')
    
    r = 0
    print(f'\tINICIO CAPTURA LIDAR')
    frame_num += 1
    while not r:
        r = save_lidar_csv_file(fileName, num_psckets, net_interface)
    print(f'\FIN CAPTURA LIDAR')

    print('For the next sample please wait {wmin} minutes')
    time.sleep(60*wmin)

print('TOMA DE DATOS FINALIZADA')
