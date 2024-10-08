import pyautogui
from time import sleep, time
import os
import sys
import json
import random
from itertools import repeat
import configparser



# make sure to place the resource rooms correctly for collections
# you must have two characters in your account
# start script with py -u ./bot/playpback.py ./bot/config.ini
# define parameters in config.ini
# tested on python 3.12
def main():
    change, rss = read_config(sys.argv[1])
    index = 0
    initializePyAutoGUI()
    countdownTimer() 
    # running forever
    while True:
        # collect, recruit, help, rally and gather
        do_all(rss)
        # switch to the other character in this account
        switch_char()
        countdownTimerMins(3)
        # collect, recruit, help, rally and gather
        do_all(rss)
        # if you defined the change array, change account.
        if change:
            change_acc(change[index])
            index += 1
            if index >= len(change):
                index = 0
        else:
            # otherwise switch back to the other character and start again
            switch_char()
        countdownTimerMins(3)
    
    print("Done")


def do_alliance():
    path = 'alliance/'
    if checkColor(528, 984) == (217, 72, 71):
        playActions(path + 'enter.json')
        sleep(2)
        if checkColor(1473, 636) == (201, 53, 54):
            playActions(path + 'tech_enter.json')
            sleep(1)
            if checkColor(631, 777) == (239, 78, 80):
                playActions(path + 'tech_donate.json')
                sleep(1)
                if checkColor(1848, 971) == (38, 64, 112):
                    playActions(path + 'tech_donate_do.json')
                playActions("general/cancel.json")
            playActions("general/cancel.json")
        sleep(1)
        if checkColor(1469, 778) == (201, 53, 54):
            playActions(path + 'gift_enter.json')
            sleep(1)
            if checkColor(1769, 271) == (38, 65, 111):
                playActions(path + 'gift_claim_all.json')
                playActions('general/wakeup.json')
                sleep(1)
            playActions(path + 'gift_second_enter.json')
            sleep(1)
            while checkColor(1769, 271) == (38, 65, 111):
                playActions(path + 'gift_claim.json')
                playActions('general/wakeup.json')
                sleep(1)
            playActions(path + 'gift_cancel.json')
            sleep(1)
        playActions(path + 'daily_rewards.json')
        sleep(2)
        playActions("general/cancel.json")
        sleep(2)

def read_config(config_file_name):
    config = configparser.ConfigParser()
    config.read(config_file_name)
    change = []
    if 'Accounts' in config and 'change' in config['Accounts']:
        change = config['Accounts']['change']
    if 'Resources' in config:
        rss_array = []
        rss_array.extend(repeat('gp', int(config['Resources']['gp'])))
        rss_array.extend(repeat('iron', int(config['Resources']['iron'])))
        rss_array.extend(repeat('wood', int(config['Resources']['wood'])))
        rss_array.extend(repeat('food', int(config['Resources']['food'])))
        rss = {
            'array': rss_array,
            'level': int(config['Resources']['level'])
        }
    else:
        raise BaseException()
    return change, rss

# collect rss, recruit if free, help members if no rally, rally if rally available and you have enough ap (only the first one), send all marches gathering
def do_all(rss):
    if checkColor(977, 531) not in [(0, 0, 0), (1, 1, 1)]:
        playActions('general/exit_enter_castle.json')
        sleep(2.00)
    collect()
    do_alliance()
    recruit()
    help()
    # rally()
    success = True
    while success:
        success = gather(rss)

def change_acc(name):
    path = 'change/'
    playActions(path + "logout1.json")
    countdownTimerMins(1)
    playActions(path + "logout2.json")
    sleep(10)
    playActions(path + f"login_{name}.json")
    countdownTimerMins(3)
    ad_check()

def help():
    path = 'help/'
    if checkColor(1476, 913) == (99, 255, 71):
        playActions(path + "help.json")
    elif checkColor(1366, 906) == (99, 255, 71):
        playActions(path + "help2.json")

def rally():
    path = 'rally/'
    if checkColor(1460, 914) == (255, 77, 74) and checkColor(237, 136) == (42, 208, 151):
        playActions(path + "open.json")
        sleep(2.00)
        if checkColor(1439, 357) == (28, 135, 145):
            playActions(path + "add_to.json")
            sleep(1.00)
            if checkColor(1370, 307) == (231, 220, 184):
                playActions(path + "march.json")
            else:
                playActions('general/cancel.json')
        else:
            playActions(path + "exit.json")



def recruit():
    path = 'recruit/'
    if checkColor(1078, 998) == (247, 66, 66):
        playActions(path + "recruit.json")
        sleep(2.00)
        if checkColor(1747, 729) == (247, 66, 66):
            playActions(path + "recruit_click.json")
        playActions(path + "recruit_adv.json")
        sleep(2.00)
        if checkColor(1747, 729) == (247, 66, 66):
            playActions(path + "recruit_click.json")
        playActions("general/cancel.json")
        sleep(2.00)

def switch_char():
    path = 'switch/'
    playActions(path + 'switch_char_pre.json')
    sleep(2.00)
    if checkColor(1602, 158) in [(55, 201, 40), (55, 199, 42)]:
        playActions(path + "switch_char_1.json")
    else:
        playActions(path + "switch_char_2.json")
    countdownTimerMins(2)
    success = ad_check()
    while success:
        success = ad_check()


def ad_check():
    success = False
    if checkColor(1806, 113) == (246, 245, 245) or checkColor(1825, 101) == (246, 245, 245):
        playActions("general/remove_ad.json")
        success = True
    elif checkColor(1839, 73) == (246, 245, 245) or checkColor(1854, 101) == (246, 245, 245):
        playActions("general/remove_ad_2.json")
        success = True
    elif checkColor(1772, 128) == (246, 245, 245) or checkColor(1771, 126) == (246, 245, 245):
        playActions("general/remove_ad_3.json")
        success = True
    sleep(3.00)
    playActions("general/wakeup.json")
    return success

def collect():
    path = 'collect/'
    #for jluke
    while checkColor(957, 229) in [(243, 234, 210), (243, 233, 208)] or checkColor(923, 212) in [(247, 241, 222), (247, 241, 221)]:
        playActions(path + "collect_all.json")
        sleep(5.00)
        if checkColor(1501, 965) in [(41, 77, 135)]:
            playActions(path + "speed_up.json")
    if checkColor(773,345) in [(253, 251, 239), (252, 251, 239), (255, 251, 239)]:
        playActions(path + "collect_1.json")
        sleep(1.00)
    if checkColor(1165,345) in [(253, 251, 239), (255, 251, 239)]:
        playActions(path + "collect_2.json")
        sleep(1.00)
    if checkColor(1165,597) in [(253, 251, 239), (255, 251, 239)]:
        playActions(path + "collect_3.json")
        sleep(1.00)
    if checkColor(773,597) in [(253, 251, 239), (255, 251, 239)]:
        playActions(path + "collect_4.json")
        sleep(1.00)
    playActions('general/exit_enter_castle.json')
    sleep(2.00)

def gather(rss):
    path = 'gather/'
    rss_type = rss['array'][int(random.random() * len(rss['array']))]
    rss_level = rss['level']
    file_name = f'gather{rss_level}_{rss_type}.json'
    playActions(path + file_name)
    sleep(2.00)
    if checkColor(387, 827) == (236, 224, 186):
        playActions(path + "gather_left.json")
    else:
        playActions(path + "gather_right.json")
    sleep(1.50)
    if checkColor(1494, 325) == (236, 224, 186):
        playActions(path + "gather_finish.json")
        sleep(2.00)
        return True
    else:
        playActions("general/cancel.json")
        sleep(2.00)
        return False
    

def checkColor(x, y):
    im = pyautogui.screenshot()
    print(im.getpixel((x, y)))
    return(im.getpixel((x, y)))


def initializePyAutoGUI():
    # Initialized PyAutoGUI
    # https://pyautogui.readthedocs.io/en/latest/introduction.html
    # When fail-safe mode is True, moving the mouse to the upper-left corner will abort your program.
    pyautogui.FAILSAFE = True


def countdownTimer():
    # Countdown timer
    print("Starting", end="", flush=True)
    for i in range(0, 10):
        print(".", end="", flush=True)
        sleep(1)
    print("Go")

def countdownTimerMins(mins):
    # Countdown timer
    print(f"Waiting {mins} Minuten:", flush=True)
    for i in range(0, mins * 6):
        if i % 6 == 0:
            print(f"{i / 6 + 1}. Minute\n", flush=True)
        else:
            print(f".", end="", flush=True)
        sleep(10)
    pyautogui.moveTo(int(random.random() * 1000 + 1), 100, duration=0.25)
    sleep(5.0)
    print("Go")

def playActions(filename):
    # Read the file
    script_dir = os.path.dirname(__file__)
    filepath = os.path.join(
        script_dir, 
        'recordings', 
        filename
    )
    with open(filepath, 'r') as jsonfile:
        # parse the json
        data = json.load(jsonfile)
        
        # loop over each action
        # Because we are not waiting any time before executing the first action, any delay before the initial
        # action is recorded will not be reflected in the playback.
        for index, action in enumerate(data):
            action_start_time = time()

            # look for escape input to exit
            if action['button'] == 'Key.esc':
                break

            # perform the action
            if action['type'] == 'keyDown':
                key = convertKey(action['button'])
                pyautogui.keyDown(key)
                print("keyDown on {}".format(key))
            elif action['type'] == 'keyUp':
                key = convertKey(action['button'])
                pyautogui.keyUp(key)
                print("keyUp on {}".format(key))
            elif action['type'] == 'click':
                pyautogui.click(action['pos'][0], action['pos'][1], duration=0.25)
                print("click on {}".format(action['pos']))
            elif action['type'] == 'move':
                pyautogui.moveTo(action['pos'][0], action['pos'][1], duration=0.25)
                print("move to {}".format(action['pos']))

            # then sleep until next action should occur
            try:
                next_action = data[index + 1]
            except IndexError:
                # this was the last action in the list
                break
            elapsed_time = next_action['time'] - action['time']

            # if elapsed_time is negative, that means our actions are not ordered correctly. throw an error
            if elapsed_time < 0:
                raise Exception('Unexpected action ordering.')

            # adjust elapsed_time to account for our code taking time to run
            elapsed_time -= (time() - action_start_time)
            if elapsed_time < 0:
                elapsed_time = 0
            print('sleeping for {}'.format(elapsed_time))
            sleep(elapsed_time)


# convert pynput button keys into pyautogui keys
# https://pynput.readthedocs.io/en/latest/_modules/pynput/keyboard/_base.html#Key
# https://pyautogui.readthedocs.io/en/latest/keyboard.html
def convertKey(button):
    PYNPUT_SPECIAL_CASE_MAP = {
        'alt_l': 'altleft',
        'alt_r': 'altright',
        'alt_gr': 'altright',
        'caps_lock': 'capslock',
        'ctrl_l': 'ctrlleft',
        'ctrl_r': 'ctrlright',
        'page_down': 'pagedown',
        'page_up': 'pageup',
        'shift_l': 'shiftleft',
        'shift_r': 'shiftright',
        'num_lock': 'numlock',
        'print_screen': 'printscreen',
        'scroll_lock': 'scrolllock',
    }

    # example: 'Key.F9' should return 'F9', 'w' should return as 'w'
    cleaned_key = button.replace('Key.', '')

    if cleaned_key in PYNPUT_SPECIAL_CASE_MAP:
        return PYNPUT_SPECIAL_CASE_MAP[cleaned_key]

    return cleaned_key


if __name__ == "__main__":
    main()
