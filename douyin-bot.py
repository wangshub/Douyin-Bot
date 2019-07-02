# -*- coding: utf-8 -*-
import sys
import random
import time
from PIL import Image
import argparse

if sys.version_info.major != 3:
    print('Please run under Python3')
    exit(1)
try:
    from common import debug, config, screenshot, UnicodeStreamFilter
    from common.auto_adb import auto_adb
    from common import apiutil
    from common.compression import resize_image
except Exception as ex:
    print(ex)
    print('请将脚本放在项目根目录中运行')
    print('请检查项目根目录中的 common 文件夹是否存在')
    exit(1)

VERSION = "0.0.1"

# 我申请的 Key，随便用，嘻嘻嘻
# 申请地址 http://ai.qq.com
AppID = '1106858595'
AppKey = 'bNUNgOpY6AeeJjFu'

DEBUG_SWITCH = True
FACE_PATH = 'face/'

adb = auto_adb()
adb.test_device()
config = config.open_accordant_config()

# 审美标准
BEAUTY_THRESHOLD = 80

# 最小年龄
GIRL_MIN_AGE = 14


def yes_or_no():
    """
    检查是否已经为启动程序做好了准备
    """
    while True:
        yes_or_no = str(input('请确保手机打开了 ADB 并连接了电脑，'
                              '然后打开手机软件，确定开始？[y/n]:'))
        if yes_or_no == 'y':
            break
        elif yes_or_no == 'n':
            print('谢谢使用')
            exit(0)
        else:
            print('请重新输入')


def _random_bias(num):
    """
    random bias
    :param num:
    :return:
    """
    return random.randint(-num, num)


def next_page():
    """
    翻到下一页
    :return:
    """
    cmd = 'shell input swipe {x1} {y1} {x2} {y2} {duration}'.format(
        x1=config['center_point']['x'],
        y1=config['center_point']['y']+config['center_point']['ry'],
        x2=config['center_point']['x'],
        y2=config['center_point']['y'],
        duration=200
    )
    adb.run(cmd)
    time.sleep(1.5)


def follow_user():
    """
    关注用户
    :return:
    """
    cmd = 'shell input tap {x} {y}'.format(
        x=config['follow_bottom']['x'] + _random_bias(10),
        y=config['follow_bottom']['y'] + _random_bias(10)
    )
    adb.run(cmd)
    time.sleep(0.5)


def thumbs_up():
    """
    点赞
    :return:
    """
    cmd = 'shell input tap {x} {y}'.format(
        x=config['star_bottom']['x'] + _random_bias(10),
        y=config['star_bottom']['y'] + _random_bias(10)
    )
    adb.run(cmd)
    time.sleep(0.5)


def tap(x, y):
    cmd = 'shell input tap {x} {y}'.format(
        x=x + _random_bias(10),
        y=y + _random_bias(10)
    )
    adb.run(cmd)


def auto_reply():

    msg = "垆边人似月，皓腕凝霜雪。就在刚刚，我的心动了一下，小姐姐你好可爱呀_Powered_By_Python"

    # 点击右侧评论按钮
    tap(config['comment_bottom']['x'], config['comment_bottom']['y'])
    time.sleep(1)
    #弹出评论列表后点击输入评论框
    tap(config['comment_text']['x'], config['comment_text']['y'])
    time.sleep(1)
    #输入上面msg内容 ，注意要使用ADB keyboard  否则不能自动输入，参考： https://www.jianshu.com/p/2267adf15595
    cmd = 'shell am broadcast -a ADB_INPUT_TEXT --es msg {text}'.format(text=msg)
    adb.run(cmd)
    time.sleep(1)
    # 点击发送按钮
    tap(config['comment_send']['x'], config['comment_send']['y'])
    time.sleep(0.5)

    # 触发返回按钮, keyevent 4 对应安卓系统的返回键，参考KEY 对应按钮操作：  https://www.cnblogs.com/chengchengla1990/p/4515108.html
    cmd = 'shell input keyevent 4'
    adb.run(cmd)


def parser():
    ap = argparse.ArgumentParser()
    ap.add_argument("-r", "--reply", action='store_true',
                    help="auto reply")
    args = vars(ap.parse_args())
    return args


def main():
    """
    main
    :return:
    """
    print('程序版本号：{}'.format(VERSION))
    print('激活窗口并按 CONTROL + C 组合键退出')
    debug.dump_device_info()
    screenshot.check_screenshot()

    cmd_args = parser()

    while True:
        next_page()

        time.sleep(1)
        screenshot.pull_screenshot()

        resize_image('autojump.png', 'optimized.png', 1024*1024)

        with open('optimized.png', 'rb') as bin_data:
            image_data = bin_data.read()

        ai_obj = apiutil.AiPlat(AppID, AppKey)
        rsp = ai_obj.face_detectface(image_data, 0)

        major_total = 0
        minor_total = 0

        if rsp['ret'] == 0:
            beauty = 0
            for face in rsp['data']['face_list']:

                msg_log = '[INFO] gender: {gender} age: {age} expression: {expression} beauty: {beauty}'.format(
                    gender=face['gender'],
                    age=face['age'],
                    expression=face['expression'],
                    beauty=face['beauty'],
                )
                print(msg_log)
                face_area = (face['x'], face['y'], face['x']+face['width'], face['y']+face['height'])
                img = Image.open("optimized.png")
                cropped_img = img.crop(face_area).convert('RGB')
                cropped_img.save(FACE_PATH + face['face_id'] + '.png')
                # 性别判断
                if face['beauty'] > beauty and face['gender'] < 50:
                    beauty = face['beauty']

                if face['age'] > GIRL_MIN_AGE:
                    major_total += 1
                else:
                    minor_total += 1

            # 是个美人儿~关注点赞走一波
            if beauty > BEAUTY_THRESHOLD and major_total > minor_total:
                print('发现漂亮妹子！！！')
                thumbs_up()
                follow_user()

                if cmd_args['reply']:
                    auto_reply()

        else:
            print(rsp)
            continue


if __name__ == '__main__':
    try:
        # yes_or_no()
        main()
    except KeyboardInterrupt:
        adb.run('kill-server')
        print('谢谢使用')
        exit(0)
