import os
import re

mask = re.compile("/(\w+)/res/(\d+).html")

def accepted_files(folder):
    raw = os.listdir(folder)
    accepted = 'jpg', 'jpeg', 'png', 'gif', 'webm'
    for filename in raw[:]:
        if not any(filename.lower().endswith('.' + ext) for ext in accepted):
            raw.remove(filename)
    return raw
    
def basic_data(threadlink):
    board, thread = mask.findall(threadlink)[0]
    data = {'task': 'post', 'board': board, 'thread': thread}
    return data