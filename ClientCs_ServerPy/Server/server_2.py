import socket
import os
import io
import os.path
import matplotlib.pyplot as plt
import matplotlib as mpl
from os import listdir
from os.path import isfile, join
import cv2

import threading, time
from msvcrt import getch

import sys
sys.path.append('..\\GazePlot')
from index2 import *

current_path = sys.path[0]
base_path = str(current_path.replace('\Server', '\\'))

path_imgs = base_path+str('imgs')
path_csvs  =  base_path+str('csvs')
save_path =  base_path+str('gaze_analysis')

file = None
can = True

'''
    TCP CONNECTION
'''
s = socket.socket()
host = socket.gethostbyname('localhost')
port = 12345
s.bind((host, port))
s.listen(1)
print("Waiting for a connection...")
c, addr = s.accept()
print("Connection from: " + str(addr))


'''
    SLIDER
'''
mpl.rcParams['toolbar'] = 'None'
name_imgs = [f for f in listdir(path_imgs) if isfile(join(path_imgs, f))]

print(name_imgs)
print([join(path_imgs,f) for f in name_imgs])

images = [cv2.imread(join(path_imgs,f)) for f in name_imgs]
curr_pos = 0
fig = plt.figure()
ax = fig.add_subplot(111)
ax.axis('off')
plt.tight_layout() 
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

for file in os.listdir(path_csvs):
    if os.path.isfile(join(path_csvs,file)):
        os.remove(join(path_csvs,file))
               

plt.imshow(images[curr_pos])
figManager = plt.get_current_fig_manager() 
figManager.full_screen_toggle()


file = open(join(path_csvs,'PHOTO_' + '0' + str(curr_pos) + '.csv'), 'a')
file.write('PHOTO_' + '0' + str(curr_pos) + ',-,-,-\n')

def save_on_file():
    global c
    global file
    global can 

    print("in save_on_file")
    flag = True    
    while flag:
        try:
            data = c.recv(1024)
            # print(data)
            # app += data.decode("utf-8")
            if str(data) == "b''":
                raise Exception('Exception')
            if can:
                file.write(str(data.decode("utf-8")) + '\n')
                print('wif: '+str(data.decode("utf-8")))
        except: 
            print("Exeption")
            flag = False
            break
    print("Done save_on_file")


def key_event_2(e):
    global curr_pos    
    global file
    global can
    can = False
    # old_pos = curr_pos
    
    if e.key == "right":
        curr_pos = curr_pos + 1

    elif e.key == "left":
        curr_pos = curr_pos - 1

    elif e.key == 'enter':
        plt.close()
        file.write('END_,-,-,-\n') # +str(old_pos)+'\n')
        return

    else:
        can = True
        return

    curr_pos = curr_pos % len(images)
    file.write('END_,-,-,-\n') # +str(old_pos)+'\n')
    file.close()
    file = open(join(path_csvs, 'PHOTO_'+ (str(curr_pos) if curr_pos > 9 else '0'+str(curr_pos)) +'.csv'), 'a')
    file.write('PHOTO_'+ (str(curr_pos) if curr_pos > 9 else '0'+str(curr_pos)) +',-,-,-\n')
    plt.cla()
    plt.axis('off')
    plt.imshow(images[curr_pos])
    plt.draw()
    can = True

threading.Thread(target = save_on_file).start()

fig.canvas.mpl_connect('key_press_event', key_event_2)
fig.show()
plt.show()

print("Done.")

file.close()
c.close()
s.close()

for file_name in os.listdir(path_csvs):
    photo_name = file_name.split('.')[0]+'.png'
    create_fixation_file(path_csvs + '\\' + file_name, path_imgs + '\\' + photo_name, save_path + '\\')