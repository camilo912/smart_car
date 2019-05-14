import cv2

class Capture():
    def __init__(self):
        # self.address = 'data/VID_20190404_200633.mp4'
        # self.address = 'data/VID_20190423_120846.mp4'
        self.address = 'http://10.42.0.235:8080/?action=stream'
        # self.address = 'data/video_20.avi'
        self.open_conection()
    
    def open_conection(self):
        self.cap = cv2.VideoCapture(self.address)

    def close_conection(self):
        self.cap.release()

    def get_image(self):
        # # use open and close here instead of in consturctor for streaming
        # self.open_conection()
        ret, frame = self.cap.read()
        # self.close_conection()
        return ret, frame
