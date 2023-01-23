from resources.Data import Dicts
from datetime import datetime
from logger_main import *


GROUP_1 = Dicts.GROUP_1
GROUP_2 = Dicts.GROUP_2
GROUP_3 = Dicts.GROUP_3

def choose_day():
    current_time = datetime.now().strftime("%H")
    current_day = datetime.today().weekday()
    if current_time == '00':
        if current_day != 0:
            return current_day - 1
        else:
            return 6
    else:
        return current_day

def get_time_zone(time=None):
    if time is None:
        time = datetime.now().strftime("%H")

    if time >= 21 or time == 0:
        return '21-1'
    else:
        ranges = map(lambda x: x.split('-'), Dicts.TYPE_1.keys())
        time_zone = '-'.join(list(filter(lambda x: time in range(int(x[0]), int(x[1])), ranges))[0])
        return time_zone


def inform(group: int):
    current_time = datetime.now().strftime("%H")
    right_border = get_time_zone().split('-')[1]
    difference = int(right_border) - int(current_time)
    next_condition = get_next_condition(group)
    if next_condition in ("Можливе Відключення", "Немає Енергії") and difference == 1:
        return True
    else:
        return False


def get_next_condition(group: int) -> str:
    time = int(datetime.now().strftime("%H"))
    day = choose_day()
    if group == 1:
        return GROUP_1[Dicts.WEEK_DAY[day]][get_time_zone(time + 4)]
    elif group == 2:
        return GROUP_2[Dicts.WEEK_DAY[day]][get_time_zone(time + 4)]
    else:
        return GROUP_3[Dicts.WEEK_DAY[day]][get_time_zone(time + 4)]



def get_condition(group: int) -> str:
    time = int(datetime.now().strftime("%H"))
    day = choose_day()
    time_zone = get_time_zone(time)
    if group == 1:
        return GROUP_1[Dicts.WEEK_DAY[day]][time_zone]
    elif group == 2:
        return GROUP_2[Dicts.WEEK_DAY[day]][time_zone]
    else:
        return GROUP_3[Dicts.WEEK_DAY[day]][time_zone]



def get_day_sсhedule(group: int) -> dict:
    day = choose_day()
    if group == 1:
        return GROUP_1[Dicts.WEEK_DAY[day]]
    elif group == 2:
        return GROUP_2[Dicts.WEEK_DAY[day]]
    else:
        return GROUP_3[Dicts.WEEK_DAY[day]]




