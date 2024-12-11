import cv2
import math

class UtlilitesFunction:
    def __init__(self):
        pass

    def findDistance(self,point1, point2, img=None):


        x1, y1 = point1
        x2, y2 = point2
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        length = math.hypot(x2 - x1, y2 - y1)
        info = (x1, y1, x2, y2, cx, cy)
        if img is not None:
            cv2.circle(img, (x1, y1), 1, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 1, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 1)
            # cv2.circle(img, (cx, cy), 1, (255, 0, 255), cv2.FILLED)
            return length,info, img
        else:
            return length, info
        
    def rescaleFrame(self,image,scale=0.75):
        '''
        Work for Image,Video & Live Video Feed
        '''
        width = int(image.shape[1]*scale)
        height = int(image.shape[0]*scale)
        dimensions = (width,height)

        scaledImage = cv2.resize(image,dimensions,interpolation=cv2.INTER_AREA)
        return scaledImage