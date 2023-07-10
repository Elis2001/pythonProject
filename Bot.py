import telebot
import tempfile
from Config import TOKEN

bot = telebot.TeleBot(TOKEN)

# Создаем временную папку
temp_dir = tempfile.TemporaryDirectory()


@bot.message_handler(content_types=['text', 'photo', 'audio', 'sticker'])
def message_handler(message):
    if message.text:  # Если сообщение является текстом
        bot.send_message(message.chat.id, message.text)  # Отправляем обратно то же самое сообщение

    if message.photo:  # Если сообщение содержит фотографию
        photo = message.photo[-1]  # Берем последнюю доступную фотографию
        file_id = photo.file_id

        # Получение объекта файла
        file_info = bot.get_file(file_id)
        file_path = file_info.file_path

        # Скачивание файла на сервер
        downloaded_file = bot.download_file(file_path)

        # Создаем уникальное имя файла
        file_name = f'{file_id}.jpg'
        file_path = f'{temp_dir.name}/{file_name}'

        # Сохраняем файл во временной папке
        with open(file_path, 'wb') as file:
            file.write(downloaded_file)

        # Отправляем изображение обратно
        with open(file_path, 'rb') as file:
            bot.send_photo(message.chat.id, file)

    elif message.content_type == 'sticker':  # Если сообщение содержит стикер
        bot.send_sticker(message.chat.id, message.sticker.file_id)  # Отправляем стикер обратно

    elif message.content_type == 'audio':  # Если сообщение содержит аудиофайл
        bot.send_audio(message.chat.id, message.audio.file_id)  # Отправляем аудиофайл обратно

    # Удаляем файл после использования
    temp_dir.cleanup()


if __name__ == '__main__':
    bot.polling(True)
