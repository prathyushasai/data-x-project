import numpy as np
import cv2
import os, sys

cwd = os.getcwd()
if 'frames' not in os.listdir(cwd):
    os.mkdir(cwd + "/frames")
run = True

def livestream_to_frames():

    def start_end(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            sys.exit(0)
        
    window_name='Live Stream'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 600, 600)
    cap = cv2.VideoCapture(0)
    framerate = cv2.cv.CV_CAP_PROP_FPS * 3
    count = 0

    while(run):
        # Capture frame-by-frame
        ret, frame = cap.read()
        cv2.setMouseCallback(window_name, start_end)
        cv2.imshow(window_name, frame)
        if count % framerate == 0:        
            # Our operations on the frame come here
            name = "frame%d.jpg"%count
            cv2.imwrite(os.path.join(cwd+'/frames/', name), frame)
        cv2.putText(frame, str(count), (20, 500), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 2)
            # Display the resulting frame
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        count+=1
        

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
if __name__ == '__main__':
    livestream_to_frames()
