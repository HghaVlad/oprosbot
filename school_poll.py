from analitic import analyse,getimg
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, LabeledPrice, ReplyKeyboardMarkup, ReplyKeyboardRemove
from datetime import datetime
import pymysql as sq

bot = telebot.TeleBot("token")
base_h = 'localhost'
base_user = 'admin'
base_pass = 'admin'
base_name = 'polls'
poll_info = {}
print("it works")

@bot.message_handler(commands=['start'])
def st_com(message):
    with sq.connect(host=base_h,user=base_user,password=base_pass,database=base_name ) as con:
        cur = con.cursor()
        cur.execute(f"SELECT t_id FROM admins where t_id = {message.chat.id} ")
        res = cur.fetchone()
        if res == None:
            user_keyb = ReplyKeyboardMarkup(True)
            user_keyb.add("Пройти опрос")
            bot.send_message(message.chat.id, "*Привет*\nЭтот бот предназначен для создания и проведения опросов среди школьников",parse_mode='Markdown',reply_markup=user_keyb)
        else:
            admin_keyb =ReplyKeyboardMarkup(True)
            admin_keyb.add("Пройти опрос")
            admin_keyb.add("Редактировать опрос")
            bot.send_message(message.chat.id,"*Вы авторизовались как администратор*",parse_mode='Markdown',reply_markup=admin_keyb)

@bot.message_handler(regexp='Пройти опрос')
def get_poll(message):
    with sq.connect(host=base_h,user=base_user,password=base_pass,database=base_name ) as con:
        cur = con.cursor()
        start_poll = InlineKeyboardMarkup(row_width=1)
        cur.execute("SELECT id, name FROM polls WHERE `show` = 1")
        polls = cur.fetchall()
        if len(polls) == 0:
            bot.send_message(message.chat.id, "*Для вас нет доступных опросов*",parse_mode='Markdown')
        else:
            x = 0
            cur.execute(f"SELECT poll_id FROM poll_req WHERE t_id = {message.chat.id}")
            polls_completed = [int(x[0]) for x  in cur.fetchall()]
            for id in polls:
                if id[0] not in polls_completed:
                    x = 1
                    start_poll.add(InlineKeyboardButton(text=id[1], callback_data='getpoll?'+str(id[0])))
            if x == 0:
                bot.send_message(message.chat.id, "*Для вас нет доступных опросов*",parse_mode='Markdown')
            else:
                bot.send_message(message.chat.id,"*Выберите опрос*",parse_mode='Markdown',reply_markup=start_poll)

@bot.message_handler(regexp='Редактировать опрос')
def edit_poll(message):
    with sq.connect(host=base_h,user=base_user,password=base_pass,database=base_name ) as con:
        cur = con.cursor()
        cur.execute(f"SELECT t_id FROM admins where t_id = {message.chat.id} ")
        res = cur.fetchone()
        if res == None:
            bot.send_message(message.chat.id,"*У вас нет доступа*",parse_mode='Markdown')
        else:
            cur.execute("SELECT id, name FROM polls ")
            polls = cur.fetchall()
            admin_keyb = InlineKeyboardMarkup()
            for i in range(0,len(polls),2):
                try:
                    admin_keyb.add(InlineKeyboardButton(text=polls[i][1], callback_data='admin_editpoll?'+str(polls[i][0])),InlineKeyboardButton(text=polls[i+1][1], callback_data='admin_editpoll?'+str(polls[i+1][0])))
                except:
                    admin_keyb.add(InlineKeyboardButton(text=polls[i][1], callback_data='admin_editpoll?'+str(polls[i][0])))
            admin_keyb.add(InlineKeyboardButton(text='Создать опрос',callback_data='admin_createpoll'))
            bot.send_message(message.chat.id,"*Выберите опрос*",parse_mode='Markdown',reply_markup=admin_keyb)

@bot.callback_query_handler(func=lambda call:True)
def calldata(call):
    if call.data.startswith('getpoll'):
        id = call.data.split("?")[1]
        with sq.connect(host=base_h,user=base_user,password=base_pass,database=base_name ) as con:
            cur = con.cursor()
            cur.execute(f"SELECT * FROM polls WHERE id = {id} ")
            poll = cur.fetchone()
            if poll == None:
                backinl = InlineKeyboardMarkup()
                backinl.add(InlineKeyboardButton(text='Назад',callback_data='polls_back'))
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text='*Такого опроса не существует*',parse_mode='Markdown')
            else:
                cur.execute(f"SELECT id FROM poll_req WHERE t_id = {call.message.chat.id} and poll_id = {id}")
                req = cur.fetchone()
                if req == None:
                    startdoPoll = InlineKeyboardMarkup()
                    startdoPoll.add(InlineKeyboardButton(text='Да',callback_data='startdoPoll?'+str(id)),InlineKeyboardButton(text='Нет',callback_data='polls_back'))
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='*Вы хотите начать проходить опрос?*',parse_mode='Markdown',reply_markup=startdoPoll)

    elif call.data == 'polls_back':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        get_poll(call.message)

    elif call.data.startswith('startdoPoll'):
        id = call.data.split("?")[1]
        with sq.connect(host=base_h,user=base_user,password=base_pass,database=base_name ) as con:
            cur = con.cursor()
            cur.execute(f"SELECT * FROM polls WHERE id = {id} ")
            poll = cur.fetchone()
            quests = poll[3].split(",;")
            que = quests[0].split("/;")
            poll_info.update({call.message.chat.id:{'step':0, 'list':quests,'poll_id':id }})
            if que[1] == 'no':
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.send_message(chat_id=call.message.chat.id,text=str(que[0]),parse_mode='Markdown')
                bot.register_next_step_handler(call.message, get_poll_info)
            else:
                inls = que[1].split("|")
                inl = InlineKeyboardMarkup()
                for i in range(0, len(inls), 2):
                    try:
                        inl.add(InlineKeyboardButton(text=inls[i], callback_data='doPollans?'+str(inls[i])),InlineKeyboardButton(text=inls[i+1], callback_data='doPollans?'+str(inls[i+1])))
                    except:
                        inl.add(InlineKeyboardButton(text=inls[i], callback_data='doPollans?'+str(inls[i])))
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.send_message(chat_id=call.message.chat.id,text=str(que[0]),parse_mode='Markdown',reply_markup=inl)
    elif call.data.startswith("doPollans"):
        info = call.data.split("?")[1]
        poll_info[call.message.chat.id]['s'+str(poll_info[call.message.chat.id]['step'])] = info
        poll_info[call.message.chat.id]['step'] = poll_info[call.message.chat.id]['step'] +1
        if poll_info[call.message.chat.id]['step'] == len(poll_info[call.message.chat.id]['list']):
            inl = InlineKeyboardMarkup()
            inl.add(InlineKeyboardButton(text='Да',callback_data='finishdoPoll'),InlineKeyboardButton(text='Нет',callback_data='polls_back'))
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.send_message(call.message.chat.id,"*Опрос завершен\n*Отправить данные?",parse_mode='Markdown',reply_markup=inl)
        else:
            que = poll_info[call.message.chat.id]['list'][poll_info[call.message.chat.id]['step']].split("/;")
            if que[1] == 'no':
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.send_message(chat_id=call.message.chat.id,text=str(que[0]),parse_mode='Markdown')
                bot.register_next_step_handler(call.message, get_poll_info)
            else:
                inls = que[1].split("|")
                inl = InlineKeyboardMarkup()
                for i in range(0, len(inls), 2):
                    try:
                        inl.add(InlineKeyboardButton(text=inls[i], callback_data='doPollans?'+str(inls[i])),InlineKeyboardButton(text=inls[i+1], callback_data='doPollans?'+str(inls[i+1])))
                    except:
                        inl.add(InlineKeyboardButton(text=inls[i], callback_data='doPollans?'+str(inls[i])))
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.send_message(chat_id=call.message.chat.id,text=str(que[0]),parse_mode='Markdown',reply_markup=inl)
    elif call.data == 'finishdoPoll':
        with sq.connect(host=base_h,user=base_user,password=base_pass,database=base_name ) as con:
            cur = con.cursor()
            cur.execute(f"SELECT id FROM poll_req WHERE t_id = {call.message.chat.id} and poll_id = {poll_info[call.message.chat.id]['poll_id']}")
            res = cur.fetchone()
            if res == None:
                answers = ''
                for i in range(len(poll_info[call.message.chat.id]['list'])):
                    answers = answers + poll_info[call.message.chat.id]['s'+str(i)] + '/;'
                answers = answers[:-2]
                print("hey",datetime.now())
                cur.execute(f"INSERT INTO poll_req(poll_id, Answers, t_id, Date) VALUES({poll_info[call.message.chat.id]['poll_id']}, '{answers}', {call.message.chat.id}, '{datetime.today().date()}' ) ")
                cur.execute(f"UPDATE polls Set cols = cols + 1 WHERE id = {poll_info[call.message.chat.id]['poll_id']} ")
                con.commit()
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                get_poll(call.message)
            else:
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.send_message(call.message.chat.id,"*Вы уже участвовали в этом опросе*",parse_mode='Markdown')
                get_poll(call.message)

    # Админ панель
    elif call.data.startswith("admin_editpoll"):
        id = call.data.split("?")[1]
        with sq.connect(host=base_h,user=base_user,password=base_pass,database=base_name ) as con:
            cur = con.cursor()
            cur.execute(f"SELECT `name`, `cols`, `show` FROM polls WHERE id = {id} ")
            res = cur.fetchone()
            if res[2] == 0:
                t = 'Скрыт'
            else:
                t = 'Открыт'
            inline = InlineKeyboardMarkup()
            inline.add(InlineKeyboardButton(text='Посмотреть результаты',callback_data='admin_pollAnalitic?'+str(id)))
            inline.add(InlineKeyboardButton(text='Удалить',callback_data='admin_pollDelete?'+str(id)))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b>Опрос</b> {t}\n\n<b>Название:</b> {res[0]}\n<b>Количество участников:</b> {res[1]}',parse_mode='HTML',reply_markup=inline)
    elif call.data.startswith("admin_pollAnalitic"):
        id = call.data.split("?")[1]
        with sq.connect(host=base_h,user=base_user,password=base_pass,database=base_name ) as con:
            cur = con.cursor()
            cur.execute(f"SELECT Answers FROM poll_req WHERE poll_id = {id} ")
            answers = cur.fetchall()
            cur.execute(f"SELECT Questions FROM polls WHERE id = {id} ")
            quests = cur.fetchone()[0].split(",;")
            print(answers)
            print(answers[0][0])
            newanswers = ['0' for _ in range(len(answers))]
            for i in range(len(answers)):
                newanswers[i] = answers[i][0].split('/;')
            data = analyse(newanswers)
            name = str(call.message.chat.id)+'-'+str(datetime.today().date()).replace('.','')
            images = getimg(name, data,quests)
            med = [InputMediaPhoto(open(x, 'rb')) for x in images]
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.send_media_group(call.message.chat.id, media=med)
    elif call.data.startswith('admin_pollDelete'):
        id = call.data.split("?")[1]
        inline = InlineKeyboardMarkup()
        inline.add(InlineKeyboardButton(text='Да',callback_data='admin_pollDelyes?'+str(id)),InlineKeyboardButton(text='Нет',callback_data='admin_pollDelno'))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text="*Вы хотить удалить опрос?*",reply_markup=inline,parse_mode='Markdown')
    elif call.data.startswith("admin_pollDelyes?"):
        id = call.data.split("?")[1]
        with sq.connect(host=base_h,user=base_user,password=base_pass,database=base_name ) as con:
            cur = con.cursor()
            cur.execute(f"DELETE FROM polls WHERE id = '{id}' ")
            cur.execute(F"DELETE FROM poll_req WHERE poll_id = {id} ")
            con.commit()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="*Опрос успешно удален*",parse_mode='Markdown')
        edit_poll(call.message)
    elif call.data == 'admin_pollDelno':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        edit_poll(call.message)
    elif call.data == 'admin_createpoll':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='*Введите название опроса*',parse_mode='Markdown')
        bot.register_next_step_handler(call.message, admincreatePoll_name)
    elif call.data == 'admin_createPoll_button':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='*Введите текст кнопки*',parse_mode='Markdown')
        bot.register_next_step_handler(call.message, admincreatePoll_but)
    elif call.data == 'admin_createPoll_next':
        if poll_info[call.message.chat.id]['step'] == poll_info[call.message.chat.id]['cols_step']:
            inl = InlineKeyboardMarkup()
            inl.add(InlineKeyboardButton(text='Да',callback_data='admin_createPollYes'),InlineKeyboardButton(text='Нет',callback_data='admin_createPollNo'))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='*Опрос завершен*\nОпубликовать?',parse_mode='Markdown',reply_markup=inl)
        else:
            poll_info[call.message.chat.id]['step'] += 1
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='*Введите текст следующего вопроса*',parse_mode='Markdown')
            bot.register_next_step_handler(call.message, admincreatePoll_Info)
    elif call.data == 'admin_createPollYes':
        quest = ''
        for i in range(1, poll_info[call.message.chat.id]['cols_step']+ 1):
            quest = quest + poll_info[call.message.chat.id]['info'+str(i)] + ',;'
        quest = quest[:-2]
        with sq.connect(host=base_h,user=base_user,password=base_pass,database=base_name ) as con:
            cur = con.cursor()
            cur.execute(f"INSERT INTO polls(`name`,t_id, Questions, `cols`, `show`, `Date`) VALUES('{poll_info[call.message.chat.id]['namepf'] }',{call.message.chat.id}, '{quest}', 0 , 1, '{datetime.today().date()}'   )  ")
            con.commit()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="*Опрос успешно создан*",parse_mode='Markdown')
        edit_poll(call.message)
    elif call.data == 'admin_createPollNo':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="*Опрос удален*",parse_mode='Markdown')
        edit_poll(call.message)

def get_poll_info(message):
    poll_info[message.chat.id]['s'+str(poll_info[message.chat.id]['step'])] = message.text
    poll_info[message.chat.id]['step'] = poll_info[message.chat.id]['step'] +1
    if poll_info[message.chat.id]['step'] == len(poll_info[message.chat.id]['list']):
        inl = InlineKeyboardMarkup()
        inl.add(InlineKeyboardButton(text='Да',callback_data='finishdoPoll'),InlineKeyboardButton(text='Нет',callback_data='polls_back'))
        bot.send_message(message.chat.id,"*Опрос завершен\n*Отправить данные?",parse_mode='Markdown',reply_markup=inl)
    else:
        que = poll_info[message.chat.id]['list'][poll_info[message.chat.id]['step']].split("/;")
        if que[1] == 'no':
            bot.send_message(chat_id=message.chat.id,text=str(que[0]),parse_mode='Markdown')
        else:
            inls = que[1].split("|")
            inl = InlineKeyboardMarkup()
            for i in range(0, len(inls), 2):
                try:
                    inl.add(InlineKeyboardButton(text=inls[i], callback_data='doPollans?'+str(inls[i])),InlineKeyboardButton(text=inls[i+1], callback_data='doPollans?'+str(inls[i+1])))
                except:
                    inl.add(InlineKeyboardButton(text=inls[i], callback_data='doPollans?'+str(inls[i])))
            bot.send_message(chat_id=message.chat.id,text=str(que[0]),parse_mode='Markdown',reply_markup=inl)

def admincreatePoll_name(message):
    poll_info.update({message.chat.id:{}})
    poll_info[message.chat.id]['namepf'] = message.text
    bot.send_message(message.chat.id,"*Сколько будет вопросов?*",parse_mode='Markdown')
    bot.register_next_step_handler(message, admincreatePoll_qu)

def admincreatePoll_qu(message):
    if message.text.isdigit():
        poll_info[message.chat.id]['cols_step'] = int(message.text) 
        poll_info[message.chat.id]['step'] = 1
        bot.send_message(message.chat.id,"*Введите текст первого вопроса*",parse_mode='Markdown')
        bot.register_next_step_handler(message, admincreatePoll_Info)
    else:
        bot.send_message(message.chat.id,"*Пожалуйста введите число*",parse_mode='Markdown')
        bot.register_next_step_handler(message,admincreatePoll_qu )

def admincreatePoll_Info(message):
    poll_info[message.chat.id]['info'+str(poll_info[message.chat.id]['step'])] = message.text+ '/;no'
    inl = InlineKeyboardMarkup()
    inl.add(InlineKeyboardButton(text='Продолжить',callback_data='admin_createPoll_next'))
    inl.row(InlineKeyboardButton(text='Добавить кнопку',callback_data='admin_createPoll_button'))
    bot.send_message(message.chat.id,f"<b>Вопрос:</b> {message.text}",parse_mode='HTML',reply_markup=inl)

def admincreatePoll_but(message):
    if poll_info[message.chat.id]['info'+str(poll_info[message.chat.id]['step'])][-2:] == 'no':
        poll_info[message.chat.id]['info'+str(poll_info[message.chat.id]['step'])] = poll_info[message.chat.id]['info'+str(poll_info[message.chat.id]['step'])].replace('/;no','/;'+str(message.text))
    else:
        poll_info[message.chat.id]['info'+str(poll_info[message.chat.id]['step'])] = poll_info[message.chat.id]['info'+str(poll_info[message.chat.id]['step'])] + '|'+str(message.text)
    inl = InlineKeyboardMarkup()
    inl.add(InlineKeyboardButton(text='Продолжить',callback_data='admin_createPoll_next'))
    inl.row(InlineKeyboardButton(text='Добавить кнопку',callback_data='admin_createPoll_button'))
    if poll_info[message.chat.id]['info'+str(poll_info[message.chat.id]['step'])].split('/;')[1].replace('|','; ') == 'no':
        t = 'Нет'
    else:
        t = poll_info[message.chat.id]['info'+str(poll_info[message.chat.id]['step'])].split('/;')[1].replace('|','; ')
    bot.send_message(message.chat.id,f"<b>Вопрос:</b> {poll_info[message.chat.id]['info'+str(poll_info[message.chat.id]['step'])].split('/;')[0]}\n<b>Кнопки: </b>{t}",parse_mode='HTML',reply_markup=inl)


bot.infinity_polling()
