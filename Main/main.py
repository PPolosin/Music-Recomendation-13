# Version 1.0
# by PPolosin
# Imports
import telebot
from telebot import types
from fuzzywuzzy import process
# Globals
rules = []
artists = []
bot = telebot.TeleBot('2113720605:AAFvb5uTGnh2lChcW6M9SqSpxeFHLdQL9GQ')
last_index = 0
new_db = "new_data.txt"


def init_rules(path):
    f = open(path, encoding='UTF-8')
    rules = []
    for line in f:
        line = line.strip()
        tmp = line.split(',')
        rules.append([tmp[0], tmp[1]])
        artists.append(tmp[0])
        artists.append(tmp[1])

    return rules


def get_recommendation(artist, index=0):
    for i in range(index, len(rules)):
        if rules[i][0] == artist:
            return [rules[i][1], i]
    else:
        return ["NAN"]


rules = init_rules("rules_v1.txt")
artists = list(set(artists))
url = 'https://www.youtube.com/results?search_query=official+music+video'

@bot.message_handler(content_types=['text'])
def complete_request(message):
    global last_index
    request = message.text
    search = list(process.extractOne(request, artists))
    user_artist = search[0]
    recommendation = get_recommendation(user_artist)

    if recommendation[0] == "NAN":
        bot.send_message(message.from_user.id, "Возможно Вам понравится: Nan")
        print("nan")
    else:
        last_index = recommendation[1]
        if (search[1] > 95):
            keyboard = types.InlineKeyboardMarkup()

            key_new_rec = types.InlineKeyboardButton(text='Еще варианты', callback_data='new')
            keyboard.add(key_new_rec)

            key_like = types.InlineKeyboardButton(text=u'👍', callback_data='like')
            keyboard.add(key_like)

            key_dislike = types.InlineKeyboardButton(text=u'👎', callback_data='dislike')
            keyboard.add(key_dislike)

            answer = "Возможно Вам понравится:\n " + url + str(recommendation[0]).replace(" ", "")
            bot.send_message(message.from_user.id, answer, reply_markup=keyboard)
        else:
            keyboard = types.InlineKeyboardMarkup()

            key_new_rec = types.InlineKeyboardButton(text='Еще варианты', callback_data='new')
            keyboard.add(key_new_rec)

            key_like = types.InlineKeyboardButton(text=u'👍', callback_data='like')
            keyboard.add(key_like)

            key_dislike = types.InlineKeyboardButton(text=u'👎', callback_data='dislike')
            keyboard.add(key_dislike)

            answer = 'Возможно вы имели в виду "'  + str(user_artist) + '".' + "\nВам понравится:\n " + url + str(recommendation[0]).replace(" ", "")
            bot.send_message(message.from_user.id, answer, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "new":
        global last_index
        request = call.message.text
        search = list(process.extractOne(request, artists))
        user_artist = search[0]
        recommendation = get_recommendation(user_artist, last_index)

        if recommendation[0] == "NAN":
            last_index = 0
            bot.send_message(call.message.chat.id, "Возможно Вам понравится: Nan")
            print("nan")
        else:
            keyboard = types.InlineKeyboardMarkup()

            key_new_rec = types.InlineKeyboardButton(text='Еще варианты', callback_data='new')
            keyboard.add(key_new_rec)

            key_like = types.InlineKeyboardButton(text=u'👍', callback_data='like')
            keyboard.add(key_like)

            key_dislike = types.InlineKeyboardButton(text=u'👎', callback_data='dislike')
            keyboard.add(key_dislike)

            answer = "Возможно Вам понравится:\n " + url + str(recommendation[0]).replace(" ", "")
            bot.send_message(call.message.chat.id, answer, reply_markup=keyboard)

    elif call.data == "dislike":
        ans = "Спасибо! Вы помогаете улучшать наш сервис. "
        bot.send_message(call.message.chat.id, ans)
    elif call.data == "like":
        f = open(new_db, 'a')
        new_line = "\n" + str(call.message.chat.id) + "," + rules[last_index][1]
        f.write(new_line)
        f.close()
        ans = "Спасибо! Вы помогаете улучшать наш сервис. "
        bot.send_message(call.message.chat.id, ans)

bot.polling(none_stop=True, interval=0)
