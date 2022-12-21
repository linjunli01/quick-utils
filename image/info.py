from PIL import Image
import cv2
import sys
import os

image_path = '/image/path'
image_file = 'test.png'
argv = sys.argv
if len(argv) > 1:
    for cmd in argv:
        if cmd.startswith('--file='):
            file = cmd.split('=', 1)[1]
            if file:
                if os.path.exists(os.path.join(image_path, file)):
                    image_file = file
                else:
                    print(f'wrong file{file}')

print(f'read image:{image_file}')
data = cv2.imread(os.path.join(image_path, image_file))
print('image info:')
print(f'min:{data.min()}')
print(f'max:{data.max()}')
print(f'shape:{data.shape}')
print(f'dtype:{data.dtype}')
print(f'size:{data.size/1048576} MB')