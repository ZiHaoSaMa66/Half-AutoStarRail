import pyautogui
import pygetwindow as gw
import os
from datetime import datetime
from cnocr import CnOcr
import ctypes
import sys

mainpath = os.getcwd().replace("\\", "/")
screenshot_path = mainpath + '/screenshot.png'

debugmode = False

# CnOcr.set_caffe_logging_level("WARN")

def run_upto_admin():
    '''用于在非管理员运行时尝试提权'''
    logger.debug("检测管理员权限环境并尝试提权")
    if ctypes.windll.shell32.IsUserAnAdmin() == 0:
        logger.debug("尝试提权")
        ctypes.windll.shell32.ShellExecuteW(None,"runas",sys.executable,"".join(sys.argv),None,1)
        sys.exit()

class Logger():
    '''日志记录器'''
    global debugmode
    def __init__(self) -> None:
        pass
    def info(self,log:str):
        times = get_time_str()
        lognr = f"{times} > [INFO] {log}"
        print(lognr)
        savelog(lognr)

    def debug(self,log:str):
        global debugmode
        times = get_time_str()
        lognr = f"{times} > [DEBUG] {log}"
        savelog(lognr)
        if debugmode ==True:
            print(lognr)

    def warn(self,log:str):
        times = get_time_str()
        lognr = f"{times} > [WARN] {log}"
        print(lognr)
        savelog(lognr)
        pass
    def error(self,log:str):
        times = get_time_str()
        lognr = f"{times} > [ERR] {log}"
        print(lognr)
        savelog(lognr)
        pass
    def success(self,log:str):
        times = get_time_str()
        lognr = f"{times} > [SUCCESS] {log}"
        print(lognr)
        savelog(lognr)
        pass
    def ocr_debug(self,log:str):
        times = get_time_str()
        lognr = f"{times} > [OCR] {log}"
        if debugmode ==True:
            print(lognr)
            savelog(lognr)


logger = Logger()


def get_logfilename():
    time_str = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    return time_str


def get_time_str():
    '''返回一个时间字符串'''
    time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return time_str

logfilename = get_logfilename()
logpath = mainpath + "/" + logfilename + ".log"

def savelog(log:str):
    '''保存日志到日志文件中'''
    global logpath
    fm = open(logpath,"a") 
    # 模式 'a' 表示以追加（append）的方式打开文件，如果文件不存在则会创建文件。
    log += "\n"
    fm.write(log)
    fm.close()
    

def moveawaymose():
    '''把死人鼠标弄走'''
    pyautogui.click(819, 4)
    logger.debug("重置鼠标位置")

def getscreenshot():
    global game_x,game_y
    '''对现在的星铁窗口进行一次截图'''
    # 获取指定标题的窗口
    #sleep(3)
    moveawaymose()
    logger.info("尝试获取游戏画面")
    try:
        window = gw.getWindowsWithTitle('崩坏：星穹铁道')[0]
        # 对窗口进行截图
        screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
        #logger.info(f"debug -> {window.left},{window.top}, {window.width}, {window.height}")
        game_x = window.left + 8
        game_y = window.top
        logger.debug(f"截图获取到的gameX {game_x},gameY {game_y}")
        # 保存截图到文件
        str_p = mainpath + '\\screenshot.png'
        screenshot.save(str_p)
        logger.success("获取完成")
    except:
        logger.error("未检测到游戏窗口")
        # raise Exception("NoFindGame")

def mutp_get_cord(wordlist:list):
    '''提供需要识别的文字列表 对识别结果进行反复遍历\n
    返回识别结果列表,x偏移坐标列表,y偏移坐标列表'''
    global cord_status,xclist,yclist,game_x,game_y
    getscreenshot()
    cord_status = []
    xclist = []
    yclist = []
    logger.debug("开始进行多文本识别")

    ocr = CnOcr()
    ocr_result = ocr.ocr(screenshot_path)
    logger.ocr_debug(f"OCR_Res {ocr_result}")
    for loop_target in wordlist:
        find_status = mutp_get_cord_helper(loop_target,ocr_result)
        cord_status.append(find_status)
        
    return cord_status,xclist,yclist
                
def mutp_get_cord_helper(loop_target,ocr_result):
    global cord_status,xclist,yclist,game_x,game_y
    for result in ocr_result:
        if loop_target == result['text']:
            # 获取文字所在位置的坐标
            position = result['position']
            # 计算中心点坐标
            center_x = int((position[0][0] + position[1][0]) / 2)
            center_y = int((position[0][1] + position[2][1]) / 2)
            # 使用pyautogui进行点击
            center_x += game_x
            center_y += game_y
            logger.debug(f"点击坐标偏移量计算{center_x},{center_y}")
            
            xclist.append(center_x)
            yclist.append(center_y)
            return True
    xclist.append(None)
    yclist.append(None)
    return False
        
                
    


def getclicker(target:str):
    '''给定一个需要识别的文字进行识别并点击\n
    LiteVer使用CNOCR引擎'''
    global game_x,game_y
    getscreenshot()
    ocr = CnOcr()
    ocr_result = ocr.ocr(screenshot_path)
    logger.ocr_debug(f"{ocr_result}")
    for result in ocr_result:
        if target == result['text']:
            # 获取文字所在位置的坐标
            position = result['position']
            # 计算中心点坐标
            center_x = int((position[0][0] + position[1][0]) / 2)
            center_y = int((position[0][1] + position[2][1]) / 2)
            # 使用pyautogui进行点击
            center_x += game_x
            center_y += game_y
            logger.debug(f"点击坐标偏移量计算{center_x},{center_y}")
            pyautogui.click(center_x, center_y)
            
            break


def getclicker_with_status(target:str):
    '''给定一个需要识别的文字进行识别并点击\n
    最后返回点击状态'''
    global game_x,game_y
    getscreenshot()
    ocr = CnOcr()
    ocr_result = ocr.ocr(screenshot_path)
    logger.ocr_debug(f"{ocr_result}")
    for result in ocr_result:
        if target == result['text']:
            # 获取文字所在位置的坐标
            position = result['position']
            # 计算中心点坐标
            center_x = int((position[0][0] + position[1][0]) / 2)
            center_y = int((position[0][1] + position[2][1]) / 2)
            # 使用pyautogui进行点击
            center_x += game_x
            center_y += game_y
            logger.debug(f"点击坐标偏移量计算{center_x},{center_y}")
            pyautogui.click(center_x, center_y)
            return True
            break
    logger.debug(f"寻找的文字{target}不存在!!")
    return False
        
def getclicker_with_cord(target:str):
    '''给定一个需要识别的文字进行识别并点击\n
    最后返回偏移量坐标xy'''
    global game_x,game_y
    getscreenshot()
    ocr = CnOcr()
    ocr_result = ocr.ocr(screenshot_path)
    logger.ocr_debug(f"{ocr_result}")
    for result in ocr_result:
        if target == result['text']:
            # 获取文字所在位置的坐标
            position = result['position']
            # 计算中心点坐标
            center_x = int((position[0][0] + position[1][0]) / 2)
            center_y = int((position[0][1] + position[2][1]) / 2)
            # 使用pyautogui进行点击
            center_x += game_x
            center_y += game_y
            logger.debug(f"点击坐标偏移量计算{center_x},{center_y}")
            pyautogui.click(center_x, center_y)
            return center_x, center_y
            break


def check_str_with_cord(target:str):
    '''给定一个需要识别的文字进行识别\n
    返回是否存在文字,文字X,Y坐标'''
    global game_x,game_y
    getscreenshot()
    ocr = CnOcr()
    ocr_result = ocr.ocr(screenshot_path)
    logger.ocr_debug(f"{ocr_result}")
    for result in ocr_result:
        if target == result['text']:
            # 获取文字所在位置的坐标
            position = result['position']
            # 计算中心点坐标
            center_x = int((position[0][0] + position[1][0]) / 2)
            center_y = int((position[0][1] + position[2][1]) / 2)
            # 使用pyautogui进行点击
            center_x += game_x
            center_y += game_y
            logger.debug(f"坐标偏移量计算{center_x},{center_y}")
            return True,center_x,center_y
    logger.debug(f"寻找的文字{target}不存在!!")
    return False,None,None

def check_str(target:str):
    '''给定一个需要识别的文字进行识别\n
    返回是否存在文字'''
    getscreenshot()
    ocr = CnOcr()
    ocr_result = ocr.ocr(screenshot_path)
    logger.ocr_debug(f"OCR_Res {ocr_result}")
    for result in ocr_result:
        if target == result['text']:
            logger.debug(f"寻找的文字{target}存在")
            return True
    logger.debug(f"寻找的文字{target}不存在!!")
    return False

