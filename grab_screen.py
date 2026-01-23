# Done by Frannecklp

import cv2
import numpy as np
import win32gui, win32ui, win32con, win32api
from math import floor
import time

time.sleep(5)
def grab_screen(region=None):

    hwin = win32gui.GetDesktopWindow()

    if region:
            left,top,x2,y2 = region
            width = x2 - left + 1
            height = y2 - top + 1
    else:
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
    
    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height,width,4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return img

if __name__ == '__main__':
    import time
    time_start=time.time()
    j=0
    
    #while True:
    """
        mask_min=(72,94,97)
        mask_max=(173,249,248)
        
        img=grab_screen((80,1319,1730,1320))
        hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        masked=cv2.inRange(hsv,mask_min,mask_max)
        cv2.imshow('window',masked)
        #print(masked[0])
        find_list=[]
        for i in range(len(masked[0])):
            if masked[0][i]!=0:
                #print(i)
                find_list.append(i)
        j+=1
        if cv2.waitKey(25) & 0xFF == ord('q'):
            
            cv2.destroyAllWindows()
            #print(min(find_list)+floor((max(find_list)-min(find_list))/2))
            print(time.time()-time_start)
            break

    """
    """
        img=grab_screen((400,180,1700,1380))
        cv2.imshow('window',img)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            
            cv2.destroyAllWindows()
    """
    img=grab_screen((0,0,2560,1600))
    cv2.imshow('window',img)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        
        cv2.destroyAllWindows()
    
