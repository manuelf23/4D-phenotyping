# coding=utf-8
import subprocess
print(subprocess.__file__)
from textwrap import wrap
from convert_data import azimuth, interpolacion_azimuth,dataPoint, timeStamp, calc_xyz

def save_packets_lidar(fname, nPackets, interface):
    """[summary]

    Args:
        fname (string): File name for saving the packets without extension.
        nPackets (integer): Number of packets to be recived.
        interface (string): Network interface for reciving the packets.

    Returns:
        (integer):  Code 0: Packest were not saved correctly
                    Code 1: Packest were saved correctly
                    Code 2: The network interface does not exist
    """
    process = subprocess.Popen(['tcpdump', '-c', str(nPackets * 100), '-w' , fname + '.pcap', '-i', interface],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)

    stdout, stderr = process.communicate()
    process.terminate()
    # print(stderr)
    if '(No such device exists)' in str(stderr):
        return 2 # The network interface does not exist
    # print(str(stderr).split('\\n'))
    rPackets = int(str(stderr).split('\\n')[1].split(' ')[0])
    if rPackets == nPackets * 100:
        return 1 # Packest were saved correctly
    else:
        return 0 # Packest were not saved correctly



    LASER_ANGLES = [-15, 1, -13, 3, -11, 5, -9, 7, -7, 9, -5, 11, -3, 13, -1, 15]
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