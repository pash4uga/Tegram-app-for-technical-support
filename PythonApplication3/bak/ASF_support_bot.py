import telebot
import sqlite3
import time
import mssql
from telebot import types
from mycheck import inn_check
from mycheck import formatStr
from telebot import apihelper

apihelper.proxy = {'https': 'socks5h://127.0.0.1:9150'}
#apihelper.proxy = {'https': 'socks5h://34.76.159.209:80'}
TOKEN = '1095944337:AAHUzqbcZPNOyAB5L3Wilu9ofumQYxAcPB4'
bot  = telebot.TeleBot(TOKEN);

mssql.create()

# --------------------------------------------функции клавиатур------------------------------------------------------
hide_markup = telebot.types.ReplyKeyboardRemove()

def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.InlineKeyboardButton('Главное меню')
    markup.add(btn1)
    return markup

def keyboard_ok():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.InlineKeyboardButton('Ok')
    markup.add(btn1)
    return markup

def keyboard_phone():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton(text='Отправить мой номер телефона', request_contact=True)
    markup.add(btn1)
    return markup

def keyboard_adress():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton(text='Отправить мой текущий адрес', request_location=True)
    markup.add(btn1)
    return markup

def keyboard_name(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton(text=''+str(message.chat.first_name)+'')
    markup.add(btn1)
    return markup

def keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Подать заявку')
    btn2 = types.KeyboardButton('Cтатус заявки')
    markup.add(btn1, btn2)
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

def keyboard_yesno():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton ( text = 'Отправить' , callback_data= 'send'  )
    btn2 = types.InlineKeyboardButton ( text = 'Изменить' , callback_data= 'edit'  )
    markup.add (btn1, btn2)
    return markup


#----------------------------------------------call-бэки клавиатыр--------------------------------------
@bot.callback_query_handler(func=lambda c:c.data)
def callback_inline(c):
    if c.data == "send":
        bot.send_message(c.message.chat.id, 'Заявка оформлена.\r\nСпасибо!', reply_markup=keyboard())
        bot.send_message(c.message.chat.id, 'Ах да... отправлять то мне куда :) Так что звоните как и раньше, 280-780')
        bot.send_message("-372849868", 'Ваше имя: '+name+'\r\nКонтактный телефон: '+tele+'\r\nИНН: '+inn+'\r\nАдрес: '+adress+'\r\nПроблема: '+problem+'')
        bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text='Ваше имя: '+name+'\r\nКонтактный телефон: '+tele+'\r\nИНН: '+inn+'\r\nАдрес: '+adress+'\r\nПроблема: '+problem+'')

    elif c.data == "edit":
        bot.send_message(c.message.chat.id, 'Выберите, что хотите изменить:', reply_markup=keyboard_edit())
        bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text='Ваше имя: '+name+'\r\nКонтактный телефон: '+tele+'\r\nИНН: '+inn+'\r\nАдрес: '+adress+'\r\nПроблема: '+problem+'')
    elif c.data == "name": # изменение имени
        bot.send_message(c.from_user.id, 'Новое имя:', reply_markup=keyboard_name(c.message))
        bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text='Ваше имя: '+name+'\r\nКонтактный телефон: '+tele+'\r\nИНН: '+inn+'\r\nАдрес: '+adress+'\r\nПроблема: '+problem+'')
        bot.register_next_step_handler(c.message, lambda msg: get_name("1", msg))
    elif c.data == "phone_number": # изменение тел номера
       bot.send_message(c.from_user.id, 'Новый телефон:', reply_markup=keyboard_phone())
       bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text='Ваше имя: '+name+'\r\nКонтактный телефон: '+tele+'\r\nИНН: '+inn+'\r\nАдрес: '+adress+'\r\nПроблема: '+problem+'')
       bot.register_next_step_handler(c.message, lambda msg: get_phone("1", msg))
    elif c.data == "inn": # изменение ИНН
       bot.send_message(c.from_user.id, 'Новый ИНН:')
       bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text='Ваше имя: '+name+'\r\nКонтактный телефон: '+tele+'\r\nИНН: '+inn+'\r\nАдрес: '+adress+'\r\nПроблема: '+problem+'')
       bot.register_next_step_handler(c.message, lambda msg: get_inn("1", msg))
    elif c.data == "adress": # изменение адреса
       bot.send_message(c.from_user.id, 'Новый адрес:')
       bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text='Ваше имя: '+name+'\r\nКонтактный телефон: '+tele+'\r\nИНН: '+inn+'\r\nАдрес: '+adress+'\r\nПроблема: '+problem+'')
       bot.register_next_step_handler(c.message, lambda msg: get_adress("1", msg))
    elif c.data == "problem": # изменение проблемы
       bot.send_message(c.from_user.id, 'Новое описание:')
       bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text='Ваше имя: '+name+'\r\nКонтактный телефон: '+tele+'\r\nИНН: '+inn+'\r\nАдрес: '+adress+'\r\nПроблема: '+problem+'')
       bot.register_next_step_handler(c.message, lambda msg: get_problem("1", msg))
    elif c.data == "send_reque":
        bot.send_message(c.message.chat.id, 'Ты !')
    chatiid = c.message.chat.id
    bot.answer_callback_query(c.id, text="")

#-------------------------------------сам бот----------------------------------------------------------------
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.from_user.id, 'Добро пожаловать, '+str(message.from_user.first_name)+'!\r\nЭто в помощник оформления заявок в АСФ.\r\nВыберите желаемое действие кнопками ниже.', reply_markup=keyboard())
       
@bot.message_handler(content_types=['text'])
def start(message):
    if (message.text == 'Подать заявку'):
        bot.send_message(message.from_user.id, "Как Вас зовут?", reply_markup=keyboard_name(message))
        bot.register_next_step_handler(message, lambda msg: get_name("0", msg)) #следующий шаг – функция get_name
    elif (message.text == 'Cтатус заявки'):
        bot.send_message(message.from_user.id, "Упсс... в КИС дорога пока закрыта....(", reply_markup=main_keyboard())
    else:
        bot.send_message(message.from_user.id, 'Главное меню, выберите действие кнопками ниже', reply_markup = keyboard())
    

def get_name(edit, message): #получаем имя
    global name
    if (message.text == 'Главное меню'):
        start(message)
    elif (edit == '1'):
        bot.send_message(message.chat.id, 'Имя изменено', reply_markup=main_keyboard())
        name = message.text
        bot.send_message(message.from_user.id, 'Ваше имя: '+name+'\r\nКонтактный телефон: '+tele+'\r\nИНН: '+inn+'\r\nАдрес: '+adress+'\r\nПроблема: '+problem+'', reply_markup=keyboard_yesno())

    elif(edit == '0'): 
        bot.send_message(message.chat.id, "Введите номер телефона или используйте текущий", reply_markup=keyboard_phone())
        name = message.text
        bot.register_next_step_handler(message, lambda msg: get_phone("0", msg))
    
def get_phone (edit, message): #получаем телефон
    if (message.text == 'Главное меню'):
        start(message)
    global tele
    if (message.content_type == "contact"):
        phone = message.contact.phone_number
    else:
        phone = message.text
    tele = formatStr(phone)
    if (edit == '1'):
        if (tele):
            bot.send_message(message.chat.id, 'Номер изменен', reply_markup=main_keyboard())
            bot.send_message(message.from_user.id, 'Ваше имя: '+name+'\r\nКонтактный телефон: '+tele+'\r\nИНН: '+inn+'\r\nАдрес: '+adress+'\r\nПроблема: '+problem+'', reply_markup=keyboard_yesno())
        else:
            bot.send_message(message.from_user.id, 'Введите правильный номер!', reply_markup=keyboard_phone())
            bot.register_next_step_handler(message, lambda msg: get_phone("1", msg))
    elif (edit == '0'):
        if (tele):
            bot.send_message(message.from_user.id, 'Ваш ИНН?')
            bot.register_next_step_handler(message, lambda msg: get_inn("0", msg))
        else:
            bot.send_message(message.from_user.id, 'Введите правильный номер!', reply_markup=keyboard_phone())
            bot.register_next_step_handler(message, lambda msg: get_phone("0", msg))

def get_inn (edit, message): #получаем ИНН
    global inn
    if (message.text == 'Главное меню'):
        start(message)
    elif (edit == '1'):
        inn = message.text
        ckinn = inn_check(inn)
        if (ckinn):
            bot.send_message(message.chat.id, 'ИНН изменен', reply_markup=main_keyboard())
            bot.send_message(message.from_user.id, 'Ваше имя: '+name+'\r\nКонтактный телефон: '+tele+'\r\nИНН: '+inn+'\r\nАдрес: '+adress+'\r\nПроблема: '+problem+'', reply_markup=keyboard_yesno())
        else:
            bot.send_message(message.from_user.id, 'Не корректный ИНН, введите заново!')
            bot.register_next_step_handler(message, lambda msg: get_inn("1", msg))
    elif (edit == '0'):
        inn = message.text
        ckinn = inn_check(inn)
        if (ckinn):
            bot.send_message(message.from_user.id, 'Введите адрес', reply_markup=hide_markup)
            bot.register_next_step_handler(message, lambda msg: get_adress("0", msg))
        else:
            bot.send_message(message.from_user.id, 'Не корректный ИНН, введите заново!')
            bot.register_next_step_handler(message, lambda msg: get_inn("0", msg))

def get_adress(edit, message): #получаем адрес
    if (message.text == 'Главное меню'):
        start(message)
    global adress
    if (edit == '1'):
        bot.send_message(message.chat.id, 'Адрес изменен', reply_markup=main_keyboard())
        adress = message.text
        bot.send_message(message.from_user.id, 'Ваше имя: '+name+'\r\nКонтактный телефон: '+tele+'\r\nИНН: '+inn+'\r\nАдрес: '+adress+'\r\nПроблема: '+problem+'', reply_markup=keyboard_yesno())

    elif(edit == '0'): 
        bot.send_message(message.chat.id, "Опишите проблему", reply_markup=hide_markup)
        adress = message.text
        bot.register_next_step_handler(message, lambda msg: get_problem("0", msg))


def get_problem (edit, message): # описание завки
    global problem
    if (message.text == 'Главное меню'):
        start(message)
    elif (edit == '1'):
        bot.send_message(message.chat.id, 'Описание изменнено', reply_markup=main_keyboard())
        problem = message.text
        bot.send_message(message.from_user.id, 'Ваше имя: '+name+'\r\nКонтактный телефон: '+tele+'\r\nИНН: '+inn+'\r\nАдрес: '+adress+'\r\nПроблема: '+problem+'', reply_markup=keyboard_yesno())
    elif (edit == '0'):
        problem = message.text
        bot.send_message(message.from_user.id, 'Ваше имя: '+name+'\r\nКонтактный телефон: '+tele+'\r\nИНН: '+inn+'\r\nАдрес: '+adress+'\r\nПроблема: '+problem+'', reply_markup=keyboard_yesno())
        


while True:
    try:
        bot.polling(none_stop=True, interval=1, timeout=5)
    except Exception as e:
        print(e)
        time.sleep(10)
