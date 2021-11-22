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
parser.add_argument("turntable_step_grade", help="Ingrese los  pasos en grados [6, 12, 18, 24, 30, 36, 60, 72, 90, 120, 180, 360]", type=int)

args = parser.parse_args()

now = datetime.now()
dt_string = now.strftime("%d-%m-%Y--%H-%M-%S")
dt_string += '--' + str(args.turntable_step_grade)
base_path = './' + dt_string

num_psckets = 10
# net_interface = 'en6'
net_interface = args.interface


angle = args.turntable_step_grade
step_number_per_revolution = int(360/angle)

# print('Inicio configuracion LiDAR')
# Base_URL = 'http://192.168.1.201/cgi/'
# s = reset_lidar_config(Base_URL)
# if not s:
#     raise Exception('LiDAR no detected')
# s = turn_on_off_lidar_laser(Base_URL, 'on')
# if not s:
#     raise Exception('LiDAR no detected')
# s = set_lidar_fov(Base_URL, start=270, end=90)
# if not s:
#     raise Exception('LiDAR no detected')

# print('LiDAR configurado correctamente')

try:
    os.mkdir(base_path)
except OSError:
    print ("Creation of the directory %s failed" % base_path)
else:
    print ("Successfully created the directory %s " % base_path)

my_turntable = Turntable()

for step in range(step_number_per_revolution):
    print('TOMA DE DATOS EN', step*angle, 'GRADOS')
    fileName = base_path + '/' + str(step*angle)
    r = 0
    print('\tINICIO CAPTURA LIDAR')
    while not r:
        r = save_lidar_csv_file(fileName, num_psckets, net_interface)
    print('\tLiDAR frames saved (yes)\n')
    my_turntable.turn()
    # time.sleep(20) # tiempo de estabilización de la planta para que se deje de mover

print('TOMA DE DATA FINALIZADA')
