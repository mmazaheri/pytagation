import csv
import cv2

cameraCapture = cv2.VideoCapture('/home/mahdi/Desktop/seshanbeh/test1_ali.avi')
cv2.namedWindow('MyWindow')

print 'IMPORTANT: Type \'e\' and press ENTER when you want to quit!'
# fps = int(raw_input('Please Enter video speed(frame per sec, i.e. 60): '))
points = raw_input('Please Enter line points(x1 y1 x2 y2, i.e. 12 32  43 54): ')
points = [int(i) for i in points.split()]

skip = int(raw_input('skip frame(if not type 0 and press ENTER.)? '))
success, frame = cameraCapture.read()
success, frame = cameraCapture.read()
temp_flow = 0
frame_num = 0

with open('../some.csv', 'a') as f:
    writer = csv.writer(f)

    while success:
        frame_num += 1
        if frame_num <= skip:
            success, frame = cameraCapture.read()
            continue
        cv2.putText(frame, str(frame_num), (25, 25),
                cv2.FONT_HERSHEY_PLAIN, 2.0, (0, 0, 255),
                thickness=2, lineType=cv2.CV_AA)
        cv2.line(frame, (points[0], points[1]), (points[2], points[3]), (0,255,0), 1, cv2.CV_AA, 0)
        
        # if frame_num%(5*25) == 0:
        #     temp_flow = int(raw_input('Enter Flow: '))
            #: save temp_flow
        cv2.imshow('MyWindow', frame)
        cv2.waitKey(30)
        cars = raw_input(str(frame_num) + ' Please enter Car No: ')
        if cars == 'e':
            f.close()  
            break 
        writer.writerow([frame_num, cars])
        success, frame = cameraCapture.read()

cv2.destroyWindow('MyWindow')