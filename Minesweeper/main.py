import numpy as np
from time import sleep
from match_templat import match_templat
import cv2
from img_processing import pixel_2_cords
from grab_screen import grab_screen
from functions import add_to_board, detect_enclosed_regions, find_next_move,check_tile, find_safe_tile_recursive
from math import floor 

# green tile mask (hMin = 38 , sMin = 157, vMin = 200), (hMax = 42 , sMax = 168, vMax = 218)
# brown maks (hMin = 0 , sMin = 0, vMin = 0), (hMax = 36 , sMax = 78, vMax = 255)
lower = np.array([0,0,0])
upper = np.array([36,78,255])

debug = False


one = cv2.imread("./images/one.png",cv2.IMREAD_GRAYSCALE)
two = cv2.imread("./images/two.png",cv2.IMREAD_GRAYSCALE)
three = cv2.imread("./images/three.png",cv2.IMREAD_GRAYSCALE)
four = cv2.imread("./images/four.png",cv2.IMREAD_GRAYSCALE)
five = cv2.imread("./images/five.png",cv2.IMREAD_GRAYSCALE)
flag = cv2.imread("./images/flag.png",cv2.IMREAD_GRAYSCALE)



img_list = [[one,1],[two,2],[three,3],[four,4],[five,5],[flag,9]]

sleep(4)

board = [[0 for col in range(24)] for row in range(20)]


# Type aliases


while True:

    board_img = grab_screen((831, 522, 1730, 1273))
    board_img_gray = cv2.cvtColor(board_img, cv2.COLOR_RGB2GRAY)

    hsv = cv2.cvtColor(board_img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(board_img, board_img, mask=mask)
    if debug == True:
        cv2.imshow("result", result)
        while True:
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                print(*board, sep ='\n')
                break

    for i in range(24):
        for j in range(20):
                x = floor(2 + i * 37.4583333333)
                y = floor(2 + j * 37.55)
                if result[y][x][0] != 0:
                    board[j][i] = 8

    #y,x = match_templat(board_img_gray, img_list[5][0], 0.80,True)
    
    for i in range(len(img_list)):
        y,x = match_templat(board_img_gray, img_list[i][0], 0.80,False)

        x,y = pixel_2_cords(x,y)

        board = add_to_board(board, y, x, img_list[i][1])

    move = find_safe_tile_recursive(board)
    print(move)
    if move != None:
        board = check_tile(move[1][0], move[1][1], move[0],board)
        pass
    else:
        print(*board, sep ='\n')
        move = find_safe_tile_recursive(board)
        print(move)
        board = check_tile(move[1][0], move[1][1], move[0],board)
    #print(*board, sep ='\n')





print(*board, sep ='\n')
print(find_next_move(board))


