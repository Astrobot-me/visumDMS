import cv2,maths

class UtlilitesFunction:
    def __init__(self):
        pass

    def findDistance(self,point1, point2, img=None):
        """
        Find the distance between two landmarks based on their
        index numbers.
        :param p1: Point1
        :param p2: Point2
        :param img: Image to draw on.
        :param draw: Flag to draw the output on the image.
        :return: Distance between the points
                 Image with output drawn
                 Line information
        """

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