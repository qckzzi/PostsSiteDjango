from django.core.management.base import BaseCommand
from django.conf import settings
from telebot import TeleBot
from ...models import *


bot = TeleBot(settings.TOKEN, threaded=False)


def send_message(post_slug):
    post = Women.objects.get(slug=post_slug)
    profiles = Profile.objects.all()
    title = post.title
    content = post.content
    category = str(post.cat).lower()
    for profile in profiles:
        bot.send_photo(chat_id=profile.external_id, photo=Women.objects.get(slug=post_slug).photo,
                       caption=f"Имя {category} - {title}\n{content}")


class Command(BaseCommand):
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **kwargs):

        @bot.message_handler(commands=['start', 'help'])
        def start(message):
            if message.chat.type == 'private':
                if Profile.objects.filter(external_id=message.from_user.id).exists():
                    bot.reply_to(message, "Вы уже подписаны на рассылку! Хорошего дня! :з")
                else:
                    Profile.objects.create(external_id=message.from_user.id,
                                           username=message.from_user.username,
                                           name=message.from_user.first_name)
                    bot.reply_to(message, f"{message.from_user.first_name},"
                                          f" спасибо за подписку на рассылку! Хорошего дня! :з")
                    bot.send_message(chat_id=settings.ADMIN_ID,
                                     text=f"Новый подписчик! (username: {message.from_user.username})")

        bot.delete_webhook(drop_pending_updates=True)
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        bot.infinity_polling()
