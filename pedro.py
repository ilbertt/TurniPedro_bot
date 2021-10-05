from datetime import datetime, timedelta

'''
SHIFTS:
M=morning
A=afternoon
N=night
_=home

|M|M|A|A|N|N|_|_|_|_|M|M|A|A|N|N|_|_|_|

TOT: 19 days
'''
shift_array = [
    '🔨 *7 - 15*',
    '🔨 *7 - 15*',
    '🔨 *15 - 23*',
    '🔨 *15 - 23*',
    '🔨 *23 - 7*',
    '🔨 *23 - 7*',
    '🏠',
    '🏠',
    '🏠',
    '🏠',
    '🔨 *7 - 15*',
    '🔨 *7 - 15*',
    '🔨 *15 - 23*',
    '🔨 *15 - 23*',
    '🔨 *23 - 7*',
    '🔨 *23 - 7*',
    '🏠',
    '🏠',
    '🏠',
]

italian_days = ['Dom', 'Lun', 'Mar', 'Mer', 'Gio', 'Ven', 'Sab']

class Pedro:
    def __init__(self, start=None):
        if start != None:
            self.start = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
            with open('start.txt', 'w') as start_file:
                start_file.write(str(self.start))
        else:
            with open('start.txt', 'r') as start_file:
                self.start = datetime.strptime(start_file.readline(), '%Y-%m-%d %H:%M:%S')
    
    def set_shift_start(self, date):
        self.start = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        with open('start.txt', 'w') as start_file:
            start_file.write(str(self.start))
        return self.start

    def tell_shift(self, day):
        '''
        SHIFTS:
        M=morning
        A=afternoon
        N=night
        _=home
        
        |M|M|A|A|N|N|_|_|_|_|M|M|A|A|N|N|_|_|_|

        TOT: 19 days
        '''
        if day == 'oggi':
            date = datetime.today()
        elif day == 'domani':
            date = datetime.today() + timedelta(1)
        delta = date - self.start
        next_shift = ''
        end_shift = ''
        delta_days = delta.days % 19

        print(delta_days)

        if delta_days in [0,1,10,11]:
            #print('adesso lavora al turno di mattina')
            shift = '*mattina*'
            end_shift = 'dalle *7* alle *15*'

            if delta_days in [0,10]:
                next_shift = 'lavora di mattina, dalle *7* alle *15*'
            else:
                next_shift = 'lavora di pomeriggio, dalle *15* alle *23*'
        elif delta_days in [2,3,12,13]:
            #print(day+' lavora al turno di sera')
            shift = '*pomeriggio*'
            end_shift = 'dalle *15* alle *23*'
            
            if delta_days in [2,12]:
                next_shift = 'lavora di *pomeriggio*, dalle *15* alle *23*'
            else:
                next_shift = 'lavora di *notte*, delle *23* alle *7* del mattino dopo'
        elif delta_days in [4,5,14,15]:
            #print(day+' lavora al turno di notte')
            shift = '*notte*'
            end_shift = 'dalle *23* alle *7*'
            
            if delta_days in [4,14]:
                next_shift = 'lavora di *notte*, delle *23* alle *7* del mattino dopo'
            else:
                next_shift = 'è a casa'
        elif delta_days in [6,7,8,9,16,17,18]:
            #print(day+' non lavora')
            shift = 'none'
            if delta_days in [6,7,8,16,17]:
                next_shift = 'è a casa'
            else:
                next_shift = 'lavora di *mattina*, dalle *7* alle *15*'
        return self.format_response(day, shift, end_shift, next_shift)

    def format_response(self, day, shift, end_shift, next_shift):
        resp_this_shift = ''
        end_this_shift = ''
        resp_next_shift = ''
        #OGGI lavora di _mattina_, _finisce alle 15_
        #DOMANI _inizia alle 15_
        if shift=='none':
            resp_this_shift = '*non lavora*'
        else:
            resp_this_shift = 'lavora di '+shift
        
        if end_shift != '':
            resp_this_shift += ', '+end_shift

        if day == 'oggi':
            resp_this_shift = '_Oggi_ '+resp_this_shift
            resp_next_shift += '_Domani_ '+next_shift
        if day == 'domani':
            resp_this_shift = '_Domani_ '+resp_this_shift
            resp_next_shift += '_Dopodomani_ '+next_shift
        
        return resp_this_shift + '\n' + resp_next_shift

    def all_shift(self):
        '''
        SHIFTS:
        M=morning
        A=afternoon
        N=night
        _=home
        
        |M|M|A|A|N|N|_|_|_|_|M|M|A|A|N|N|_|_|_|

        TOT: 19 days
        '''
        
        resp = ''
        t = datetime.today()
        for i in range(7):
            increment = t + timedelta(i)
            delta = increment - self.start
            delta_days = delta.days % 19
            resp = resp + '_' + italian_days[int(increment.strftime("%w"))] + '_ ' + increment.strftime("%d/%m") + ': ' + shift_array[delta_days] + '\n'

        return resp
    
    def dio(self):
        return 'dio non esiste, ma se esiste è un *sadico di merda*'
    
    def grigliata(self):
        return "Domani sera grigliata da Pedro, offre lui."

    def university_day(self, day):
        """
        Day of the week
        Monday 0
        Tuesday 1
        Wednesday 2
        Thursday 3
        Friday 4
        Saturday 5
        Sunday 6
        """
        if day == 'oggi':
            date = datetime.today().weekday()
        elif day == 'domani':
            date = datetime.today().weekday() + 1
        import pandas as pd
        schedule=pd.read_excel('orariuni.xlsx')
        
        out = "\nLezioni di oggi:\n"
        if date == 5 or date == 6:
            return "Non ha lezioni nel weekend"
        for i in range(len(schedule.iloc[1:, date+1])):
            if schedule.iloc[i, date+1] != "free":
                out += (schedule.time[i] + "\t"+ schedule.iloc[i, date+1] + "\n")
        return out 



