import cv2
import numpy as np

def match_templat(where, what, threshold, test=False):
    res = cv2.matchTemplate(where, what, cv2.TM_CCOEFF_NORMED)
    loc = np.where( res >= threshold)
    if test:
	    whereRGB = cv2.cvtColor(where, cv2.COLOR_GRAY2RGB)
	    w1, h1 = what.shape[::-1]
	    for pt1 in zip(*loc[::-1]):
	            cv2.rectangle(whereRGB, pt1, (pt1[0] + w1, pt1[1] + h1), (0,0,255), 2)
	    cv2.imshow('matches',whereRGB)
	    #print(loc)

    y=loc[1]
    x=loc[0]
    """
    x_clean = [0]
    y_clean = [0]
    #print(len(x))
    for i in range(len(x) - 1):
        x_diffrent = 0
        y_diffrent = 0

        for cleaan_x in x_clean:
            if abs(x[i] - cleaan_x) >= 5:
                x_diffrent += 1
        
        for cleaan_y in y_clean:
            if abs(y[i] - cleaan_y) >= 5:
                y_diffrent += 1

        if x_diffrent == len(x_clean) or (y_diffrent == len(y_clean)):
            x_clean.append(x[i])
            y_clean.append(y[i])
        else:
            #print(f"skiped {x[i]}, {y[i]}")
            pass
    x_clean.pop(0)
    y_clean.pop(0)
    """
    return x,y

