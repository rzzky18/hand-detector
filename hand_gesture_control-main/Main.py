import cv2
import time
import math
import numpy as np
import pyautogui
import autopy
import HandTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Camera dimensions
wCam, hCam = 640, 480

# Initialize video capture
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Initialize time variables
pTime = 0
#cTime = 0

# Initialize hand detector
detector = htm.handDetector(maxHands=1, detectionCon=0.85, trackCon=0.8)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()   #(-63.5, 0.0, 0.5) min max

minVol = -63
maxVol = volRange[1]
print(volRange)
hmin = 50
hmax = 200
volBar = 400
volPer = 0
vol = 0
color = (0,215,255)

tipIds = [4, 8, 12, 16, 20]
mode = ''
active = 0


pyautogui.FAILSAFE = False
while True:
    success, img = cap.read()
    if not success:
        break

    # Flip the image
    img = cv2.flip(img, 1)
    
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    fingers = []

    if len(lmList) != 0:

        #Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0 -1]][1]:
            if lmList[tipIds[0]][1] >= lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        elif lmList[tipIds[0]][1] < lmList[tipIds[0 -1]][1]:
            if lmList[tipIds[0]][1] <= lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

               #  print(fingers)
        if (fingers == [0,0,0,0,0]) & (active == 0 ):
            mode='N'
        elif (fingers == [0, 1, 0, 0, 0] or fingers == [0, 1, 1, 0, 0]) & (active == 0 ):
            mode = 'Scroll'
            active = 1
        elif (fingers == [1, 1, 0, 0, 0] ) & (active == 0 ):
             mode = 'Volume'
             active = 1
        elif (fingers == [1 ,1 , 1, 1, 1] ) & (active == 0 ):
             mode = 'Cursor'
             active = 1
        elif (fingers == [0, 1, 0, 0, 1] ) & (active == 0 ): 
             mode = 'Right'
             active = 1
        elif (fingers == [0, 0, 0, 0, 1]) & (active == 0 ):
            mode = 'Left'
            active = 1 
        elif (fingers == [1, 0, 0, 0, 0]) & (active == 0 ): 
            mode = 'DoubleClick'
            active = 1                             

    ############# Scroll 👇👇👇👇##############
    if mode == 'Scroll':
        active = 1
     #   print(mode)
        putText(img, mode)
        cv2.rectangle(img, (200, 410), (245, 460), (255, 255, 255), cv2.FILLED)
        if len(lmList) != 0:
            if fingers == [0,1,0,0,0]:
              #print('up')
              #time.sleep(0.1)
                putText(img, mode = 'U', loc=(200, 455), color = (0, 255, 0))
                pyautogui.scroll(300)

            if fingers == [0,1,1,0,0]:
                #print('down')
              #  time.sleep(0.1)
                putText(img, mode = 'D', loc =  (200, 455), color = (0, 0, 255))
                pyautogui.scroll(-300)
            elif fingers == [0, 0, 0, 0, 0]:
                active = 0
                mode = 'N'

   ################# Volume 👇👇👇####################
    if mode == 'Volume':
        active = 1
       #print(mode)
        putText(img, mode)
        if len(lmList) != 0:
            if fingers[-1] == 1:
                active = 0
                mode = 'N'
                print(mode)
            
            else:
                 # print(lmList[4], lmList[8])
                    x1, y1 = lmList[4][1], lmList[4][2]  # Koordinat ujung ibu jari
                    x2, y2 = lmList[8][1], lmList[8][2]  # Koordinat ujung jari telunjuk
                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                    cv2.circle(img, (x1, y1), 10, color, cv2.FILLED) # Titik di ujung ibu jari
                    cv2.circle(img, (x2, y2), 10, color, cv2.FILLED) # Titik di ujung telunju
                    cv2.line(img, (x1, y1), (x2, y2), color, 3)  # Garis penghubung ibu jari - telunjuk
                    cv2.circle(img, (cx, cy), 8, color, cv2.FILLED) # Titik di tengah

                    length = math.hypot(x2 - x1, y2 - y1)  # Menghitung panjang garis antara ibu jari dan telunjuk
                    # print(length)

                    # hand Range 50-300
                    # Volume Range -65 - 0
                    #konversi jarak ke volume sistem
                    vol = np.interp(length, [hmin, hmax], [minVol, maxVol])
                    volBar = np.interp(vol, [minVol, maxVol], [400, 150])
                    volPer = np.interp(vol, [minVol, maxVol], [0, 100])
                    print(vol)
                    volN = int(vol)
                    if volN % 4 != 0:
                        volN = volN - volN % 4 # Membulatkan ke kelipatan 4
                        if volN >= 0:
                            volN = 0 # Maksimum volume
                        elif volN <= -64:
                            volN = -64  # Minimum volume
                        elif vol >= -11:
                            volN = vol  # Menyesuaikan volume jika tidak dalam rentang ekstrem

                 #    print(int(length), volN)
                    volume.SetMasterVolumeLevel(vol, None)
                    if length < 50:
                        cv2.circle(img, (cx, cy), 11, (0, 0, 255), cv2.FILLED) # Titik di tengah merah

                    cv2.rectangle(img, (30, 150), (55, 400), (209, 206, 0), 3)
                    cv2.rectangle(img, (30, int(volBar)), (55, 400), (215, 255, 127), cv2.FILLED)
                    cv2.putText(img, f'{int(volPer)}%', (25, 430), cv2.FONT_HERSHEY_COMPLEX, 0.9, (209, 206, 0), 3)

            
#######################################################################
    if mode == 'Right':
            active = 1
            # Menampilkan mode aktif
            putText(img, mode)
            cv2.rectangle(img, (200, 410), (245, 460), (255, 255, 255), cv2.FILLED)
            
            if len(lmList) != 0:
                # Pola jari untuk klik Kanan 
                if fingers == [1, 1, 0, 0, 1]:
                    # Simulasikan klik Kanan
                    pyautogui.click(button='right')
                    
                    # Menampilkan konfirmasi klik berhasil
                    putText(img, "Click Successful", loc=(260, 455), color=(0, 255, 0))  # Hijau sebagai konfirmasi
                    cv2.rectangle(img, (200, 410), (245, 460), (0, 255, 0), cv2.FILLED)  # Kotak hijau
                    
                    time.sleep(4)  # Jeda untuk mencegah klik berulang
                    
                # Jika semua jari turun, nonaktifkan mode
                elif fingers == [0, 0, 0, 0, 0]:
                    active = 0
                    mode = 'N'
#######################################################################

    if mode == 'Left':
        active = 1
        # Menampilkan mode aktif
        putText(img, mode)
        cv2.rectangle(img, (200, 410), (245, 460), (255, 255, 255), cv2.FILLED)
        
        if len(lmList) != 0:
            # Pola jari untuk klik kiri 
            if fingers == [0, 1, 0, 0, 1]:
                # Simulasikan klik kiri
                pyautogui.click()
                
                # Menampilkan konfirmasi klik berhasil
                putText(img, "Click Successful", loc=(260, 455), color=(0, 255, 0))  # Hijau sebagai konfirmasi
                cv2.rectangle(img, (200, 410), (245, 460), (0, 255, 0), cv2.FILLED)  # Kotak hijau
                
                time.sleep(4)  # Jeda untuk mencegah klik berulang
                
            # Jika semua jari turun, nonaktifkan mode
            elif fingers == [0, 0, 0, 0, 0]:
                active = 0
                mode = 'N'


#######################################################################

    if mode == 'DoubleClick':
            active = 1
            # Menampilkan mode aktif
            putText(img, mode)
            cv2.rectangle(img, (200, 410), (245, 460), (255, 255, 255), cv2.FILLED)
            
            if len(lmList) != 0:
                # Pola jari untuk  Double klik 
                if fingers == [1, 0, 0, 0, 1]:
                    # Simulasikan  Double klik
                    pyautogui.doubleClick()
                    
                    # Menampilkan konfirmasi klik berhasil
                    putText(img, "Click Successful", loc=(260, 455), color=(0, 255, 0))  # Hijau sebagai konfirmasi
                    cv2.rectangle(img, (200, 410), (245, 460), (0, 255, 0), cv2.FILLED)  # Kotak hijau
                    
                    time.sleep(5)  # Jeda untuk mencegah klik berulang
                    
                # Jika semua jari turun, nonaktifkan mode
                elif fingers == [0, 0, 0, 0, 0]:
                    active = 0
                    mode = 'N'

#######################################################################
    if mode == 'Cursor':
        active = 1
        #print(mode)
        putText(img, mode)
        cv2.rectangle(img, (110, 20), (620, 350), (255, 255, 255), 3)

        if fingers[1:] == [0,0,0,0]: #Kode normal Jempol 
            active = 0
            mode = 'N'
            print(mode)
        else:
            if len(lmList) != 0:
                x1, y1 = lmList[8][1], lmList[8][2]
                w, h = autopy.screen.size()
                X = int(np.interp(x1, [110, 620], [0, w - 1]))
                Y = int(np.interp(y1, [20, 350], [0, h - 1]))
                cv2.circle(img, (lmList[8][1], lmList[8][2]), 7, (255, 255, 255), cv2.FILLED)
                cv2.circle(img, (lmList[4][1], lmList[4][2]), 10, (0, 255, 0), cv2.FILLED)  #thumb

                if X%2 !=0:
                    X = X - X%2
                if Y%2 !=0:
                    Y = Y - Y%2
                print(X,Y)
                autopy.mouse.move(X,Y)
              #  pyautogui.moveTo(X,Y)
              

                # Left click
                #if fingers[0] == 0 and fingers[1] == 0:
                 
                 #   print("Left click")
                  
                  #  pyautogui.click(button='left')

                # Right click
                #if fingers[0] == 0 and fingers[2] == 0:
                 #   print("Right click")
                  #  pyautogui.click(button='right')

                # Double click
                #if fingers[0] == 0 and fingers[3] == 0:
                 #   print("Double click")
                  #  pyautogui.doubleClick()


    cTime = time.time()
    fps = 1/((cTime + 0.01)-pTime)
    pTime = cTime

    cv2.putText(img,f'FPS:{int(fps)}',(480,50), cv2.FONT_ITALIC,1,(255,0,0),2)
    cv2.imshow('Hand LiveFeed',img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    def putText(img, mode,loc = (250, 450), color = (0, 255, 255)):
        cv2.putText(img, str(mode), loc, cv2.FONT_HERSHEY_COMPLEX_SMALL,
                    3, color, 3)
