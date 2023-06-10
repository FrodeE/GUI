import pyautogui, pytweening, time, random, win32gui, cv2
from pymsgbox import *
import time

#----------------------------------

def random_interval():
    return round(random.uniform(0.3, 1), 1)

#----------------------------------

def getPointOnCurve(x1, y1, x2, y2, n, tween=None, offset=0):
    """Returns the (x, y) tuple of the point that has progressed a proportion
    n along the curve defined by the two x, y coordinates.
    If the movement length for X is great than Y, then Y offset else X
    """
    # for compatibility Backward
    if getPointOnCurve.tween and getPointOnCurve.offset:  # need DEL
        tween = getPointOnCurve.tween                     # need DEL
        offset = getPointOnCurve.offset                   # need DEL

    x = ((x2 - x1) * n) + x1
    y = ((y2 - y1) * n) + y1
    if tween and offset:
        offset = (n - tween(n)) * offset
        if abs(x2 - x1) > abs(y2 - y1):
            y += offset
        else:
            x += offset
    return x, y

#----------------------------------

getPointOnCurve.tween = None
getPointOnCurve.offset = 0

def set_curve(func, tween=None, offset=0):
    func.tween = tween
    func.offset = offset

#----------------------------------

def imageScaling(template, scale):
    img = cv2.imread(template)

    width = int(img.shape[1] * scale)
    height = int(img.shape[0] * scale)

    dsize = (width, height)

    output = cv2.resize(img, dsize, interpolation = cv2.INTER_LINEAR)

    cv2.imwrite('C:/Users/Alen/Desktop/FAAKbot/cv2-resize-image-50.png', output)

#----------------------------------

def liiguJaKliki_main(template):
    location = pyautogui.locateCenterOnScreen(template, confidence=0.75)
    while location is None:
        location = pyautogui.locateCenterOnScreen(template, confidence=0.75)
    x, y = location
    pyautogui.moveTo(x, y, random_interval())
    pyautogui.click()

def liiguJaKliki(template):
    set_curve(getPointOnCurve, pytweening.easeInCubic, round(random.uniform(20, 50)))

    if template == 'TFT.png':
        start_time = time.time()
        tftlocation = pyautogui.locateCenterOnScreen(template, confidence=0.9)
        while tftlocation is None:
            tftlocation = pyautogui.locateCenterOnScreen(template, confidence=0.9)
            elapsed_time = time.time() - start_time
            if elapsed_time > 1:
                break

        if tftlocation == None:
            tft_HLLocation = pyautogui.locateCenterOnScreen('TFT_HL.png')
            while tft_HLLocation is None:
                tft_HLLocation = pyautogui.locateCenterOnScreen('TFT_HL.png')
            TFT_HLX, TFT_HLY = tft_HLLocation
            pyautogui.moveTo(TFT_HLX, TFT_HLY, random_interval())
            pyautogui.click()
        else:
            TFTX, TFTY = tftlocation
            pyautogui.moveTo(TFTX, TFTY, random_interval())
            pyautogui.click()
    else:
        liiguJaKliki_main(template)

#----------------------------------

def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))


#----------------------------------

def callback(hwnd, extra):
    if win32gui.GetWindowText(hwnd) == 'League of Legends':
        rect = win32gui.GetWindowRect(hwnd)

#----------------------------------

def launcherFocus():
    if __name__ == "__main__":
        results = []
        top_windows = []
        win32gui.EnumWindows(windowEnumerationHandler, top_windows)
        for i in top_windows:
            if "league of legends" in i[1].lower():
                win32gui.ShowWindow(i[0],10)
                win32gui.SetForegroundWindow(i[0])
                rect = win32gui.GetWindowRect(i[0])
                x = rect[0]
                y = rect[1]
                w = rect[2] - x
                h = rect[3] - y
                break
    return (x, y), (w, h)

#----------------------------------

def scalingCoeficient(width, height):
    if width / 1280 == height / 720:
        return width / 1280

#----------------------------------

def checkPhase(template):
    if pyautogui.locateOnScreen(template, region=(775, 5, 50, 30), confidence=0.8): #, region=(775, 5, 50, 30)
        print('Test1')
        return 1
    else:
        return None

#----------------------------------

def itemGrab():
    set_curve(getPointOnCurve, pytweening.easeInCubic, round(random.uniform(20, 50)))

    pyautogui.moveTo(550, 168, random_interval())
    pyautogui.click(button='right')
    time.sleep(2)

    pyautogui.move(760, 0, random_interval())
    pyautogui.click(button='right')
    time.sleep(3)
    pyautogui.move(0, 550, random_interval())
    pyautogui.click(button='right')
    time.sleep(2)
    pyautogui.move(-760, 0, random_interval())
    pyautogui.click(button='right')
    time.sleep(2)
    pyautogui.move(0, -450, random_interval())
    pyautogui.click(button='right')
    time.sleep(2)

    pyautogui.move(700, 0, random_interval())
    pyautogui.click(button='right')
    time.sleep(3)
    pyautogui.move(0, 400, random_interval())
    pyautogui.click(button='right')
    time.sleep(2)
    pyautogui.move(-640, 0, random_interval())
    pyautogui.click(button='right')
    time.sleep(2)
    pyautogui.move(0, -350, random_interval())
    pyautogui.click(button='right')
    time.sleep(2)

    pyautogui.move(580, 0, random_interval())
    pyautogui.click(button='right')
    time.sleep(1.5)
    pyautogui.move(0, 300, random_interval())
    pyautogui.click(button='right')
    time.sleep(1.5)
    pyautogui.move(-520, 0, random_interval())
    pyautogui.click(button='right')
    time.sleep(1.5)
    pyautogui.move(0, -250, random_interval())
    pyautogui.click(button='right')
    time.sleep(1.5)

    pyautogui.move(460, 0, random_interval())
    pyautogui.click(button='right')
    time.sleep(1)
    pyautogui.move(0, 200, random_interval())
    pyautogui.click(button='right')
    time.sleep(1)
    pyautogui.move(-400, 0, random_interval())
    pyautogui.click(button='right')
    time.sleep(1)
    pyautogui.move(0, -150, random_interval())
    pyautogui.click(button='right')
    time.sleep(1)

def getItemsOnGround():
    while(True):
        if checkPhase('Round4.png'):
            itemGrab()
            break

#----------------------------------

def gameCheck():
    try:
        (x, y), (w, h) = launcherFocus()
        if (w, h) == (1920,1080):
            return 1
        else:
            return None
    except:
        return None

def accept():
    liiguJaKliki('Accept.png')
    while (True):
        time.sleep(7)
        if gameCheck():
            print('test')
            break
        else:
            liiguJaKliki('Accept.png')

#----------------------------------

pyautogui.getPointOnLine = getPointOnCurve

#----------------------------------

try:
    (x, y), (w, h) = launcherFocus()
except:
    alert(text='Please run the launcher and log in', title='Error', button='OK')
    quit()

liiguJaKliki('Play.png')
liiguJaKliki('TFT.png')
liiguJaKliki('Normal_HL.png')
liiguJaKliki('Confirm.png')
pyautogui.move(0, -50)
liiguJaKliki('FindMatch.png')
accept()

exit()