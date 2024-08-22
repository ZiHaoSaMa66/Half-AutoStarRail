from lib.Script import run_upto_admin
run_upto_admin()


from lib.Script import *
from time import sleep
from datetime import datetime

without_Tips = True
skip_into_fight_wait = False



def main_start_shuaben(goal:int):
    '''开始刷本的主要逻辑函数'''
    save_left_LoopCount(goal)
    
    print("请对本次副本队伍进行配置")
    
    if not without_Tips:
        print("请尽量保证刷本过程中因练度不足或奶量不足")
        print("导致的刷本循环中出现失败情况")
        print("(问就是还没开始写出现失败情况的处理方式)")
        print("此时请不要移动游戏窗口或遮挡挑战按钮")
        
    input("配置完毕请敲击回车开始")
    cx,cy = lowjd_getclicker_with_cord("挑战")
    
    pyautogui.click(cx,cy)
    formal_part(goal)
    
    os.system("cls")
    logger.success("本次循环自动化完成")



def formal_part(goaltznum:int):
    global game_x,game_y
    '''正式进行刷本'''
    if not skip_into_fight_wait:
        logger.info("等待进入副本战斗...")
        sleep(10)

    leftcheck = 30
    pyautogui.press('v')
    print("若程序关闭了你的自动战斗请手动开回来plz\n")
    logger.info("战斗开始")
    
    start_time = datetime.now()
    
    while True: #当剩余刷本次数未等于0时继续循环
        
        while leftcheck>0: #当等待检查运行状态剩余时间未小于0时继续循环
            sleep(1)
            
            now_time = datetime.now()
            # 计算时间差
            time_difference = now_time - start_time
            total_seconds = int(time_difference.total_seconds())
            # 计算小时、分钟和秒钟
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            leftcheck -= 1
            os.system("cls")
            print("\n")
            print(f"总循环已经运行 > {hours:02}:{minutes:02}:{seconds:02} <")
            print(f"当前剩余循环 {goaltznum} 次")
            print(f"距离下一次检测状态剩 {leftcheck} sec")
            print("\n")
            
        
        checkwordlist = ["战斗失败","再来一次","退出关卡"]
        os.system("cls")
        logger.info("开始进行副本通关状态检测 请等待..")
        if goaltznum ==1:
            # exit = getclicker_with_status() #并尝试退出副本
            
            cstatus,xlist,ylist=mutp_get_cord(checkwordlist)
            
            # exit_checker,ex,ey = check_str_with_cord("退出关卡")
            if cstatus[0]==True:
                logger.warn("挑战失败... 请手动重启循环")
                save_left_LoopCount(1)
                break
            
            elif cstatus[1]==False:
                logger.success("未检测到副本通关 继续等待")
                leftcheck = 30
                
            elif cstatus[2]==True:
                pyautogui.click(xlist[2],ylist[2])
                save_left_LoopCount(0)
                break
            
        elif goaltznum >1:
            # ctn,cx,cy = check_str_with_cord("再来一次") #检测是否完成挑战出现再次挑战按钮
            cstatus,xlist,ylist=mutp_get_cord(checkwordlist)
            if cstatus[1] ==True: #如果为是 代表按钮出现 副本完成 并进行点击一次
                goaltznum -=1
                leftcheck = 25
                
                save_left_LoopCount(goaltznum)
                
                pyautogui.click(xlist[1],ylist[1])
                sleep(3)
                logger.info("开始检测体力状态")
                checker = CheckPow_v2()
                if checker ==False:
                    #如果有弹窗无体力可补充则强制进行退出
                    logger.warn("当前已经没有多余的后备开拓力")
                    logger.info("将强制结束循环")
                    getclicker("取消") #点击取消键
                    sleep(3)
                    getclicker("退出关卡") #并尝试退出副本
                    
                    break
                else:
                    logger.success("体力状态检测完成")
                    pass
            elif cstatus[0]==True:
                logger.warn("挑战失败... 请手动重启循环")
                break
            elif cstatus[1]==False:
                logger.success("未检测到副本通关 继续等待")
                leftcheck = 35

        
def CheckPow_v2():
    '''检查是否有体力补充窗口并自动补充体力\n
    返回None 无弹窗\n
    返回False 有弹窗 无体力可补充\n
    返回True 有弹窗,已经成功补充体力'''
    
    have_hou_bei_kai_tuo_li = check_str("取出等量后备开拓力")
    if have_hou_bei_kai_tuo_li ==True:
        lowjd_getclicker("确认")
        sleep(3)
        # pyautogui.click(x,y)
        lowjd_getclicker("确认")
        
        sleep(1.5)
        
        lowjd_getclicker("点击空白处关闭")
        
        sleep(2)
        
        _ctn = getclicker_with_status("再来一次")#此时再尝试点击继续挑战按钮
        
        sleep(3)
        
        have_tan_chuang = check_str("开拓力补充")
        if have_tan_chuang ==True:
            return False
        else:
            return True

    else:
        return None
    
os.system("cls")

print("----------------------------------------------")
print("半-自动 星穹铁道 重构版")
print("Re:Half-Auto StarRail Beta 1.2")
print("Powered by ZiHao with love")
print("----------------------------------------------")

if not without_Tips:
    print("请确保目前已经选择好需要刷的任意副本")
    print("包括难度等级 单次循环挑战次数")
    print("如果程序在上一轮循环中崩溃了你可以尝试键入 last ")
    print("")
while True:
    try:
        skip_into_fight_wait = False
        
        goalnum = input("请输入需要的循环次数 >")
        
        if goalnum == 'last':
            
            Last_lpnum = read_left_LoopCount()
            if Last_lpnum == 0:
                logger.warn("你还没有进行过任何循环或上一次循环已完成")
                raise Exception("NoLastLoop")
            
            goalnum = Last_lpnum
            logger.info(f"已读取上一次剩余循环次数 {goalnum}")
            skip_into_fight_wait = True
            
        elif int(goalnum) <=0:
            logger.error("循环次数不能小于或等于0")
            
            raise Exception("LoopNumError")

        
        
        main_start_shuaben(int(goalnum))
        os.system("cls")
    except Exception as e:
        if not without_Tips:
            print("啊哦?输入的数值是不是有问题呢?")
            print("如果你坚信这是一个错误 请反馈")
        logger.error(f"{e} at input lpnum")
