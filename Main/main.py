# Version 1.0
# Imports
import telebot
from telebot import types
from fuzzywuzzy import process
import sqlite3
from googletrans import Translator, constants
import random


# Globals
rules = []
artists_additional = []
geners = []
artists = []
bot = telebot.TeleBot("")
last_index = 0
new_db = "new_data.txt"
url = 'https://www.youtube.com/results?search_query=official+music+video'
translator = Translator()
user_genre = ""
tmp_message = ''
def get_recommendation(user_artist):
    con = sqlite3.connect('new_data/new_rules_sql.db')
    cur = con.cursor()
    row = cur.execute('SELECT * FROM project WHERE target = (?)', [user_artist])
    return (list(row))
def init_artists_2(path):
    f = open(path, encoding='UTF-8')
    for line in f:
        line = line.replace("\n", "")
        line = line.split(",")
        new_tmp = []
        new_tmp.append(line[0])
        new_tmp.append(line[1])
        artists_additional.append(new_tmp)
        geners.append(line[1])

def init_artists(path):
    f = open(path, encoding='UTF-8')
    for line in f:
        line = line.strip()
        tmp = line.split(',')
        artists.append(tmp[0])
        artists.append(tmp[1])
    return artists

def return_all_recommendation(lst):
    s = ""
    cnt = 1
    for el in lst:
        if (len(s) < 3500):
            s += str(cnt) + ". " + url + str(el[1]).replace(" ", "a")
            s += "\n"
            cnt+=1
    return s



artists = init_artists("new_data/new_associative_rules_2.txt")
artists = list(set(artists))
init_artists_2("new_data/add_artists_with_genre.txt")

geners = list(set(geners))


global_genere_queue = {}
tmp_message = ''
print("Total additional geners:", len(geners))
print("Total artists: ", len(artists))
@bot.message_handler(content_types=['text'])
def complete_request(message):

    global last_index
    request = message.text
    #geners[message.chat.id] = None
    if request == "/genre":
        bot.send_message(message.from_user.id, "Введите предпочитаемый жанр: ")
        bot.register_next_step_handler(message, get_genre)
    else:
        search = list(process.extractOne(request, artists))
        user_artist = search[0]
        print(search[1])
        if (search[1] > 65):

            recommendation = get_recommendation(user_artist)
            recommendation_to_user = return_all_recommendation(recommendation)
            print(len(return_all_recommendation(recommendation)))
        else:
            recommendation = 0
        if (recommendation) == 0:
            keyboard = types.InlineKeyboardMarkup()
            key_new_rec = types.InlineKeyboardButton(text='Я не нашел того, чего искал', callback_data='new')
            keyboard.add(key_new_rec)
            bot.send_message(message.from_user.id, "Упс...Еще нет сформированных правил для данного исполнителя(или попробуйте правильно ввести имя исполнителя), попробуйте что-то другое.", reply_markup=keyboard)
            print("nan")
        else:

            if search[1] > 95:

                keyboard = types.InlineKeyboardMarkup()

                key_new_rec = types.InlineKeyboardButton(text='Я не нашел того, чего искал', callback_data='new')
                keyboard.add(key_new_rec)

                key_like = types.InlineKeyboardButton(text=u'👍', callback_data='like')
                keyboard.add(key_like)

                key_dislike = types.InlineKeyboardButton(text=u'👎', callback_data='dislike')
                keyboard.add(key_dislike)

                answer = search[0] + " Возможно Вам понравится:\n " + url + recommendation_to_user
                bot.send_message(message.from_user.id, answer, reply_markup=keyboard)
            else:
                keyboard = types.InlineKeyboardMarkup()

                key_new_rec = types.InlineKeyboardButton(text='Я не нашел того, чего искал', callback_data='new')
                keyboard.add(key_new_rec)

                key_like = types.InlineKeyboardButton(text=u'👍', callback_data='like')
                keyboard.add(key_like)

                key_dislike = types.InlineKeyboardButton(text=u'👎', callback_data='dislike')
                keyboard.add(key_dislike)

                answer = 'Возможно вы имели в виду "' + str(user_artist) + '".' + "\nВам понравится:\n " + recommendation_to_user
                bot.send_message(message.from_user.id, answer, reply_markup=keyboard)


def get_genre(message):
    global user_genre
    #if global_genere_queue[message.chat.id] == None:
    request = message.text
    request = str(request)
    translation = translator.translate(request)
    # print(translation.text)
    search = list(process.extractOne(translation.text, geners))
    global_genere_queue[message.chat.id] = search[0]
    #else:
        #search = [global_genere_queue[message.chat.id]]

    new = []
    #print("Here", search[0])
    for el in artists_additional:
        if el[1] == search[0]:
            new.append(el)
    #print(new)
    keyboard = types.InlineKeyboardMarkup()
    key_like = types.InlineKeyboardButton(text=u'👍', callback_data='like')
    keyboard.add(key_like)

    key_dislike = types.InlineKeyboardButton(text=u'👎', callback_data='dislike_2')
    keyboard.add(key_dislike)


    key_another_genre = types.InlineKeyboardButton(text='Выбрать другой жанр', callback_data='new')
    keyboard.add(key_another_genre)

def get_genre(message):
    global user_genre
    global tmp_message
    # if global_genere_queue[message.chat.id] == None:
    request = message.text
    request = str(request)
    translation = translator.translate(request)
    # print(translation.text)
    search = list(process.extractOne(translation.text, geners))
    global_genere_queue[message.chat.id] = search[0]
    # else:
    # search = [global_genere_queue[message.chat.id]]
    user_genre = search[0]
    tmp_message = message
    new = []
    # print("Here", search[0])
    for el in artists_additional:
        if el[1] == search[0]:
            new.append(el)
    # print(new)
    keyboard = types.InlineKeyboardMarkup()
    key_like = types.InlineKeyboardButton(text=u'👍', callback_data='like')
    keyboard.add(key_like)

    key_dislike = types.InlineKeyboardButton(text=u'👎', callback_data='dislike_2')
    keyboard.add(key_dislike)

    key_another_genre = types.InlineKeyboardButton(text='Выбрать другой жанр', callback_data='new')
    keyboard.add(key_another_genre)


    answer = "GENRE: " + "["+ search[0] +"]" "\n" +"Пожалуйста, оцените рекомендацию: " + "\n" + url + new[random.randint(0, len(new)-1)][0] + "\n" + "Чтобы попробовать найти другую композицию похожего жанра, нажмите на 👎."
    bot.send_message(message.from_user.id, answer, reply_markup=keyboard)

def get_genre_repeat(message):
    search = [user_genre]
    print("HERE", search)
    new = []
    # print("Here", search[0])
    for el in artists_additional:
        if el[1] == search[0]:
            new.append(el)
    # print(new)
    keyboard = types.InlineKeyboardMarkup()
    key_like = types.InlineKeyboardButton(text=u'👍', callback_data='like')
    keyboard.add(key_like)

    key_dislike = types.InlineKeyboardButton(text=u'👎', callback_data='dislike_2')
    keyboard.add(key_dislike)

    key_another_genre = types.InlineKeyboardButton(text='Выбрать другой жанр', callback_data='new')
    keyboard.add(key_another_genre)

    answer = "GENRE: " + "[" + search[0] + "]" "\n" + "Пожалуйста, оцените рекомендацию: " + "\n" + url + \
             new[random.randint(0, len(new) - 1)][
                 0] + "\n" + "Чтобы попробовать найти другую композицию похожего жанра, нажмите на 👎."
    bot.send_message(message.from_user.id, answer, reply_markup=keyboard)

    bot.send_message(message.from_user.id, search[0])
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):

    if call.data == "new":
        keyboard = types.InlineKeyboardMarkup()
        key_new_random= types.InlineKeyboardButton(text='Я не определился. Выбрать случайный', callback_data='random')
        keyboard.add(key_new_random)
        global_genere_queue[call.message.chat.id] = None
        ans = "Перейти к выбору жанрна, нажав на /genre "

        bot.send_message(call.message.chat.id, ans, reply_markup=keyboard)

    elif call.data == "dislike":
        ans = "Спасибо! Вы помогаете улучшать наш сервис. "
        bot.send_message(call.message.chat.id, ans)
    elif call.data == "dislike_2":
        get_genre_repeat(tmp_message)
    elif call.data == "like":
        f = open(new_db, 'a')
        new_line = "\n" + str(call.message.chat.id) + ","
        f.write(new_line)
        f.close()
        ans = "Спасибо! Вы помогаете улучшать наш сервис. "
        bot.send_message(call.message.chat.id, ans)
    if call.data == "random":
        new  = []
        random_genre = geners[random.randint(0, len(geners)-1)]
        for el in artists_additional:
            if el[1] == random_genre:
                new.append(el)

        keyboard = types.InlineKeyboardMarkup()
        key_like = types.InlineKeyboardButton(text=u'👍', callback_data='like')
        keyboard.add(key_like)

        key_another_genre = types.InlineKeyboardButton(text='Выбрать другой жанр', callback_data='new')
        keyboard.add(key_another_genre)

        answer = "GENRE: " + "[" + random_genre + "]" "\n" + "Пожалуйста, оцените рекомендацию: " + "\n" + url + \
                 new[random.randint(0, len(new) - 1)][
                     0]
        bot.send_message(call.message.chat.id, answer, reply_markup=keyboard)


bot.polling(none_stop=True, interval=0)
