import telebot
import sqlite3
import time
import mssql
from telebot import types
from mycheck import inn_check
from mycheck import formatStr
from telebot import apihelper


#-------------------------------------------Коннект-------------------------------------------------------------



apihelper.proxy = {'https': 'socks5h://127.0.0.1:9150'}
#apihelper.proxy = {'https': 'socks5h://34.76.159.209:80'}
TOKEN = '1095944337:AAHUzqbcZPNOyAB5L3Wilu9ofumQYxAcPB4'
bot  = telebot.TeleBot(TOKEN);
name = {}
tele = {}  
inn = {}
adress = {}
problem={}
#mssql.create()

# --------------------------------------------функции клавиатур------------------------------------------------------
hide_markup = telebot.types.ReplyKeyboardRemove()

def keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('главное меню ⏎')
    btn2 = types.KeyboardButton('Редактировать личные данные')
    markup.add(btn1, btn2)
    return markup

def keyboard_sql(rows, message, ver):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_back = types.KeyboardButton('главное меню ⏎')
    btn_cont = types.KeyboardButton(text='Отправить мой номер телефона', request_contact=True)
    btn_name = types.KeyboardButton(text=str(message.chat.first_name))
    buttons_added = []
    buttons_in_row = 2
    for row in rows:
        if (len(row)==2 and (ver=='name')):
            buttons_added.append(types.InlineKeyboardButton(text = str(row[0])))
        elif (len(row)==2 and (ver=='cont')):
            buttons_added.append(types.InlineKeyboardButton(text = str(row[1])))
        elif (len(row)==2):
            buttons_added.append(types.InlineKeyboardButton(text = str(row[0])+': '+str(row[1])))
        else:
            buttons_added.append(types.InlineKeyboardButton(text = str(row[0])))
        if len(buttons_added) == buttons_in_row:
            print (row[0])
            markup.add(*buttons_added)
            buttons_added = []
    if buttons_added:
        markup.add(*buttons_added)
    if(ver=='cont'):
        markup.add(btn_cont)
    if(ver=='name'):
        markup.add(btn_name)
    markup.add(btn_back)
    return markup

def keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Оформить заявку')
    btn2 = types.KeyboardButton('Удалить личные данные')
    markup.add(btn1,btn2)
    return markup

def keyboard_edit():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton ( text = 'Имя' , callback_data= 'name'  )
    btn2 = types.InlineKeyboardButton ( text = 'Телефон' , callback_data= 'phone_number'  )
    btn3 = types.InlineKeyboardButton ( text = 'ИНН' , callback_data='inn'  )
    btn4 = types.InlineKeyboardButton ( text = 'Адрес' , callback_data='adress'  )
    btn5 = types.InlineKeyboardButton ( text = 'Описание проблемы' , callback_data='problem'  )
    markup.row (btn1, btn2, btn3)
    markup.row (btn4, btn5)
    return markup

def keyboard_edit_person():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton ( text = 'Имя и телефон' , callback_data='del_user'  )
    btn2 = types.InlineKeyboardButton ( text = 'ИНН' , callback_data='del_inn'  )
    btn3 = types.InlineKeyboardButton ( text = 'Адрес' , callback_data='del_adress'  )
    btn4 = types.InlineKeyboardButton ( text = 'Отмена' , callback_data= 'main_menu'  )
    markup.row (btn1)
    markup.row (btn2, btn3)
    markup.row (btn4)
    return markup

def keyboard_yesno():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton ( text = 'Отправить' , callback_data= 'send'  )
    btn2 = types.InlineKeyboardButton ( text = 'Изменить' , callback_data= 'edit'  )
    btn3 = types.InlineKeyboardButton ( text = 'Отмена' , callback_data= 'main_menu'  )
    markup.add (btn1, btn2)
    markup.add (btn3)
    return markup

#-------------------------------------сам бот----------------------------------------------------------------
@bot.message_handler(commands=[ 'start', 'help' ]) 
def welcome(message):
    user_id = message.from_user.id
    rows = mssql.select_last_user(user_id)
    print(rows)
    if (rows):
        bot.send_message(message.from_user.id, 'Что желаете, '+str(message.from_user.first_name)+'?', reply_markup=keyboard())
        for row in rows:
            name[user_id] = row.name
            tele[user_id] = row.phone
            inn[user_id] = row.inn
            adress[user_id] = row.adress
            print (name)
        return True
    else:
        bot.send_message(message.from_user.id, 'Добро пожаловать, '+str(message.from_user.first_name)+'!\r\nЭто в помощник оформления заявок в АСФ.')
        bot.send_message(message.from_user.id, 'Давайте сначала познакомимся и я Вас запомню :)\r\nВ дальнейшем Вы сможете удалить сохраненые данные или ввесли новые при оформлении заявки.')
        bot.send_message(message.from_user.id, 'Напишите мне как к Вам обращаться?', reply_markup=keyboard_sql(rows, message, 'name'))
        bot.register_next_step_handler(message, lambda msg: get_name("0", msg))
        return False
    
@bot.message_handler(content_types=["text", "sticker", "pinned_message", "photo", "audio"])
def start(message):
    print(message)
    if (message.text == 'Оформить заявку'):
        if (welcome(message)):
            bot.send_message(message.from_user.id, "Опишите Вашу проблему:", reply_markup=hide_markup)
            bot.register_next_step_handler(message, lambda msg: get_problem("0", msg)) #следующий шаг – функция get_problem
    elif (message.text == 'Удалить личные данные'):
        #bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.from_user.id, "Выберите, что хотите удалить:", reply_markup=keyboard_edit_person())
    elif (message.text == 'главное меню ⏎'):
        welcome(message)
    else:
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        bot.send_message(message.from_user.id, 'Для начала работы нажмите на /start.', reply_markup = hide_markup)

def get_name(edit, message): #получаем имя
    user_id = message.from_user.id
    rows = mssql.select_user(user_id)
    if (message.text == 'главное меню ⏎'):
        welcome(message)
        return
    elif (edit == '1'):
        bot.send_message(message.chat.id, 'Имя изменено.', reply_markup=keyboard())
        name[user_id] = message.text
        bot.send_message(message.from_user.id, 'Ваше имя: '+name[user_id]+'\r\nКонтактный телефон: '+tele[user_id]+'\r\nИНН: '+inn[user_id]+'\r\nАдрес: '+adress[user_id]+'\r\nПроблема: '+problem[user_id]+'', reply_markup=keyboard_yesno())

    elif(edit == '0'):
        bot.send_message(message.chat.id, "Введите номер телефона:", reply_markup=keyboard_sql(rows, message, 'cont'))
        name[user_id] = message.text
        print (name.items())
        bot.register_next_step_handler(message, lambda msg: get_phone("0", msg))

def get_phone (edit, message): #получаем телефон
    user_id = message.from_user.id
    rows = mssql.select_user(user_id)
    if (message.text == 'главное меню ⏎'):
        welcome(message)
        return
    if (message.content_type == "contact"):
        phone = message.contact.phone_number
    else:
        phone = message.text
    tele[user_id] = formatStr(phone)
    print (tele.items())
    if (edit == '1'):
        if (tele[user_id]):
            bot.send_message(message.chat.id, 'Номер изменен', reply_markup=keyboard())
            bot.send_message(message.from_user.id, 'Ваше имя: '+name[user_id]+'\r\nКонтактный телефон: '+tele[user_id]+'\r\nИНН: '+inn[user_id]+'\r\nАдрес: '+adress[user_id]+'\r\nПроблема: '+problem[user_id]+'', reply_markup=keyboard_yesno())
        else:
            bot.send_message(message.from_user.id, 'Введите правильный номер!', reply_markup=keyboard_sql(rows, message, 'cont'))
            bot.register_next_step_handler(message, lambda msg: get_phone("1", msg))
    elif (edit == '0'):
        if (tele[user_id]):
            rows = mssql.select_inn(user_id)
            bot.send_message(message.from_user.id, 'Введите Ваш ИНН или выберите из сохраненных ранее:', reply_markup=keyboard_sql(rows, message, '0')) #
            bot.register_next_step_handler(message, lambda msg: get_inn("0", msg))
        else:
            bot.send_message(message.from_user.id, 'Введите правильный номер!', reply_markup=keyboard_sql(rows, message, 'cont'))
            bot.register_next_step_handler(message, lambda msg: get_phone("0", msg))

def get_inn (edit, message): #получаем ИНН
    user_id = message.from_user.id
    if (message.text == 'главное меню ⏎'):
        welcome(message)
        return
    elif (edit == '1'):
        inn[user_id] = message.text
        ckinn = inn_check(inn[user_id])
        print (inn.items())
        if (ckinn):
            bot.send_message(message.chat.id, 'ИНН изменен', reply_markup=keyboard())
            bot.send_message(message.from_user.id, 'Ваше имя: '+name[user_id]+'\r\nКонтактный телефон: '+tele[user_id]+'\r\nИНН: '+inn[user_id]+'\r\nАдрес: '+adress[user_id]+'\r\nПроблема: '+problem[user_id]+'', reply_markup=keyboard_yesno())
        else:
            bot.send_message(message.from_user.id, 'Не корректный ИНН, введите заново!')
            bot.register_next_step_handler(message, lambda msg: get_inn("1", msg))
    elif (edit == '0'):
        inn[user_id] = message.text
        ckinn = inn_check(inn[user_id])
        print (inn.items())
        if (ckinn):
            rows = mssql.select_adress(user_id)
            bot.send_message(message.from_user.id, 'Введите адрес объекта или выберите из сохраненных ранее:', reply_markup=keyboard_sql(rows, message, '0')) #
            bot.register_next_step_handler(message, lambda msg: get_adress("0", msg))
        else:
            bot.send_message(message.from_user.id, 'Не корректный ИНН, введите заново!')
            bot.register_next_step_handler(message, lambda msg: get_inn("0", msg))

def get_adress(edit, message): #получаем адрес
    user_id = message.from_user.id
    if (message.text == 'главное меню ⏎'):
        welcome(message)
        return
    if (edit == '1'):
        bot.send_message(message.chat.id, 'Адрес изменен.', reply_markup=keyboard())
        adress[user_id] = message.text
        print (adress.items())
        bot.send_message(message.from_user.id, 'Ваше имя: '+name[user_id]+'\r\nКонтактный телефон: '+tele[user_id]+'\r\nИНН: '+inn[user_id]+'\r\nАдрес: '+adress[user_id]+'\r\nПроблема: '+problem[user_id]+'', reply_markup=keyboard_yesno())
    elif(edit == '0'): 
        bot.send_message(message.chat.id, "Я Вас запомнил! :)", reply_markup=hide_markup)
        bot.send_message(message.chat.id, "Теперь вы можете оформить заявку или удалить свои данные.", reply_markup=keyboard())
        adress[user_id] = message.text
        mssql.insert(user_id, name[user_id], tele[user_id], inn[user_id], adress[user_id])
        print (adress.items())
        bot.register_next_step_handler(message, start)

def get_problem (edit, message): # описание завки
    user_id = message.from_user.id
    if (message.text == 'главное меню ⏎'):
        welcome(message)
        return
    elif (edit == '1'):
        bot.send_message(message.chat.id, 'Описание изменнено', reply_markup=keyboard())
        problem[user_id] = message.text
        print (problem.items())
        bot.send_message(message.from_user.id, 'Ваше имя: '+name[user_id]+'\r\nКонтактный телефон: '+tele[user_id]+'\r\nИНН: '+inn[user_id]+'\r\nАдрес: '+adress[user_id]+'\r\nПроблема: '+problem[user_id]+'', reply_markup=keyboard_yesno())
    elif (edit == '0'):
        problem[user_id] = message.text
        print (problem.items())
        bot.send_message(message.from_user.id, 'Все верно?', reply_markup=hide_markup)
        bot.send_message(message.from_user.id, 'Ваше имя: '+name[user_id]+'\r\nКонтактный телефон: '+tele[user_id]+'\r\nИНН: '+inn[user_id]+'\r\nАдрес: '+adress[user_id]+'\r\nПроблема: '+problem[user_id]+'', reply_markup=keyboard_yesno())

def del_user(message):
    if (message.text == 'главное меню ⏎'):
        welcome(message)
        return
    else:
        user_id = message.from_user.id
        rows = mssql.select_user(user_id)
        try:
            n, p = map(str, message.text.split(': '))
            print (user_id, n, p)
            mssql.del_user(user_id , n, p)
        except:
            bot.send_message(message.from_user.id, "Таких данных нет. Выберите, что хотите удалить кнопками ниже:", reply_markup=keyboard_sql(rows, message, '0'))
            return
        rows = mssql.select_user(user_id)
        if(rows):
           bot.send_message(message.from_user.id, "Выберите, что хотите удалить:", reply_markup=keyboard_sql(rows, message, '0'))
           bot.register_next_step_handler(message, del_user)
        else:
           bot.send_message(user_id, 'Больше нет сохраненных данных, в дальнейшем нужно будет заполнить анкету заново.', reply_markup=keyboard())
           name.pop('user_id', None)
           tele.pop('user_id', None)
           print(name, tele)

def del_inn(message):
    if (message.text == 'главное меню ⏎'):
        welcome(message)
        return
    else:
        user_id = message.from_user.id
        mssql.del_inn(user_id , message.text)
        rows = mssql.select_inn(user_id)
        if(rows):
           bot.send_message(message.from_user.id, "Выберите, что хотите удалить:", reply_markup=keyboard_sql(rows, message, '0'))
           bot.register_next_step_handler(message, del_inn)
        else:
           bot.send_message(user_id, 'Больше нет сохраненных ИНН, в дальнейшем нужно будет заполнить анкету заново.', reply_markup=keyboard())
           inn.pop('user_id', None)
           print(inn)

def del_adress(message):
     if (message.text == 'главное меню ⏎'):
        welcome(message)
        return
     else:
        user_id = message.from_user.id
        mssql.del_adress(user_id , message.text)
        rows = mssql.select_adress(user_id)
        if(rows):
            bot.send_message(message.from_user.id, "Выберите, что хотите удалить:", reply_markup=keyboard_sql(rows, message, '0'))
            bot.register_next_step_handler(message, del_adress)
        else:
            bot.send_message(user_id, 'Больше нет сохраненных адресов, в дальнейшем нужно будет заполнить анкету заново.', reply_markup=keyboard())
            adress.pop('user_id', None)
            print(adress)

def log(message):
    print("\n ------")
    from datetime import datetime
    print(datetime.now())
    print("Сообщение от {0} {1}. (id = {2}) \nТекст = {3}".format(message.from_user.first_name,
                                                                   message.from_user.last_name,
                                                                   str(message.from_user.id), message.text))
        
#----------------------------------------------call-бэки клавиатыр--------------------------------------
@bot.callback_query_handler(func=lambda c:c.data)
def callback_inline(c):
    user_id = c.from_user.id
    if c.data == "send":
        bot.send_message(c.message.chat.id, 'Ваша заявка оформлена.\r\nСпасибо!', reply_markup=keyboard())
        mssql.insert(user_id, name[user_id], tele[user_id], inn[user_id], adress[user_id])
        bot.send_message("-372849868", 'Новая заявка!\r\nИмя: '+name[user_id]+'\r\nКонтактный телефон: '+tele[user_id]+'\r\nИНН: '+inn[user_id]+'\r\nАдрес: '+adress[user_id]+'\r\nПроблема: '+problem[user_id]+'')
        bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text='Ваше имя: '+name[user_id]+'\r\nКонтактный телефон: '+tele[user_id]+'\r\nИНН: '+inn[user_id]+'\r\nАдрес: '+adress[user_id]+'\r\nПроблема: '+problem[user_id]+'')
        #welcome(c.message)
    elif c.data == "edit":
        bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text='Ваше имя: '+name[user_id]+'\r\nКонтактный телефон: '+tele[user_id]+'\r\nИНН: '+inn[user_id]+'\r\nАдрес: '+adress[user_id]+'\r\nПроблема: '+problem[user_id]+'')
        bot.send_message(c.message.chat.id, 'Выберите, что хотите изменить:', reply_markup=keyboard_edit())
    elif c.data == "name": # изменение имени
        rows = mssql.select_user(user_id)
        bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text='Ваше имя: '+name[user_id]+'\r\nКонтактный телефон: '+tele[user_id]+'\r\nИНН: '+inn[user_id]+'\r\nАдрес: '+adress[user_id]+'\r\nПроблема: '+problem[user_id]+'')
        bot.send_message(user_id, 'Выберите или введите новое имя:', reply_markup=keyboard_sql(rows, c.message, 'name'))
        bot.register_next_step_handler(c.message, lambda msg: get_name("1", msg))
    elif c.data == "phone_number": # изменение тел номера
       rows = mssql.select_user(user_id)
       bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text='Ваше имя: '+name[user_id]+'\r\nКонтактный телефон: '+tele[user_id]+'\r\nИНН: '+inn[user_id]+'\r\nАдрес: '+adress[user_id]+'\r\nПроблема: '+problem[user_id]+'')
       bot.send_message(user_id, 'Выберите или введите новый номер телефона:', reply_markup=keyboard_sql(rows, c.message, 'cont'))
       bot.register_next_step_handler(c.message, lambda msg: get_phone("1", msg))
    elif c.data == "inn": # изменение ИНН
       rows = mssql.select_inn(user_id)
       bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text='Ваше имя: '+name[user_id]+'\r\nКонтактный телефон: '+tele[user_id]+'\r\nИНН: '+inn[user_id]+'\r\nАдрес: '+adress[user_id]+'\r\nПроблема: '+problem[user_id]+'')
       bot.send_message(user_id, 'Выберите или введите новый ИНН:', reply_markup=keyboard_sql(rows, c.message, '0'))
       bot.register_next_step_handler(c.message, lambda msg: get_inn("1", msg))
    elif c.data == "adress": # изменение адреса
       rows = mssql.select_adress(user_id)
       bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text='Ваше имя: '+name[user_id]+'\r\nКонтактный телефон: '+tele[user_id]+'\r\nИНН: '+inn[user_id]+'\r\nАдрес: '+adress[user_id]+'\r\nПроблема: '+problem[user_id]+'')
       bot.send_message(user_id, 'Выберите или введите новый адрес:', reply_markup=keyboard_sql(rows, c.message, '0'))
       bot.register_next_step_handler(c.message, lambda msg: get_adress("1", msg))
    elif c.data == "problem": # изменение проблемы
       bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text='Ваше имя: '+name[user_id]+'\r\nКонтактный телефон: '+tele[user_id]+'\r\nИНН: '+inn[user_id]+'\r\nАдрес: '+adress[user_id]+'\r\nПроблема: '+problem[user_id]+'')
       bot.send_message(user_id, 'Новое описание:')
       bot.register_next_step_handler(c.message, lambda msg: get_problem("1", msg))
    elif c.data == "del_user": # удалить Имя и телефон
       rows = mssql.select_user(user_id)
       if(rows):
           bot.send_message(user_id, 'Выберите что удалить:', reply_markup=keyboard_sql(rows, c.message, '0'))
           bot.register_next_step_handler(c.message, del_user)
       else:
           bot.delete_message(chat_id=c.message.chat.id, message_id=c.message.message_id)
           bot.send_message(user_id, 'У Вас нет сохраненных данных.', reply_markup=keyboard())
    elif c.data == "del_inn": # удалить ИНН
       rows = mssql.select_inn(user_id)
       if(rows):
           bot.send_message(user_id, 'Выберите что удалить:', reply_markup=keyboard_sql(rows, c.message, '0'))
           bot.register_next_step_handler(c.message, del_inn)
       else:
           bot.delete_message(chat_id=c.message.chat.id, message_id=c.message.message_id)
           bot.send_message(user_id, 'У Вас нет сохраненных ИНН.', reply_markup=keyboard())
    elif c.data == "del_adress": # удалить адрес
       rows = mssql.select_adress(user_id)
       if(rows):
           bot.send_message(user_id, 'Выберите что удалить:', reply_markup=keyboard_sql(rows, c.message, '0'))
           bot.register_next_step_handler(c.message, del_adress)
       else:
           bot.delete_message(chat_id=c.message.chat.id, message_id=c.message.message_id)
           bot.send_message(user_id, 'У Вас нет сохраненных адресов.', reply_markup=keyboard())

    elif c.data == "main_menu": # в главное меню ⏎
       bot.send_message(user_id, 'главное меню ⏎', reply_markup=keyboard())
       bot.delete_message(chat_id=c.message.chat.id, message_id=c.message.message_id)



    chat_id = c.message.chat.id
    bot.answer_callback_query(c.id, text="")

while True:
    try:
        #bot.polling(none_stop=True)
        bot.infinity_polling(none_stop=True, interval=1)
    except Exception as e:
        print(e)
        time.sleep(10)


