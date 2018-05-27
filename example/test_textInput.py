import os


def adb_keyboard_input(text):
    """
    adb keyboard app input unicode text
    :param text:
    :return:
    """
    cmd = 'adb shell am broadcast -a ADB_INPUT_TEXT --es msg {text}'.format(text=text.replace(' ', '%s'))
    os.system(cmd)


adb_keyboard_input('hello world')