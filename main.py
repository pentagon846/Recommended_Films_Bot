import os

from bs4 import BeautifulSoup
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from dotenv import load_dotenv

load_dotenv()
def get_recommended_movies():
    url = 'https://rezka-ua.tv/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    }
    try:
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            print(f"Error: {res.status_code}")
            exit(1)
    except:
        print("Error: Unable to establish connection to the website, \n please try again")
        exit(1)

    soup = BeautifulSoup(res.text, 'html.parser')

    recommended_movies = []

    for movie in soup.find_all('div', class_='b-content__inline_item'):
        title = movie.find('div', class_='b-content__inline_item-link').get_text(strip=True)
        recommended_movies.append(title)
        if len(recommended_movies) >= 10:
            break

    # print("Рекомендовані фільми за поточний день:")
    # for movie in recommended_movies:
    #     print(movie)
    return recommended_movies


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Привіт! Використовуйте команду /movies для отримання рекомендованих фільмів за поточний день.')


def movies(update: Update, context: CallbackContext):
    movies = get_recommended_movies()
    if movies:
        response = 'Рекомендовані фільми за день: \n' + "\n".join(movies)
    else:
        response = 'Не вдалося знайти рекомендований фільм.'
    update.message.reply_text(response)


def main():
    TOKEN = os.getenv('TOKEN')

    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Реєструємо обробники команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("movies", movies))

    # Запускаємо бота
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
