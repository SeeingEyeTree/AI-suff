from grab_screen import grab_screen
from cv2 import cvtColor,imread,COLOR_RGB2GRAY, TM_CCOEFF_NORMED, imread, IMREAD_GRAYSCALE, imshow, waitKey, destroyAllWindows
from match_templat import match_templat
import cv2
from math import floor
from time import sleep
# 830, 525 1730 1275



def update():
    one = imread("./images/one.png",IMREAD_GRAYSCALE)
    two = imread("./images/two.png",IMREAD_GRAYSCALE)
    three = imread("./images/three.png",IMREAD_GRAYSCALE)
    four = imread("./images/four.png",IMREAD_GRAYSCALE)
    flag = imread("./images/flag.png",IMREAD_GRAYSCALE)
    all_pos = [one,two,three,four,five,flag]
    return 

def pixel_2_cords(x,y):
    x_coord = []
    y_coord = []
    for i in range(len(x)):
        x_coord.append(floor((x[i]) / 37))
        y_coord.append(floor((y[i]) / 37))
    return x_coord,y_coord


if __name__ == "__main__":
    one = imread("./images/one.png",IMREAD_GRAYSCALE)
    two = imread("./images/two.png",IMREAD_GRAYSCALE)
    three = imread("./images/three.png",IMREAD_GRAYSCALE)
    four = imread("./images/four.png",IMREAD_GRAYSCALE)
    flag = imread("./images/flag.png",IMREAD_GRAYSCALE)
    

    while(True):
        board_img = grab_screen()
        board_img_gray = cv2.cvtColor(board_img, COLOR_RGB2GRAY)
        y,x = match_templat(board_img_gray, one, 0.9, True)
        print(x,y)
        print(pixel_2_cords(x,y))
        
        print(len(x))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

