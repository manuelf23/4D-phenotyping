# coding=utf-8
from scapy.all import *
from textwrap import wrap
from convert_data import azimuth, interpolacion_azimuth,dataPoint, timeStamp, calc_xyz
from spackets import save_packets_lidar
import csv


# LASER_ANGLES = [-15, 1, -13, 3, -11, 5, -9, 7, -7, 9, -5, 11, -3, 13, -1, 15]

azimuth_array = []
dataP_array = []
dataPFire_array = []
xyzP_array = []
xyzPFire_array = []

header_index = [0, 42]
dataLen = 100


def method_filter_HTTP(pkt):
    # LASER_ANGLES = [-15, 1, -13, 3, -11, 5, -9, 7, -7, 9, -5, 11, -3, 13, -1, 15]
    azimuth_array = []
    dataP_array = []
    dataPFire_array = []
    xyzP_array = []
    xyzPFire_array = []
    a=bytes(pkt)
    hexarray=a.hex().split('ffee')
    if len(hexarray) == 13:
       
        hexarray.pop(0)
    
        for n in range(12):
            data_block = wrap(hexarray[n], 2) #cada data_block tiene 98 bytes en este punto, porque en el split se quitaron los 2 bytes de la bandera FFEE, los siguientes 2 bytes son de azimuth
            az = azimuth(data_block[0:2])
            azimuth_array.append(az)
            
            if n:
                azp = interpolacion_azimuth(azimuth_array[len(azimuth_array) - 2], az)
                azimuth_array.insert(len(azimuth_array) - 1, azp)
            if n == 11:
                azimuth_array.append(az)
        for n in range(12):
            data_block = wrap(hexarray[n], 2)[2:]
 
            for x in range(2):
                xloop= x + 1
                dataPFire_array.clear()
                xyzPFire_array.clear()
                for laser_id in range(16):
      
                    ini = 3*(laser_id + (16*x))
                    fin = 3*(laser_id + 1 + (16*x))

                    
                    dataP = dataPoint(data_block[ini:fin])
                        
                    dataPFire_array.append(dataP[0])

                    azimuth_value = azimuth_array[(n*2)+x] + laser_id

                    val = calc_xyz(dataP[0], azimuth_value, laser_id)
                    if val[0]+val[1]+val[2] != 0:
                        xyzPFire_array.append(calc_xyz(dataP[0], azimuth_value, laser_id))
                        writer.writerow({'X':val[0], 'Y':val[1], 'Z':val[2], 'azimuth':azimuth_value, 'laser_id':laser_id})
 
                dataP_array.append(dataPFire_array)
                xyzP_array.append(xyzPFire_array)

            
def save_lidar_csv_file(fname, nPackets, interface): 
    
    status = save_packets_lidar(fname, nPackets, interface)
    # status = 1
    if status == 1:
        try:
            with open(fname + '.csv', mode='w') as lidar_frames:
                global writer
                fieldnames = ["X", "Y", "Z", "azimuth", "laser_id"]
                writer = csv.DictWriter(lidar_frames, fieldnames=fieldnames)
                writer.writeheader()
                sniff(offline= fname+".pcap",prn=method_filter_HTTP,store=0)
                return 1
        except Exception as e:
            print('Error read_frames_lidar:', e)
            return 0
        
    else:
        return 0
