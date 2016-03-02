# coding: utf8

import os
import sys
import time
import random

import requests
requests = requests.Session()

import funcs

NUMBER = 4
PAUSE = 20

_, thread, folder = sys.argv
all = funcs.accepted_files(folder)

while len(all) >= NUMBER:
    files = {}
    for i in range(NUMBER):
        filename = random.choice(all)
        all.remove(filename)
        path = os.path.join(folder, filename)
        files['image{}'.format(i + 1)] = open(path, 'rb').read()
    response = requests.post('https://2ch.hk/makaba/posting.fcgi', 
                            data=funcs.basic_data(thread),  
                            files=files
                            )
    print (response.status_code)
    time.sleep(PAUSE)
