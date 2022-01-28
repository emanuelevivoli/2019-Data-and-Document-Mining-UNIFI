import csv
import gazeplotter
from gazeplotter import *
from cc_finder import *
from match_rect_fixs import *
import time
from PIL import Image
import os
import codecs, json 

def create_fixation_file(photo_csv_file, photo_file, save_path):
    photo_name = photo_file.split('\\')[-1].split('.')[0]
    path_imgs = photo_file.replace(photo_file.split('\\')[-1], '')
    print(photo_name)

    with open(photo_csv_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        fixations = []
        for row in csv_reader:
            print(row)
            if len(row) == 4:
                type_, x, y, t = row
                if type_ == photo_file.split('\\')[-1].split('.')[0]:
                    fix = []
                elif type_ == "FS":
                    if len(fix) == 0:
                        fix.append([x, y, 0])
                elif type_ == "DF":
                    if len(fix) == 0:
                        fix.append([x,y,0])
                    # do nothing or:
                    # fix[0][2] = fix[0][2] + 1
                elif type_ == "FE":
                    if len(fix) == 1 and x != 'NaN':
                        fix.append([x, y, None])
                elif type_ == "TIME":
                    if len(fix) == 2:
                        fix.append([x, y, t])
                        fixations.append(fix)
                        fix = []
                elif type_ == "END_":
                    #finalize_photo(fix, fixations)
                    #se non ho trovato FE prima di trovare END, forse si puo' evitare questo controllo.. ?! 
                    if len(fix) == 1:
                        fix = []

    photo_0 = {	'x'  :numpy.asarray([ int((float(x[0][0]) + float(x[1][0]))/2) for x in fixations]),
                'y'  :numpy.asarray([ int((float(x[0][1]) + float(x[1][1]))/2) for x in fixations]),
                'dur':numpy.asarray([ float(x[2][2].split(":")[-1])*1500 for x in fixations ])}
    print('.................')
    # print(photo_0)
    im = Image.open(photo_file)
    width, height = im.size
    print(width, height)
    
    '''
        WE NEED TO SEPARATE THE FOLLOWING PARTS IN:
        - def save_fix-heat_maps()
        - def copy_original()
        - def save_rects()
        - def save_fixs()
    '''

    # save_fix-heat_maps
    fig = draw_fixations_new(photo_0, (width, height), imagefile = photo_file, durationsize=True, durationcolour=True, alpha=1, savefilename=save_path+photo_name+'_fixs.png')
    heatmap = draw_heatmap_new(photo_0, (width, height), imagefile = photo_file, durationweight=True, alpha=1, savefilename=save_path+photo_name+"_heat.png")   
    
    # copy_original
    fig, ax = draw_display((width, height), imagefile=photo_file)
    ax.invert_yaxis()
    fig.savefig(save_path + photo_name + '\\' + photo_name + '.png')
    
    # save_rects
    find_all(photo_name, path_imgs, save_path)

    list_photo_0 = []
    list_photo_0.append(photo_0['x'].tolist())
    list_photo_0.append(photo_0['y'].tolist())
    list_photo_0.append(photo_0['dur'].tolist())

    # save_fixs
    with open(save_path + photo_name + '\\fixs.txt', 'w+') as fp:
        fp.write(json.dumps(list_photo_0))

    # print('find in: ', save_path + '\\' + photo_name + '\\' + 'rects.txt', save_path + photo_name + '\\fixs.txt')
    match_rect_fixs(photo_name,  save_path + '\\' + photo_name + '\\' + 'rects.txt', save_path + photo_name + '\\fixs.txt')

    return True # fig, heatmap