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
    if delta.days in [0,1] or delta.days%8==0 or delta.days%9==0:
        #print('adesso lavora al turno di mattina')
        if delta.seconds <= 28800:
            shift = 'mattina'
            end_shift = 'finisce alle 15'
        else:
            shift = 'none'
        if delta.days==0 or delta.days%8==0:
            next_shift = 'inizia alle 7, finisce alle 15'
        else:
            next_shift = 'inizia alle 15, finisce alle 23'
    elif delta.days in [2,3] or delta.days%10==0 or delta.days%11==0:
        #print(day+' lavora al turno di sera')
        if delta.seconds > 28800 and delta.seconds <= 57600:
            shift = 'pomeriggio'
            end_shift = 'finisce alle 23'
        else:
            shift = 'none'
        if delta.days==2 or delta.days%10==0:
            next_shift = 'inizia alle 15, finisce alle 23'
        else:
            next_shift = 'inizia alle 23, finisce alle 7 del mattino dopo'
    elif delta.days in [4,5] or delta.days%12==0 or delta.days%13==0:
        #print(day+' lavora al turno di notte')
        if delta.seconds > 57600 and delta.seconds <= 86399:
            shift = 'night'
            end_shift = 'finisce alle 15'
        else:
            shift = 'none'
        if delta.days==4 or delta.days%12==0:
            next_shift = 'inizia alle 23, finisce alle 7 del mattino dopo'
        else:
            next_shift = 'è a casa'
    elif delta.days in [6,7] or delta.days%14==0 or delta.days%15==0:
        #print(day+' non lavora')
        shift = 'none'
        if delta.days==6 or delta.days%14==0:
            next_shift = 'è a casa'
        else:
            next_shift = 'inizia alle 7, finisce alle 15'
    return format_response(day, shift, end_shift, next_shift)

def format_response(day, shift, end_shift, next_shift):
    resp_this_shift = ''
    end_this_shift = ''
    resp_next_shift = ''
    #OGGI lavora di _mattina_, _finisce alle 15_
    #DOMANI _inizia alle 15_
    if shift=='none':
        resp_this_shift = 'non lavora'
    else:
        resp_this_shift = 'lavora di '+shift
    
    if end_shift != '':
        resp_this_shift += ', '+end_shift

    if day == 'oggi':
        resp_this_shift = 'Oggi '+resp_this_shift
        resp_next_shift += 'Domani '+next_shift
    if day == 'domani':
        resp_this_shift = 'Domani '+resp_this_shift
        resp_next_shift += 'Dopodomani '+next_shift
    
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
            print(chatInfo)
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
                    await self.sender.sendMessage(shift_explain)
                elif 'domani' in text:
                    t = datetime.today()
                    t = t + timedelta(1)
                    shift_explain = tell_shift('domani', t)
                    await self.sender.sendMessage(shift_explain)
                elif 'dio' in text:
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

TOKEN = '1445371219:AAHcGxxqYiyioSEhjPo2vLVPHaprJ21WOUw'

bot = telepot.aio.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, MessageHandler, timeout=10),
])

loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot).run_forever())
print('Listening ...')

loop.run_forever()
