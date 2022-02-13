import cv2
import numpy as np
import argparse
from skel_kinect2 import KinectStream

class DrawSkeleton:
    def __init__(self, file) -> None:
        self.__stream = KinectStream(file)
        self.reset()
    
    def __del__(self) -> None:
        cv2.destroyAllWindows()

    def reset(self):
        self.__image = np.ones((480, 640, 3), np.uint8) * 255

    def draw(self):
        scale = 300
        offset_factor = 1/2
        for skeleton in self.__stream:
            for name in skeleton:
                x, y, _ = skeleton[name]
                h, w, _ = self.__image.shape
                x, y = int(x*scale + w*offset_factor), int(-y*scale + h*offset_factor)
                cv2.circle(self.__image, (x, y), 3, (0, 0, 255), -1)
                cv2.putText(self.__image, '{}'.format(name), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
                cv2.imshow('Skeleton', self.__image)
            if cv2.waitKey(0) & 0xFF == ord('q'):
                break
            self.reset()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='?', type=str, help='skeleton_ssi.csv file from nova software')
    args = parser.parse_args()

    draw_skel = DrawSkeleton(args.file)
    draw_skel.draw()