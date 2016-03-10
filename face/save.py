
import cv2
import cv2.cv as cv
import sys

cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)
frameCount= 0;
img_count=0
skipFrame = 2;
img_batch_size = 30;

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.6,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
	
	if  img_count < img_batch_size and frameCount % skipFrame == 0:
		crop_frame = frame[y:y+h, x:x+w]
		cv2.imwrite( "Image-" + str(img_count) + ".jpg", crop_frame );	
		img_count +=1
		
    # Display the resulting frame
    cv2.imshow('Video', frame)
    frameCount+=1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
