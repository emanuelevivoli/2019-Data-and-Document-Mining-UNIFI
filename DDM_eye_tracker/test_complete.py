import sys
import time
import matplotlib.pyplot as plt

input = sys.stdin.readline()
app = str(input)
print(app)
sys.stdout.flush()

import matplotlib.image as mpimg
import matplotlib as mpl
from os import listdir
from os.path import isfile, join


mpl.rcParams['toolbar'] = 'None'

# Get images and inizialize list images
name_imgs = [f for f in listdir('./images') if isfile(join('./images', f))]
images = [mpimg.imread('./images/'+f) for f in listdir('./images') if isfile(join('./images', f))]

#Start real code
curr_pos = 0
fig = plt.figure()
ax = fig.add_subplot(111)
ax.axis('off')
plt.tight_layout()
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

print(name_imgs[curr_pos])
sys.stdout.flush()
plt.imshow(images[curr_pos])
figManager = plt.get_current_fig_manager() 
figManager.full_screen_toggle()


def key_event(e):
    global curr_pos
    #If right button pressed -> go to next image
    if e.key == "right":
        curr_pos = curr_pos + 1
    #If left button pressed -> go to previous image
    elif e.key == "left":
        curr_pos = curr_pos - 1
    elif e.key == 'enter':
        print("END")
        sys.stdout.flush()
        plt.close()
    else:
        return
    curr_pos = curr_pos % len(images)

    plt.cla()
    plt.axis('off')
    print(name_imgs[curr_pos])
    sys.stdout.flush()
    plt.imshow(images[curr_pos])
    plt.draw()



#fig.axes('off')
#fig = plt.figure()
fig.canvas.mpl_connect('key_press_event', key_event)
fig.show()
#ax = fig.add_subplot(111)

plt.show()