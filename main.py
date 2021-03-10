import logging
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, executor, types
from pedro import Pedro

with open('token.txt', 'r') as token_file:
    API_TOKEN = token_file.readline()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

pedro = Pedro()

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    name = message.from_user.full_name
    if name:
        resp = 'Ciao '+name+'!\nBenvenuto in Turni Pedro, ora non ha più scampo!'
    else:
        resp = 'Ciao!\nBenvenuto in Turni Pedro, ora non ha più scampo!'
    await message.answer(resp)

# handle command '/oggi'
@dp.message_handler(commands=['oggi'])
async def send_reply(message: types.Message):
    shift_explain = pedro.tell_shift('oggi')
    await message.answer(shift_explain, parse_mode=types.ParseMode.MARKDOWN)

# handle command '/domani'
@dp.message_handler(commands=['domani'])
async def send_reply(message: types.Message):
    shift_explain = pedro.tell_shift('domani')
    await message.answer(shift_explain, parse_mode=types.ParseMode.MARKDOWN)

# handle command '/tabella'
@dp.message_handler(commands=['tabella'])
async def send_reply(message: types.Message):
    await message.answer(pedro.all_shift(), parse_mode=types.ParseMode.MARKDOWN)

# handle command '/dio'
@dp.message_handler(commands=['dio'])
async def send_reply(message: types.Message):
    await message.answer(pedro.dio(), parse_mode=types.ParseMode.MARKDOWN)

# handle set time
@dp.message_handler(regexp='^.*/set.*$')
async def set_new_date(message: types.Message):
    username = message.from_user.mention
    if (username == '@ilbert98'):
        try:
            t = message.text[4:].strip()    # remove '/set' from string, keep only the date
            t += ' 07:00:00'
            START = datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
            with open('start.txt', 'w') as start_file:
                start_file.write(str(START))
            await message.answer('Inizio impostato per il '+str(START))
        except Exception as e:
            print('ERROR', e)
            await message.answer("C'è stato un errore:\n"+str(e))
        return
    await message.answer('Non hai le autorizzazioni per impostare il giorno iniziale')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)