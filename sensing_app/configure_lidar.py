# base_URL = 'http://192.168.1.201/cgi/'
import requests

def reset_lidar_config(base_URL):
    url = base_URL + 'reset'
    params = {'data': 'reset_system'}
    rcode = requests.post(url, data=params)
    success = rcode in range(200, 207)
    if success:
        print("Configuraciones del LiDAR Re-establecias, esperar 10s")
        time.time(10)
        return success, rcode
    else:
        return success, rcode
    

def turn_on_off_lidar_laser(base_URL, state):
    if state != 'on' or state != 'off':
        raise TypeError('state different of on or off')
    url = base_URL + 'setting'
    params = {'laser': state}
    rcode = requests.post(url, data=params)
    success = rcode in range(200, 207)
    if success:
        time.time(1)
        return success, rcode
    else:
        return success, rcode


def set_lidar_rpm(base_URL, rpm):
    if rpm not in range(0, 600):
        raise ValueError('rpm out of range (0-600)')
    url = base_URL + 'setting'
    params = {'rpm': str(rpm)}
    rcode = requests.post(url, data=params)
    success = rcode in range(200, 207)
    if success:
        time.time(1)
        return success, rcode
    else:
        return success, rcode


def set_lidar_fov(base_URL, start=0, end=359):
    if start not in range(0, 359) or end not in range(0, 359):
        raise ValueError('start or range out of range (0-359)')
    if start == end:
        raise ValueError('start and range can not have the same value)')
    url = base_URL + 'setting/fov'
    params = {'start': str(start), 'end':str(end)}
    rcode = requests.post(url, data=params)
    success = rcode in range(200, 207)
    if success:
        time.time(1)
        return success, rcode
    else:
        return success, rcode
