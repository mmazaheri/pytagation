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

#: Open Video file
cameraCapture = cv2.VideoCapture('/home/mahdi/Desktop/train_videos/chamraan.avi')
points = raw_input('Please Enter line points(x1 y1 x2 y2, i.e. 12 32  43 54): ')
points = [int(i) for i in points.split()]

skip = int(raw_input('skip frame(if not type 0 and press ENTER.)? '))

#: Reading first two frames
success, frame = cameraCapture.read()
success, frame = cameraCapture.read()
frame_num = 0

with open('../ant_file_3.csv','a') as ant_file:
    cswriter = csv.writer(ant_file, delimiter=',')

    while success:
        frame_num += 1
        if frame_num <= skip:
            continue

        cv2.putText(frame,
                    str(frame_num),
                    (25, 25),
                    cv2.FONT_HERSHEY_PLAIN,
                    2.0,
                    (0, 0, 255),
                    thickness=2,
                    lineType=cv2.CV_AA
                    )

        cv2.line(   frame,
                    (points[0], points[1]),
                    (points[2], points[3]),
                    (0,255,0),
                    1,
                    cv2.CV_AA,
                    0
                )

        cv2.imshow('MyWindow', frame)
        cv2.setMouseCallback('MyWindow', onMouse)

        while True:
            temp = img.copy()
            cv2.rectangle(temp, (slc['x'],slc['y']), (slc['x']+slc['w'],slc['y']+slc['h']), (0,255,0), 2)
            if chng == 1 and type(takh) is not str:
                print 'bayad beneviseh!'
                chng = 2
                data_row = [f, takh, slc['x'], slc['y'], slc['x']+slc['w'], slc['y']+slc['h']]
            elif chng == 3:
                data_row.extend([slc['x'], slc['y'], slc['x']+slc['w'], slc['y']+slc['h']])
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
