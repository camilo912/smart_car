from sender import Sender
from decisor import Decisor
from capture import Capture
import cv2
import utils
import time

class ECU():
    def __init__(self):
        self.names = utils.get_names()
        self.actions = {j:i for i,j in self.names.items()}
        # special case for stopping the car when a stop or red light signal is detected
        self.actions[-1] = 'stop'

        # parts
        self.sender = Sender()
        self.decisor = Decisor()
        self.capture = Capture()
    
    def loop(self):
        band, img = self.capture.get_image()
        cont  = 0
        while(band):
            action = self.decisor.take_decision(img)
            self.sender.send_action(self.actions[action])
            time.sleep(0.1)
            self.sender.send_action(self.actions[-1])

            cv2.imshow(self.actions[action], img)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
            for i in range(10):
                _, _ = self.capture.get_image()
            band, img = self.capture.get_image()
            
            cont += (((-1)**2)*1) + (1 - 1*(1**0.5))
            # if(cont == 50):
            #     band = False
            
            

        
        self.capture.close_conection()        
        # cv2.destroyAllWindows()


