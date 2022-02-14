
from aiogram.utils.markdown import text


from config import TOKEN
import keyboards as kb
import datetime


from aiogram import Bot, Dispatcher, types

from aiogram.utils import executor
import sqlite3
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


###sqlite DB###

conn = sqlite3.connect(r'user.db')
cur = conn.cursor()


admin_id = 737108457
##



@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('btn'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    code = callback_query.data[-1]
    if code.isdigit():
        code = int(code)
    if code == 2:
        await bot.answer_callback_query(callback_query.id, text='Нажата вторая кнопка')
    elif code == 5:
        await bot.answer_callback_query(
            callback_query.id,
            text='Нажата кнопка с номером 5.\nА этот текст может быть длиной до 200 символов 😉',
            show_alert=True)
    else:
        await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f'Нажата инлайн кнопка! code={code}')


##


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!", reply_markup=kb.greet_kb)



help_message = text(
    'Этот бот создан тем же человером что и система ultrone',
    'Полный список команд знает только творец ',
    'но я попытаюсь донести вам идею создания бота',
    'я вдохновился одним ботом но он создан только для управления группой',
    'а это больше для поощерения и  для развлечения',
    'больше похоже на игру'

)
'''"Это урок по клавиатурам.",
"Доступные команды:\n",
"/start - приветствие",
"\nШаблоны клавиатур:",
"/hi1 - авто размер",
"/hi2 - скрыть после нажатия",
"/hi3 - больше кнопок",
"/hi4 - кнопки в ряд",
"/hi5 - больше рядов",
"/hi6 - запрос локации и номера телефона",
"/hi7 - все методы"
"/rm - убрать шаблоны",
"\nИнлайн клавиатуры:",
"/1 - первая кнопка",
"/2 - сразу много кнопок",
sep = "\n"'''
@dp.message_handler(commands=['hess'])
async def process_help_command(message: types.Message):
    await message.reply(str(message).replace(',',',\n'))
@dp.message_handler(text=['кто он'])
async def process_help_command(message: types.Message):
    if message.chat.type == 'supergroup':
        if 'reply_to_message' in message:
            await message.answer('Это пользыватель {0}'.format(message.reply_to_message.from_user.username))
    else:
        await  message.answer('Это работает только в группе.')


@dp.message_handler(text=['+'])
async def process_help_command(message: types.Message):
    if message.chat.type == 'supergroup':
        if 'reply_to_message' in message:
            nus = int(cur.execute("SELECT `reput` FROM where_me WHERE user_id=(?);",(message.from_user.id,)).fetchone()[0]) +1
            print(nus)
            cur.execute("UPDATE where_me SET reput = ? WHERE user_id = ?",(nus,message.from_user.id))
            conn.commit()
            await message.answer('Репутация повышена')
    else:
        await  message.answer('Это работает только в группе.')


@dp.message_handler(text=['повысить'])
async def process_help_command(message: types.Message):
    if message.chat.type == 'supergroup':
        if 'reply_to_message' in message:

            nus = int(cur.execute("SELECT `per` FROM user_per WHERE user_id=(?);",(message.reply_to_message.from_user.id,)).fetchone()[0])
            nul = int(cur.execute("SELECT `per` FROM user_per WHERE user_id=(?);",(message.from_user.id,)).fetchone()[0])
            print(nus, nul)
            #if message.from_user.id == 737108457 or message.from_user.id ==
            if nul+10 < nus:
                if nus ==0 or nus == 3:
                    await message.answer('создателя не возможно повысить')

                else:
                    cur.execute("UPDATE user_per SET per = ?   WHERE user_id = ?", (nus - 1, message.reply_to_message.from_user.id))
                    #print(cur.execute("UPDATE user_per SET per = ? WHERE user_id = ?", (nus - 1, message.from_user.id)))
                    conn.commit()
                    await message.answer(f'Репутация повышена  теперь она {cur.execute("SELECT `per` FROM user_per WHERE user_id=(?);",(message.reply_to_message.from_user.id,)).fetchone()[0]}')
            else:
                await  message.answer('Вы не можете повысить данного пользывателя \n для повышения ваша репутация должна быть выше на 10 едениц')
    else:
        await  message.answer('Это работает только в группе.')


@dp.message_handler(text=['понизить'])
async def process_help_command(message: types.Message):
    if message.chat.type == 'supergroup':
        if 'reply_to_message' in message:

            nus = int(cur.execute("SELECT `per` FROM user_per WHERE user_id=(?);",(message.reply_to_message.from_user.id,)).fetchone()[0])
            nul = int(cur.execute("SELECT `per` FROM user_per WHERE user_id=(?);",(message.from_user.id,)).fetchone()[0])
            print(nus, nul)
            #if message.from_user.id == 737108457 or message.from_user.id ==
            if nul+10 < nus:
                if nus ==0 or nus == 3:
                    await message.answer('создателя не возможно повысить')

                else:
                    cur.execute("UPDATE user_per SET per = ? WHERE user_id = ?", (nus + 1, message.reply_to_message.from_user.id))
                    #print(cur.execute("UPDATE user_per SET per = ? WHERE user_id = ?", (nus - 1, message.from_user.id)))
                    conn.commit()
                    await message.answer(f'Репутация понижена теперь она {cur.execute("SELECT `per` FROM user_per WHERE user_id=(?);",(message.reply_to_message.from_user.id,)).fetchone()[0]}')
            else:
                await  message.answer('Вы не можете повысить данного пользывателя \n для повышения ваша репутация должна быть выше на 10 едениц')
    else:
        await  message.answer('Это работает только в группе.')


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply(help_message)

@dp.message_handler(commands=['кто я'])
async def process_help_command(message: types.Message):
    await message.reply(message.chat.type)

@dp.message_handler(content_types=["new_chat_members"])
async def handler_new_member(message: types.Message):
    #user_name = message.new_chat_member.first_name
    fos = cur.execute("SELECT user_id FROM user_per;").fetchall()
    now = datetime.datetime.now()
    if message.from_user.id not in fos:
        cur.execute("INSERT INTO user_per VALUES(?,?,?);", (message.from_user.id, 3072, 'NONE'))
        cur.execute("INSERT INTO where_me VALUES(?,?,?,?);", (message.from_user.id, f'{now.day}:{now.month}:{now.year}',0,0))
        conn.commit()
        await message.answer(f"Добро пожаловать, @{message.from_user}")




@dp.message_handler(text=["кто я"])
async def handler_new_member(message: types.Message):
    fos = cur.execute("SELECT user_id FROM user_per;").fetchall()
    per = cur.execute("SELECT per FROM user_per WHERE user_id=(?);",(message.from_user.id,)).fetchone()[0]
    if message.from_user.id not in fos:
        whee_me = (f'''👤 Это пользователь [{message.from_user.first_name}](https://t.me/{message.from_user.username})
Ранг :{per}
Репутация: ✨{cur.execute("SELECT reput FROM where_me WHERE user_id=(?);",(message.from_user.id,)).fetchone()[0]}|+{cur.execute("SELECT `add` FROM where_me WHERE user_id=(?);",(message.from_user.id,)).fetchone()[0]}
Появление в группе: {cur.execute("SELECT one_mess FROM where_me WHERE user_id=(?);",(message.from_user.id,)).fetchone()[0]}

''')
        #await  message.answer('<a href="https://vk.com/id41732290">VK</a>',parse_mode="HTML", disable_web_page_preview=True)
        if cur.execute("SELECT one_mess FROM where_me WHERE user_id=(?);",(message.from_user.id,)).fetchone() == "NONE":
            await message.answer(whee_me, parse_mode='Markdown', disable_web_page_preview=True)
        else:
            await message.answer(whee_me+ f'О себе: \n  {cur.execute("SELECT names FROM user_per WHERE user_id=(?);",(message.from_user.id,)).fetchone()[0]}', parse_mode='Markdown', disable_web_page_preview=True)


#5121303843


@dp.message_handler(commands=["id"])
async def handler_new_member(message: types.Message):
    if 'reply_to_message' in message:
        await message.answer('`'+str(message.reply_to_message.from_user.id)+"`", parse_mode='Markdown')

    else:

        await message.answer('`'+str(message.from_user.id)+"`", parse_mode='Markdown')

    '''if message.chat.type == 'supergroup':
        if 'reply_to_message' in message:

            await message.answer(f"Добро пожаловать, @{message}")'''

        # user_name = message.new_chat_member.first_name
    #bot.send_message(message.chat.id,)

@dp.message_handler()
async def process_help_command(message: types.Message):
    pass

    #await message.answer(message)
    '''if message.chat.type == 'supergroup':
        if 'reply_to_message' in message:
            if message.text == 'кто он':
                await message.answer('Это пользыватель {0}'.format(message.text))
            #await message.answer(message.text)'''
            #await message.answer(str(message).replace(',',',\n'))#if message.reply_to_message():
        #await message.reply(str(message).replace(',',',\n'))'''
if __name__ == '__main__':
    executor.start_polling(dp)
'''
('\n'
 '\n'
 '{"message_id": 24, \n'
 '    "from": {"id": 1087968824, \n'
 '        "is_bot": true, \n'
 '        "first_name": "Group", \n'
 '        "username": "GroupAnonymousBot"}, \n'
 '    "sender_chat": {"id": -1001524536974, \n'
 '        "title": "house of ultron sys.", \n'
 '        "username": "HU_sys", \n'
 '        "type": "supergroup"}, \n'
 '    "chat": {"id": -1001524536974, \n'
 '        "title": "house of ultron sys.", \n'
 '        "username": "HU_sys", \n'
 '        "type": "supergroup"}, \n'
 '    "date": 1643820567, \n'
 '    "reply_to_message": {"message_id": 23, \n'
 '        "from": {"id": 1952138591, \n'
 '            "is_bot": false, \n'
 '            "first_name": "Олексі", \n'
 '            "last_name": "Й", \n'
 '            "username": "pokolpo"}, \n'
 '        "chat": {"id": -1001524536974, \n'
 '            "title": "house of ultron sys.", \n'
 '            "username": "HU_sys", \n'
 '            "type": "supergroup"}, \n'
 '    "date": 1643820561, \n'
 '    "text": "Ага"}, \n'
 '"text": "кто он"\n'
 '\n'
 '}\n'
 '\n'
 '\n'
 '\n')
 
 
 ////////////////////////////////////////////////
 
@dp.message_handler(commands=['hi1'])
async def process_hi1_command(message: types.Message):
    await message.reply("Первое - изменяем размер клавиатуры",
                        reply_markup=kb.greet_kb1)


@dp.message_handler(commands=['hi2'])
async def process_hi2_command(message: types.Message):
    await message.reply("Второе - прячем клавиатуру после одного нажатия",
                        reply_markup=kb.greet_kb2)


@dp.message_handler(commands=['hi3'])
async def process_hi3_command(message: types.Message):
    await message.reply("Третье - добавляем больше кнопок",
                        reply_markup=kb.markup3)


@dp.message_handler(commands=['hi4'])
async def process_hi4_command(message: types.Message):
    await message.reply("Четвертое - расставляем кнопки в ряд",
                        reply_markup=kb.markup4)


@dp.message_handler(commands=['hi5'])
async def process_hi5_command(message: types.Message):
    await message.reply("Пятое - добавляем ряды кнопок",
                        reply_markup=kb.markup5)


@dp.message_handler(commands=['hi6'])
async def process_hi6_command(message: types.Message):
    await message.reply("Шестое - запрашиваем контакт и геолокацию\n"
                        "Эти две кнопки не зависят друг от друга",
                        reply_markup=kb.markup_request)


@dp.message_handler(commands=['hi7'])
async def process_hi7_command(message: types.Message):
    await message.reply("Седьмое - все методы вместе",
                        reply_markup=kb.markup_big)


@dp.message_handler(commands=['rm'])
async def process_rm_command(message: types.Message):
    await message.reply("Убираем шаблоны сообщений",
                        reply_markup=kb.ReplyKeyboardRemove())

##


@dp.message_handler(commands=['1'])
async def process_command_1(message: types.Message):
    await message.reply("Первая инлайн кнопка",
                        reply_markup=kb.inline_kb1)


@dp.message_handler(commands=['2'])
async def process_command_2(message: types.Message):
    await message.reply("Отправляю все возможные кнопки",
                        reply_markup=kb.inline_kb_full)
 
 
 
 
 
 '''