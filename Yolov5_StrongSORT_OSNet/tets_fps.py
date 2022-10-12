import cv2

cap = cv2.VideoCapture("C:\\Users\\nikol\\Yolov5_StrongSORT_OSNet\data\\video\\tets.mp4")

while True:
        cap.set(cv2.CAP_PROP_FPS,10)
        ret,frame = cap.read()
        print(cap.get(cv2.CAP_PROP_FPS))
