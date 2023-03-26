import telebot
import pandas as pd
from parser import parse_products

bot_token = "5840525763:AAH-vedDcBZwYOURuaTbMEOxHOhENOi5VrY"
bot = telebot.TeleBot(bot_token)

class File:
    name = ''
    def __init__(self):
        name = ''

@bot.message_handler(commands=['start'])
def greetings(message):
    bot.send_message(message.chat.id,text="Привет! Отправьте мне excel таблицу со списком запросов")

@bot.message_handler(content_types=["document"])
def handle_docs(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    src = f"loaded_files/{message.document.file_name}"
    File.name = src
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    msg = bot.send_message(message.chat.id,"Выполняется Парсинг!")
    bot.register_next_step_handler(msg, handle_parsing(message))
def handle_parsing(message):

    df = pd.read_excel(File.name)
    zaprosy = df["name"].tolist()
    for zapros in zaprosy:
        print(zapros)
        parse_products(zapros=zapros, result_filename=f"{zapros}")
        bot.send_document(message.chat.id, open(rf'results/{zapros}.xlsx', 'rb'))

if "__main__" == __name__:
    bot.polling()