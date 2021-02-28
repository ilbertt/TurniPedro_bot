from datetime import datetime, timedelta
import telepot
from telepot.aio.loop import MessageLoop
from telepot.aio.delegate import pave_event_space, per_chat_id, create_open
import asyncio

START = datetime(2021,1,17,7,0,0)

def tell_shift(day, date):
    with open('start.txt', 'r') as start_file:
        START = datetime.strptime(start_file.readline(), '%Y-%m-%d %H:%M:%S')
    delta = date - START
    next_shift = ''
    end_shift = ''
    delta_days = delta.days%8

    if delta_days in [0,1]:
        #print('adesso lavora al turno di mattina')
        shift = '*mattina*'
        end_shift = 'dalle *7* alle *15*'

        if delta_days==0:
            next_shift = 'lavora di mattina, dalle *7* alle *15*'
        else:
            next_shift = 'lavora di pomeriggio, dalle *15* alle *23*'
    elif delta_days in [2,3]:
        #print(day+' lavora al turno di sera')
        shift = '*pomeriggio*'
        end_shift = 'dalle *15* alle *23*'
        
        if delta_days==2:
            next_shift = 'lavora di *pomeriggio*, dalle *15* alle *23*'
        else:
            next_shift = 'lavora di *notte*, delle *23* alle *7* del mattino dopo'
    elif delta_days in [4,5]:
        #print(day+' lavora al turno di notte')
        shift = '*notte*'
        end_shift = 'dalle *23* alle *7*'
        
        if delta_days==4:
            next_shift = 'lavora di *notte*, delle *23* alle *7* del mattino dopo'
        else:
            next_shift = 'è a casa'
    elif delta_days in [6,7]:
        #print(day+' non lavora')
        shift = 'none'
        if delta_days==6:
            next_shift = 'è a casa'
        else:
            next_shift = 'lavora di *mattina*, dalle *7* alle *15*'
    return format_response(day, shift, end_shift, next_shift)

def format_response(day, shift, end_shift, next_shift):
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

class MessageHandler(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(MessageHandler, self).__init__(*args, **kwargs)
        self._count = 0

    async def on_chat_message(self, msg):
        print('handling message #', self._count)
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type == 'text' : 
            chatInfo = await bot.getChat(chat_id)
            try: 
                print('From user:', chatInfo['username'])
            except Exception as e:
                print('From user without username')
            text = msg['text'].lower().strip()
            if '/start' in text : 
                try:
                    nome = chatInfo['first_name']
                except Exception as e:
                    nome = ''
                await self.sender.sendMessage('Ciao '+nome+'!\nBenvenuto in Turni Pedro, ora non ha più scampo!')
            else:
                #shift_explain = 'non so rispondere'
                if 'oggi' in text:
                    t = datetime.today()
                    shift_explain = tell_shift('oggi', t)
                    await self.sender.sendMessage(shift_explain, parse_mode='markdown')
                elif 'domani' in text:
                    t = datetime.today()
                    t = t + timedelta(1)
                    shift_explain = tell_shift('domani', t)
                    await self.sender.sendMessage(shift_explain, parse_mode='markdown')
                elif ' dio ' or '/dio' in text:
                    await self.sender.sendMessage('dio non esiste, ma se esiste è un sadico di merda')
                elif 'start' in text:
                    if chatInfo['username'] == 'ilbert98':
                        try:
                            t = text[5:].strip()    # remoce 'start' from string, keep only the date
                            t += ' 07:00:00'
                            START = datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
                            with open('start.txt', 'w') as start_file:
                                start_file.write(str(START))
                            await self.sender.sendMessage('Inizio impostato per il '+str(START))
                        except Exception as e:
                            print('ERROR', e)
                            await self.sender.sendMessage("C'è stato un errore:\n"+str(e))
                        return
                    await self.sender.sendMessage('Non hai le autorizzazioni per impostare il giorno iniziale')
        self._count += 1

with open('token.txt', 'r') as token_file:
    TOKEN = token_file.readline()

bot = telepot.aio.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, MessageHandler, timeout=10),
])

loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot).run_forever())
print('Listening ...')

loop.run_forever()
