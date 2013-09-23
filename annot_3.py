from os import listdir
from os.path import isfile, join
import csv

import cv2

cv2.namedWindow('window')
slc = {'x':-1,'y':-1,'w':0,'h':0}
drawing_slc = False
frame = 0
chng = 0
takh = 0
data_row = []

def onMouse(event, x, y, flags, param):
    global frame, rect, drawing_slc, takh, slc, chng

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
            cv2.rectangle(frame, (slc['x'],slc['y']), (slc['x']+slc['w'],slc['y']+slc['h']), (0,0,255), 1)  
            chng = 1
            print 'changed'


#: Open Video file
cameraCapture = cv2.VideoCapture('/home/mahdi/Desktop/train_videos/chamraan.avi')
points = raw_input('Please Enter line points(x1 y1 x2 y2, i.e. 12 32  43 54): ')
points = [int(i) for i in points.split()]

skip = int(raw_input('skip frame(if not type 0 and press ENTER.)? '))

#: Reading first two frames
success, frame = cameraCapture.read()
frame_num = 0

with open('../ant_file_3.csv','a') as ant_file:
    cswriter = csv.writer(ant_file, delimiter=',')

    while success:
        success, frame = cameraCapture.read()
        frame_num += 1
        if frame_num <= skip:
            continue

        cv2.putText(frame,
                    str(frame_num),
                    (30, 30),
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

        cv2.imshow('window', frame)
        cv2.setMouseCallback('window', onMouse)

        while True:
            temp = frame.copy()
            cv2.rectangle(temp, (slc['x'],slc['y']), (slc['x']+slc['w'],slc['y']+slc['h']), (0,255,0), 2)
            if chng == 1:
                print 'bayad beneviseh!'
                chng = 0
                data_row = [frame_num, slc['x'], slc['y'], slc['x']+slc['w'], slc['y']+slc['h']]
                cswriter.writerow(data_row)

            cv2.imshow('window', temp)

            if cv2.waitKey(1) == 'f':
                print 'f'
                break
            elif cv2.waitKey(1) == 'e':
                print 'e'
                ant_file.close()
                cv2.destroyWindow('window')
                break
        if cv2.waitKey(1) == 'e':
            break
