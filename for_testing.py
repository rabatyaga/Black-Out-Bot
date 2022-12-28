from Data import Dicts
from datetime import datetime

class Electricity:
    current_time = datetime.now().strftime("%H")
    current_day = datetime.today().weekday()

    GROUP_1 = Dicts.GROUP_1
    GROUP_2 = Dicts.GROUP_2
    GROUP_3 = Dicts.GROUP_3

    def __init__(self, time=current_time):
        self.time = time

    def get_time_zone(self):
        if int(self.time) >= 21 or int(self.time) == 0:
            return '21-1'
        else:
            ranges = map(lambda x: x.split('-'), Dicts.TYPE_1.keys())
            return '-'.join(list(filter(lambda x: int(self.current_time) in range(int(x[0]), int(x[1])), ranges))[0])

    def inform(self, current_condition):
        self.current_condition = current_condition
        right_border = self.get_time_zone().split('-')[1]
        difference = int(right_border) - int(self.current_time)
        if self.current_condition in ("Можливе Відключення", "Є Енергія") and difference == 1:
            return True
        else:
            return False



    def get_condition(self, group, day=current_day):
        self.day = day
        self.group = group
        if self.group == 1:
            return self.GROUP_1[Dicts.WEEK_DAY[self.day]][self.get_time_zone()]
        elif self.group == 2:
            return self.GROUP_2[Dicts.WEEK_DAY[self.day]][self.get_time_zone()]
        else:
            return self.GROUP_3[Dicts.WEEK_DAY[self.day]][self.get_time_zone()]

    def get_day_sсhedule(self, group, day=current_day):
        self.day = day
        self.group = group
        if self.group == 1:
            return self.GROUP_1[Dicts.WEEK_DAY[self.day]]
        elif self.group == 2:
            return self.GROUP_2[Dicts.WEEK_DAY[self.day]]
        else:
            return self.GROUP_3[Dicts.WEEK_DAY[self.day]]


print(Electricity().get_condition(1))
