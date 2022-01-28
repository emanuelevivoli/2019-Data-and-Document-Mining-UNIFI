#!/usr/bin/python

import socket
import os
import io
import os.path
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib as mpl
from os import listdir
from os.path import isfile, join

import threading, time
from msvcrt import getch

#def Main():

# CHANGE IT
path_ = 'C:/Users/emanuelevivoli/source/repos/ClientCs_ServerPy/ClientCs_ServerPy/Server/'
path_imgs = 'C:/Users/emanuelevivoli/source/repos/ClientCs_ServerPy/ClientCs_ServerPy/images'
file = None
# can = True

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
images = [mpimg.imread(join(path_imgs,f)) for f in listdir(path_imgs) if isfile(join(path_imgs, f))]
curr_pos = 0
fig = plt.figure()
ax = fig.add_subplot(111)
ax.axis('off')
plt.tight_layout() 
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)


if os.path.isfile(path_+'PHOTO_'+str(curr_pos)+'.csv'):
    os.remove(path_+'PHOTO_'+str(curr_pos)+'.csv')
               

plt.imshow(images[curr_pos])
figManager = plt.get_current_fig_manager() 
figManager.full_screen_toggle()


file = open(path_+'PHOTO_'+str(curr_pos)+'.csv', 'a')


def save_on_file():
    global c
    global file
    
    print("in save_on_file")
    flag = True    
    while flag:
        # if can:
        try:
            data = c.recv(1024)
            # app += data.decode("utf-8")
            if str(data) == "b''":
                raise Exception('Exception')
            file.write(str(data.decode("utf-8"))+'\n')
            print('write in file: '+str(data.decode("utf-8")))
        except: 
            print("Exeption")
            flag = False

def key_event():
    # global can
    # can = False
    global curr_pos
    global file
    global path_
    
    lock = threading.Lock()
    while True:
        with lock:
            key = getch()
            print(key)

            if key == "b'M'":
                print("right")
                curr_pos = curr_pos + 1
                
            #If left button pressed -> go to previous image
            elif key == "b'\xe0'":
                print("left")
                curr_pos = curr_pos - 1
            
            elif key == "b'\x1b'":
                print("esc")
                file.write("END \n")
                plt.close()

            else:
                # can = True
                return

            file.write("END \n")
            file.close()
            curr_pos = curr_pos % len(images)
            
            file = open(path_+'PHOTO_'+str(curr_pos)+'.csv', 'a')
            file.write("START \n")
            print('write in file: PHOTO_'+str(curr_pos))

            plt.cla()
            plt.axis('off')
            plt.imshow(images[curr_pos])
            plt.draw()
            # can = True

# file.write('PHOTO_'+str(curr_pos))

threading.Thread(target = save_on_file).start()
threading.Thread(target = key_event).start()

# fig.canvas.mpl_connect('key_press_event', key_event)
fig.show()
plt.show()

print("Done.")

file.close()
c.close()
s.close()



#if __name__ == "__main__":
#    Main()