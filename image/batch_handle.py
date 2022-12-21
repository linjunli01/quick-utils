from multiprocessing import Process, Value, Lock
import os,math,time
from framework.progressBar import ProgressBar
from PIL import Image
import numpy as np
from decimate import decimate

RESOURCE_PATH = '/image/path'
OUTPUT_PATH = '/image/path'
RESOURCE_IMAGES = []
PROCESS_NUM = 5

def transfer(l, num, lock):
    for file in l:
        with Image.open(os.path.join(RESOURCE_PATH, file)) as image:
            res = decimate(np.array(image))
            res_img = Image.fromarray(res)
            res_img.save(fp=os.path.join(OUTPUT_PATH, file), format='png')
            if lock.acquire():
                num.value += 1
                lock.release()

if __name__ == '__main__':
    print(f'traverse resource dir:{RESOURCE_PATH}')
    for dir_path, dir_name, file_names in os.walk(RESOURCE_PATH):
        for name in file_names:
            # if name.endswith('.png'):
            RESOURCE_IMAGES.append(name)
    print(f'get images total:{len(RESOURCE_IMAGES)}')
    print(f'output paht:{OUTPUT_PATH}')
    mode = math.ceil(len(RESOURCE_IMAGES) / PROCESS_NUM)
    SPLIT_IMAGES = [[] for i in range(PROCESS_NUM)]
    index = 0
    count = 0
    for i in RESOURCE_IMAGES:
        SPLIT_IMAGES[index].append(i)
        count += 1
        if count % mode == 0:
            index += 1
    bar = ProgressBar(f'process image:', len(RESOURCE_IMAGES))
    num = Value('i', 0)
    lock = Lock()
    count = 0
    print('start binning')
    start = time.time_ns()
    for l in SPLIT_IMAGES:
        Process(target=transfer, args=[l, num, lock]).start()
    while count < num.value or count < len(RESOURCE_IMAGES):
        if count < num.value:
            count = num.value
            bar.update()
    if num.value >= len(RESOURCE_IMAGES):
        while bar.count < len(RESOURCE_IMAGES):
            bar.update()
        time.sleep(0.5)
        print(f'spent time: {(time.time_ns() - start) / 1000000000} s')
        print('finished')