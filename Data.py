class Dicts:
    SCHEDULE_1 = '1group.png'
    SCHEDULE_2 = '2group.png'
    SCHEDULE_3 = '3group.png'
    PICTURE_1 = 'night_lviv.jpg'
    PICTURE_2 = 'lights.jpg'

    TYPE_1 = {'1-5': 'Можливе Відключення',
              '5-9': 'Немає Енергії',
              '9-13': 'Є Енергія',
              '13-17': 'Можливе Відключення',
              '17-21': 'Немає Енергії',
              '21-1': 'Є Енергія'}

    TYPE_2 = {'1-5': 'Немає Енергії',
              '5-9': 'Є Світло',
              '9-13': 'Можливе Відкючення',
              '13-17': 'Немає Енергії',
              '17-21': 'Є Енергія',
              '21-1': 'Можливе Відключення'}

    TYPE_3 = {'1-5': 'Є Енергія',
              '5-9': 'Можливе Відключення',
              '9-13': 'Немає Енергії',
              '13-17': 'Є Енергія',
              '17-21': 'Можливе Відключення',
              '21-1': 'Немає Енергії'}

    GROUP_1 = {'Понеділок': TYPE_2,
               'Вівторок': TYPE_3,
               'Середа': TYPE_1,
               'Четвер': TYPE_2,
               "П'ятниця": TYPE_3,
               'Субота': TYPE_1,
               'Неділя': TYPE_2}

    GROUP_2 = {'Понеділок': TYPE_3,
               'Вівторок': TYPE_1,
               'Середа': TYPE_2,
               'Четвер': TYPE_3,
               "П'ятниця": TYPE_1,
               'Субота': TYPE_2,
               'Неділя': TYPE_3}

    GROUP_3 = {'Понеділок': TYPE_1,
               'Вівторок': TYPE_2,
               'Середа': TYPE_3,
               'Четвер': TYPE_1,
               "П'ятниця": TYPE_2,
               'Субота': TYPE_3,
               'Неділя': TYPE_1}


    WEEK_DAY = {0: 'Понеділок',
                1: 'Вівторок',
                2: 'Середа',
                3: 'Четвер',
                4: "П'ятниця",
                5: 'Субота',
                6: 'Неділя'}

