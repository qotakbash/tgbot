import telebot
import requests

from github import Github



TELEGRAM_TOKEN = "5855937352:AAGTXLlIwIf373SkOqE1s3Qjc8VIK5_60CY"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def load_last_update(message):

    # Извлекаем имя пользователя и название репозитория
    # из текстового запроса, который мы отправили боту в чате.
    _, user_name, repo_name = message.text.split()

    # Создаем объект для взаимодействия с гитхабом.
    g = Github()

    # Загружаем пользователя по его имени.
    try:
        user = g.get_user(user_name)
    except Exception as e:
        return None


    # Ищем репозиторий по его названию.
    target_repo = None
    for repo in user.get_repos():
        if repo.name == repo_name:
            target_repo = repo
            break

    # Если мы не нашли репозиторий с таким именем.
    if target_repo is None:
        return None

    date = target_repo.updated_at

    return date.year, date.month, date.day


# Ожидаем получить на вход команду в следующем формате:
# check <имя пользователя> <имя репозитория>
def check_request(message):
    request = message.text.split()
    if len(request) == 3 and request[0] == 'check':
        return True
    return False

@bot.message_handler(func=check_request)
def check_repo_update(message):

    # Получение данных с сервера
    updated_date = load_last_update(message)

    if updated_date is None:
        response = "User or repo not found!"
    else:
        response = "Last updated: %s : %s : %s" % updated_date

    bot.send_message(message.chat.id, response)


# Ожидаем получить на вход команду в следующем формате:
# show <имя пользователя>
def check_show_request(message):
    request = message.text.split()
    if len(request) == 2 and request[0] == 'show':
        return True
    return False

@bot.message_handler(func=check_show_request)
def show_repos(message):
    _, user_name = message.text.split()

    # Создаем объект для взаимодействия с гитхабом.
    g = Github()

    # Загружаем пользователя по его имени.
    try:
        user = g.get_user(user_name)
    except Exception as e:
        return "No such user!"

    repos_list = [repo.name for repo in user.get_repos()]

    # Ищем репозиторий по его названию.
    bot.send_message(message.chat.id, "\n".join(repos_list))


bot.polling()