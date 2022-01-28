import json
import cv2
import numpy
import math
from sklearn.cluster import KMeans
import json
import pandas as pd
import ast
import numpy as np
from numpy.linalg import *
import csv

from win32api import GetSystemMetrics
from scipy.spatial import distance

W = GetSystemMetrics(0)
H = GetSystemMetrics(1)

def match_rect_fixs(photo_name, rects_path, fixs_path):
    # print('path del rect', rects_path)
    rect = []
    fixs = []
    
    with open(rects_path) as rect_file:
        rect = json.load(rect_file)
    with open(fixs_path) as fixs_file:
        fixs = json.load(fixs_file)
    
    # 1)    associare le parole del testo alle cc, ma NON i pallini sulle i, e le virgole e gli ' e gli accenti
    rect_0 = []
    i = 0
    for x0, y0, w0, h0 in rect:
        maybe = True
        j = 0
        for x1, y1, w1, h1 in rect:
            if not i == j:
                if x0 > x1 and y0 > y1 and x0+w0 < x1+w1 and y0+h0 < y1+h1:
                    maybe = False
            j += 1
        if maybe:
            rect_0.append([x0, y0, w0, h0])
        i += 1

    img = cv2.imread(rects_path.replace('rects.txt', '') + photo_name + '.png')
    for (x, y, w, h) in rect_0:
        cv2.rectangle(img, (x, y), (x+w, y+h), color=(255, 0, 255), thickness=1)

    cv2.imwrite( rects_path.replace('rects.txt', '') + photo_name + '_cc.png', img)

    rect_1 = [[x, y, w, h, int(x+w/2), int(y+h/2)] for x, y, w, h in rect_0]
    h_ = [h for x, y, w, h, l1, l2 in rect_1]
    w_ = [w for x, y, w, h, l1, l2 in rect_1]
    h_mean = sum(h_) / len(h_)
    w_mean = sum(w_) / len(w_)
    # print(h_mean)

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    bins = gray/255
    bw = 1 - bins
    # print(bw)
    left = [ [i, 0] for i, x in enumerate(bw) if sum(x)>0 ] 
 
    min_max_list = []
    point = [ left[0][0], left[0][0] ]
    for y, x in left[1:]:
        if y - point[1] > 1:
            min_max_list.append(point)
            point = [y, y]
        else:
            point[1] = y
    min_max_list.append(point)
    # print(min_max_list)
    
    app = []
    for x, y, w, h, cx, cy in rect_1:
        for i, y_ in enumerate(min_max_list):
            if y_[0] <= cy <= y_[1]:
                app.append(i)
                break

    new_rect = list(map(lambda a: [a[0], a[1]], zip(rect_1, app)))
    new_rect = sorted(new_rect, key=lambda x: (x[1], x[0][0], x[0][2]*x[0][3]))
    new_rect = [x for x in new_rect if x[0][3] > h_mean*0.6 or x[0][2] > w_mean*0.7]
    
    rect_dic = { 'a': [r[0] for r in new_rect], 'b': [r[1] for r in new_rect] }
    
    df = pd.DataFrame(rect_dic)
    grouped = df.groupby('b')['a'].apply(list)
    

    '''
        print rectangle in different colors grouped by lines
    '''
    COLS = [(255, 0, 0),(0, 255, 0),(0, 0, 255),(0, 0, 0),(255, 0, 255),(0, 255, 255),(255, 255, 0)]
    for (x, y, w, h, cx, cy), i in new_rect:
        cv2.rectangle(img, (x, y), (x+w, y+h), color=COLS[i], thickness=1)
    cv2.imwrite( rects_path.replace('rects.txt', '') + photo_name + '_colori.png', img)

    txt_path = r'../txts/'
    with open(txt_path + photo_name + '.txt', 'r', encoding='utf-8') as txt_file:
        txt = ast.literal_eval(txt_file.read())

    words = [t.replace('.', '').replace(',', '').replace(';', '').replace(':', '').replace('\'', ' ').replace('’',' ').replace('  ', ' ').split(' ') for t in txt]
    
    words_counter = 0
    for i, row in enumerate(words):
        pos_counter = 0
        for j, word in enumerate(row):
            for k in range(len(word)):
                grouped[i][pos_counter] += [word[k], word, k, words_counter]
                pos_counter += 1
            words_counter += 1

    rect_tot = []   
    for group in grouped:
        rect_tot += group
   
    fixs_ = [[x, y, dur, i, 'fixs'] for x, y, dur, i in zip(fixs[0], fixs[1], fixs[2], range(0, len(fixs[0])))]

    fix = [[x,y] for x,y,a,a,a in fixs_]
    
    # # 2)    su all_ scorrere finchè non trovo uno con 'fixs' e prelevare quello prima e quello dopo 
    # #       (o uno dei due che minimizza la distanza dal bordo o dal centroide in norma 2) 

    # min distanza fra fix iesima e rect j esimo
    # calcolo le dist minime dai centri dei rect...
    rect_center = [[cx, cy] for x, y, w, h, cx, cy, let, wor, let_idx, wor_idx in rect_tot]

    # print(rect_center)
    di = distance.cdist(fix, rect_center, 'euclidean')

    # lista di liste : fixs[0] avrà le distanze della prima fix da ogni componente
    # le ordino e prendo le prime 4 componenti più vicine e con queste vado a calcolare la distanza dai segmenti
    fixs_ = []
    # cerco min distance btw fix iesima e componente j esima 

    vista = []
    for i in range(len(di)):
        fixs_.append([[di[i][j], j] for j in range(len(di[i]))])
        # ordino la lista in base alle min distanze con le componenti e prendo solo le 4 componenti a min distanza
        fixs_[i].sort(key=lambda x: x[0])
        fixs_[i] = [fixs_[i][j] for j in range(1)]
        # print('min distanza di fix ', i, ' da componente ', fixs_[i][0][1] ,' ', rect_tot[fixs_[i][0][1]], ' : ', fixs_[i][0][0])
        
        if len(rect_tot[fixs_[i][0][1]]) > 10:
            # if type((rect_tot[fixs_[i][0][1]])[10])==list:
            app =  list((rect_tot[fixs_[i][0][1]])[10])
            app.append(i)
            (rect_tot[fixs_[i][0][1]])[10] = app
        else:
            rect_tot[fixs_[i][0][1]] += [[i]]

        wor_idx, wor, let_idx = rect_tot[fixs_[i][0][1]][9], rect_tot[fixs_[i][0][1]][7], rect_tot[fixs_[i][0][1]][8]
        vista.append([i, wor_idx, wor, let_idx])

    # # 3)    creare i due file di rappresentazione che dice il prof (vista.cvs & sommario.cvs)

    sommario = [ [ele[9], ele[7], (ele[8] if len(ele) > 10 else None)] for ele in rect_tot ]
    dict_sommario = {'a': [ele[0] for ele in sommario], 'b':  [ele[1] for ele in sommario], 'c': [ele[2] for ele in sommario]}
    df = pd.DataFrame(dict_sommario)
    grouped_sommario = df.groupby(['a', 'b'])

    csv_ = []
    for (i, word), group in grouped_sommario:
        chars = grouped_sommario['c'].apply(list)[(i, word)]
        chars = [x for x in chars if str(x) != 'nan']
        csv_.append(str(i)+','+str(word)+',"'+str(chars)+'"')
        print(i, word,  chars)
            

    with open(rects_path.replace('rects.txt', '') + "sommario.csv", "w", encoding='utf8') as f:
        for row in csv_:
            f.write(row+'\n')    
    
    with open(rects_path.replace('rects.txt', '') + 'vista.csv', 'w') as file_vi:
        for row in vista:
            file_vi.write(','.join([str(x) for x in row])+'\n')  
            

    # # TUTTO QUELLO CHE C'è QUI SOTTO  NON SI USA, LO LASCIO PER ORA
    # # print('min distanza:  ',fixs_[0], ' di fix ', fix_i,' da componente ', fixs_[fix_i][j][1])
    # # distanza di un punto p_fix dalla retta passante per p1 e p2 
    # # idea: per ogni fix cerco i rect a min distanza ( calcolo la distanza fra centro del rect e punto di fix),
    # # prendo i primi 4 risultati e per questi calcolo la distanza min tra punto di fix e segmento dato da ogni lato delle componenti connesse

    # # point coordinates of rects
    # # p0--------p2
    # # |         |
    # # |         |
    # # p1--------p3
    # for fix_i in range(len(fixs_)):
    #     min_dist = float('inf')
    #     index_min_dist = None
    #     # print('-')
    #     x_fix, y_fix = fix[fix_i]
    #     # print('fix coordinates: ', x_fix, y_fix)
    #     p_fix = (x_fix,y_fix)
    #     for j in range(len(fixs_[fix_i])):
    #         # print(rect[fixs_[fix_i][j][1]])
    #         x,y,w,h = rect[fixs_[fix_i][j][1]]
    #         p0 = np.array((x,y))
    #         p1 = np.array((x,y+h))
    #         p2 = np.array((x+w, y))
    #         p3 = np.array((x+w, y+h))

    #         # distanza del segmento passante da p1 e p2 da p3
    #         min_dist_fix = min([norm(np.cross(p0-p1, p1-p_fix))/norm(p0-p1), norm(np.cross(p2-p0, p0-p_fix))/norm(p2-p0), norm(np.cross(p1-p3, p3-p_fix))/norm(p1-p3), norm(np.cross(p2-p3, p3-p_fix))/norm(p2-p3)])
            
    #         if min_dist_fix < min_dist:
    #             min_dist = min_dist_fix
    #             index_min_dist = fixs_[fix_i][j][1]
    #         # dist = norm(np.cross(p2-p1, p1-p3))/norm(p2-p1)
    #         # print('min distanza:  ', min_dist_fix, ' di fix ', fix_i,' da componente ', fixs_[fix_i][j][1])
    #     # print('min distanza finale di fix ', fix_i,' da componente ', index_min_dist,' : ', min_dist)
        

    
    

    return True


