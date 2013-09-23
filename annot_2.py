from os import listdir
from os.path import isfile, join
import csv

import cv2

cv2.namedWindow('MyWindow')
slc = {'x':-1,'y':-1,'w':0,'h':0}
drawing_slc = False
img = 0
chng = 0
takh = 0
data_row = []

def onMouse(event, x, y, flags, param):
    global img, rect, drawing_slc, takh, slc, chng

    if event == cv2.EVENT_MOUSEMOVE:
        if drawing_slc:
            slc['w'] = x - slc['x']
            slc['h'] = y - slc['y']

    elif event == cv2.EVENT_LBUTTONDOWN:
        drawing_slc = True
        slc['x'] = x
        slc['y'] = y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing_slc = False
        if slc['w'] < 0:
            slc['x'] += slc['w']
            slc['w'] *= -1

        if slc['h'] < 0:
            slc['y'] += slc['h']
            slc['h'] *= -1

        if chng == 0:
            cv2.rectangle(img, (slc['x'],slc['y']), (slc['x']+slc['w'],slc['y']+slc['h']), (0,0,255), 1)
            takh = raw_input('Please Enter Driving offenses[if 0 skipped]: ')
            a = takh  
            try:
                takh = int(takh)
                if takh == 0:
                    cv2.rectangle(img, (slc['x'],slc['y']), (slc['x']+slc['w'],slc['y']+slc['h']), (255,255,255), 2)
                else:
                    chng = 1
                    print 'changed'
            except:
                takh = a
        elif chng == 2:
            cv2.rectangle(img, (slc['x'],slc['y']), (slc['x']+slc['w'],slc['y']+slc['h']), (255,0,0), 1)
            chng = 3

points = raw_input('Please Enter line points(x1 y1 x2 y2, i.e. 12 32  43 54): ')
points = [int(i) for i in points.split()]

mypath = '/home/mahdi/Desktop/Vision Sources/test_imgs'#raw_input('Please type the image folder address: ')
images_addr = [ f for f in listdir(mypath) if isfile(join(mypath,f))]

with open('../ant_file_2.csv','a') as ant_file:
    cswriter = csv.writer(ant_file, delimiter=',')
    for f in images_addr:
        img = cv2.imread(join(mypath,f))
        img = cv2.resize(img,(0,0),fx=0.4,fy=0.4)
        temp = img.copy()
        cv2.line(img, (points[0], points[1]), (points[2], points[3]), (0,255,0), 1, cv2.CV_AA, 0)
        cv2.imshow('MyWindow', img)
        cv2.setMouseCallback('MyWindow', onMouse)    
        while True:
            temp = img.copy()
            cv2.rectangle(temp, (slc['x'],slc['y']), (slc['x']+slc['w'],slc['y']+slc['h']), (0,255,0), 2)
            if chng == 1 and type(takh) is not str:
                print 'bayad beneviseh!'
                chng = 2
                data_row = [f, takh, int(2.5*slc['x']), int(2.5*slc['x']), int(2.5*(slc['x']+slc['w'])), int(2.5*(slc['y']+slc['h']))]
            elif chng == 3:
                data_row.extend([int(2.5*slc['x']), int(2.5*slc['x']), int(2.5*(slc['x']+slc['w'])), int(2.5*(slc['y']+slc['h']))])
                cswriter.writerow(data_row)
                chng = 0
            cv2.imshow('MyWindow', temp)
            cv2.waitKey(1)
            
            if takh == 'f':
                takh = -1
                break
            elif takh == 'e':
                ant_file.close()
                cv2.destroyWindow('MyWindow')
                break
        if takh == 'e':
            break

