# -*- coding: utf-8 -*-
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup
import os
import xlrd
import glob

try:
    os.mkdir('C:\\Users\\User\\PycharmProjects\\CowPoke_GoTo\\list\\')
except:
    pass
workspace = 'C:\\Users\\User\\PycharmProjects\\CowPoke_GoTo\\list\\'

REQUEST_KWARGS = {'proxy_url': 'socks5://t.geekclass.ru:7777',
                  'urllib3_proxy_kwargs': {
                      'username': 'geek',
                      'password': 'socks',
                  }}
def sortByAlphabet(inputStr):
    return inputStr[0]


def settler(base):
    print("УПОРОШКИИИИИИИ")
    boys = []
    girls = []
    s = os.listdir(base)
    s.sort(key=sortByAlphabet)
    sex = ''
    for d in s:
        e = open(base + d, 'r')
        for i, line in enumerate(e):
            if i == 0:
                age = int(line[:len(line) - 1])
            elif i == 1:
                sex = str(line)[0]
            else:
                break
        if sex.lower() == "м":
            boys.append([int(age), ' '.join(d.split('_'))])
        elif sex.lower() == "ж":
            girls.append([int(age), ' '.join(d.split('_'))])
    boys.sort(key=sortByAlphabet)
    girls.sort(key=sortByAlphabet)
    return boys, girls

def rooms(boys, girls, b, g, type1, type2):
    tempure = []
    spred = {}
    cnt = 0
    k = 3
    j = 0

    if (type1 * 4) + (type2 * 3) < b + g:
        return -1

    for i in range(b):
        print(tempure)
        if cnt < k:
            tempure.append(boys[i][1])
            cnt += 1
            continue
        else:
            cnt = 0
            type1 = type1 - 1
            j += 1
            paper = list(tempure)
            spred[j] = paper
            print(paper)
            tempure.clear()
            if type1 == 0:
                k = 4
                type1 = type2
        tempure.append(boys[i][1])
        cnt += 1

    if tempure:
        cnt = 0
        type1 = type1 - 1
        j = j + 1
        paper = list(tempure)
        spred[j] = paper
        tempure.clear()
        if type1 == 0:
            k = 4
            type1 = type2

    if len(spred.get(j)) == 1:
        a = spred.get(j - 1)[1]
        spred.get(j).append(a)
        del spred.get(j - 1)[1]

    for i in range(g):
        if cnt < k:
            tempure.append(girls[i][1])
            cnt += 1
            continue
        else:
            cnt = 0
            type1 = type1 - 1
            j = j + 1
            paper = list(tempure)
            spred[j] = paper
            tempure.clear()
            if type1 == 0:
                k = 4
                type1 = type2
        tempure.append(girls[i][1])
        cnt += 1
    if tempure:
        cnt = 0
        type1 = type1 - 1
        j = j + 1
        paper = list(tempure)
        spred[j] = paper
        tempure.clear()
        if (type1 == 0):
            k = 4
            type1 = type2

    if len(spred.get(j)) == 1:
        a = spred.get(j - 1)[1]
        spred.get(j).append(a)
        del spred.get(j - 1)[1]

    return spred


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="""Здравствуй, кто бы ты ни был! :)
Я помогу тебе распределить людей по группам!
Для начала нужно загрузить список всех участников с их личными данными (ФИО, возраст, пол, комната, направление, комментарий)""")


def link(bot, update):
    doc = bot.getFile(update.message.document.file_id)
    ufr = bot.request._request_wrapper('GET',
                                       doc.file_path
                                       )
    f = open('{}\doc.xlsx'.format(os.getcwd()), "wb")
    f.write(ufr)
    f.close()

    r = glob.glob(workspace + "*")
    for i in r:
        os.remove(i)

    wb = xlrd.open_workbook("doc.xlsx")
    sheet = wb.sheet_by_index(0)
    for m in range(0, sheet.nrows):
        name = ('_'.join(sheet.cell_value(m, 0).split()) + ".txt").lower()
        activephile = open(workspace + name, 'w')
        activephile.write(sheet.cell_value(m, 1) + '\n')  # возраст
        activephile.write(sheet.cell_value(m, 2) + '\n')  # пол маккартни
        activephile.write(sheet.cell_value(m, 3) + '\n')  # комната
        activephile.write(sheet.cell_value(m, 4) + '\n')  # направление
        activephile.write(sheet.cell_value(m, 5) + '\n')  # комментарий

    reply_keyboard = [['Комнаты', 'Мероприятие', 'Свечки']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text("А теперь выбери тип сортировки", reply_markup=markup)


def filter(bot, update):
    message = update.message.text
    try:
        n = int(message)
    except:
        pass
    if message == 'Свечки':
        update.message.reply_text("Отлично! Какое количество команд?")
    elif message == 'Мероприятие':
        update.message.reply_text("Хорошо. Сколько будет команд?")
    elif message == 'Комнаты':
        print(1)
        boys, girls = settler(workspace)
        print(boys)
        print(girls)
        # update.message.reply_text("Сколько парней, девушек на смене? Сколько трёхместный и четырёхместных домов? Ввести в формате <n1 n2 n3 n4>")
        print(rooms(boys, girls, 41, 4, 6, 8))
    elif message.lower() == 'да':
        r = glob.glob(workspace + "*")
        for i in r:
            os.remove(i)


def list(bot, update):
    lon = os.listdir(workspace)
    if len(lon) > 0:
        new = []
        for j in lon:
            k = j.split('_')
            new.append(' '.join(k[:-1]) + ' ' + k[-1][:-4])
        new.sort(key=sortByAlphabet)
        output = []
        for j in new:
            l = ''
            for k in j.split():
                l += k[0].upper() + k[1:] + ' '
            l += '\n'
            output.append(l)
        update.message.reply_text(''.join(output))

    else:
        update.message.reply_text("Пока что нет участников")


def add(bot, update, args):
    memory = args[3:]
    activephile = open(str(workspace + args[0] + '_' + args[1] + '_' + args[2][:-1] + '.txt'), 'w')
    print(len(memory))
    for j in range(len(memory)):
        print(j)
        if j != len(memory) - 1:
            activephile.write(memory[j][:-1] + '\n')
        else:
            activephile.write(memory[j])


def count(bot, update):
    n = update.message.text
    update.message.reply_text('{}'.format(n))


def remove(bot, update, args):
    name = '_'.join(args).lower() + '.txt'
    os.remove(workspace + name)


def view(bot, update, args):
    name = '_'.join(args).lower() + '.txt'
    if os.path.isfile(workspace + name):
        activephile = open(str(workspace + name), 'r')
        new_activephile = activephile.read().split('\n')[:-1]
        update.message.reply_text(
            'Возраст: ' + new_activephile[0] + '\n' + 'Пол: ' + new_activephile[1] + '\n' + 'Комната: ' +
            new_activephile[2] + '\n' + 'Направление: ' + new_activephile[3] + '\n' + 'Комментарий: ' + new_activephile[
                4])


def clear(bot, update):
    update.message.reply_text('Погоди, уверен? Да/Нет')



updater = Updater(token='820418482:AAFuEdJLEx82e6N8x-IKytz_r2JbqvtrX2U', request_kwargs=REQUEST_KWARGS)

start_handler = CommandHandler('start', start)
document = MessageHandler(Filters.document, link)
clear_data = CommandHandler('clear', clear)
full_list = CommandHandler('list', list)
add_pupil = CommandHandler('add', add, pass_args=True)
view_pupil = CommandHandler('view', view, pass_args=True)
remove_pupil = CommandHandler('remove', remove, pass_args=True)
filter_text = MessageHandler(Filters.text, filter)

updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(document)
updater.dispatcher.add_handler(filter_text)
updater.dispatcher.add_handler(clear_data)
updater.dispatcher.add_handler(full_list)
updater.dispatcher.add_handler(add_pupil)
updater.dispatcher.add_handler(view_pupil)
updater.dispatcher.add_handler(remove_pupil)
updater.start_polling()
updater.idle()
