# coding=utf-8
import requests
import json
import time
import shutil
import os.path


def take_photos_parrot(fname, sequoia_ip = '192.168.47.1'):
    r = requests.get('http://' + sequoia_ip + '/capture/start')
    # print(json.dumps(r.json(), indent = 4))
    time.sleep(5)
    r = requests.get('http://' + sequoia_ip + '/capture')
    print(r.json()['status'])
    if r.json()['status'] == 'Ready':
        print('CAPTURA EXITOSA')
        r = requests.get('http://' + sequoia_ip + '/file/internal')
        r_json = r.json()
        last_ph_folder = list(r_json.keys())[-1]
        if r_json[last_ph_folder] == 5:
            r = requests.get('http://' + sequoia_ip + '/download/' + last_ph_folder, stream=True)
            if r.status_code == 200:
                with open(fname + '.zip', 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                    return 1
            else:
                return 0
        else:
            return 0
    else:
        r = requests.get('http://' + sequoia_ip + '/capture/stop')
        print('CAPTURA FALLIDA')
        time.sleep(2)
        return 0

    

def main():
    take_photos_parrot('prueba')


if __name__ == '__main__':
    main()