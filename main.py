import random
import telebot
import time
from config import TOKEN

bot = telebot.TeleBot(TOKEN)
tasks = dict()
RANDOM_TASKS = []
HELP = """
Список команд:
/help - отобразить справку по программе,
/add - добавить задачу в список в формате /add {Название задачи} {Дата выполнения (DD.MM.YYYY)},
/show - отобразить все добавленные задачи в формате /show {Дата выполнения (DD.MM.YYYY)},
/choose_random - выбрать случайную задачу на Сегодня,
/add_random - добавить задачу в список случайных задач в формате /add_random {Название задачи},
/remove - удалить задачу из списка в формате /remove {Название задачи} {Дата выполнения (DD.MM.YYYY)}."""


def add_todo(date, task):
    date = date.lower()
    if tasks.get(date) is not None:
        tasks[date].append(task)
    else:
        tasks[date] = [task]


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Чтобы отобразить список доступных команд, введите команду /help")


@bot.message_handler(commands=['help'])
def help(message):
    try:
        bot.send_message(message.chat.id, HELP)
    except Exception:
            bot.send_message(message.chat.id, "Неверный формат команды!")

@bot.message_handler(commands=['show'])
def show(message):
    try:
        date = message.text.split()[1]
        try:
            if date.lower() != 'сегодня':
                valid_date = time.strptime(date, '%d/%m/%Y')
        except ValueError:
            bot.send_message(message.chat.id, "Неверный формат даты!")
            return
        if date in tasks:
            todos = ''
            for task in tasks[date]:
                todos += f'- {task}\n'
            if todos == '':
                bot.send_message(message.chat.id, f"Нет задач на {date}!")
        else:
            todos = 'Такой даты нет!'
        bot.send_message(message.chat.id, todos)
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "Неверный формат команды!")


@bot.message_handler(commands=['add'])
def add(message):
    try:
        _, task_name, date = message.text.split(maxsplit=2)
        try:
            valid_date = time.strptime(date, '%d/%m/%Y')
        except ValueError:
            bot.send_message(message.chat.id, "Неверный формат даты!")
            return
        task = ' '.join([task_name])
        add_todo(date, task)
        bot.send_message(message.chat.id, f'Задача "{task}" добавлена на дату {date}!')
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "Неверный формат команды!")


@bot.message_handler(commands=['add_random'])
def add_random(message):
    try:
        new_random_task = message.text.split()[1].lower()
        RANDOM_TASKS.append(new_random_task)
        bot.send_message(message.chat.id, f'Случайная задача "{new_random_task}" успешно добавлена!')
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "Неверный формат команды!")


@bot.message_handler(commands=['choose_random'])
def choose_random(message):
    try:
        if len(RANDOM_TASKS) == 0:
            bot.send_message(message.chat.id, "Список случайных задач пуст!\nЧтобы добавить задачу, используйте команду /add {Дата выполнения (DD.MM.YYYY)} {Название задачи}")
        else:
            random_task = random.choice(RANDOM_TASKS)
            add_todo("Сегодня", random_task)
            RANDOM_TASKS.remove(random_task)
            bot.send_message(message.chat.id, f'Случайная задача "{random_task}" успешно добавлена на Сегодня!')
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "Неверный формат команды!")


@bot.message_handler(commands=['remove'])
def remove(message):
    try:
        date = message.text.split()[2]
        try:
            if date.lower() != 'сегодня':
                valid_date = time.strptime(date, '%d/%m/%Y')
        except ValueError:
            bot.send_message(message.chat.id, "Неверный формат даты!")
            return
        removed_task = message.text.split()[1].lower()
        if removed_task in tasks[date]:
            tasks[date].remove(removed_task)
            bot.send_message(message.chat.id, f'Задача "{removed_task}" успешно удалена!')
        else:
            bot.send_message(message.chat.id, "Такой задачи не существует!")
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "Неверный формат команды!")


bot.polling(none_stop=True)
