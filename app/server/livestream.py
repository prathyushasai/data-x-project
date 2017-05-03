import numpy as np
import cv2
import os, sys

def livestream_to_frames():

    def start_end(event, x, y, flags, param):
        global run
        if event == cv2.EVENT_LBUTTONDOWN:
            sys.exit(0)
        
    window_name='Live Stream'
    # cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, start_end)

    cap = cv2.VideoCapture(0)
    count = 0
    cwd = os.getcwd()

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
    
        # Our operations on the frame come here
        name = "frame%d.jpg"%count
        if 'frames' not in os.listdir(cwd):
            os.mkdir(cwd + "/frames")
        cv2.imwrite(os.path.join(cwd+'/frames/', name), frame)
        count+=1

        # Display the resulting frame
        cv2.imshow(window_name, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

    
livestream_to_frames()