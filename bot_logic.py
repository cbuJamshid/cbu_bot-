import telebot
from telebot.types import Message
from config import BOT_TOKEN
from utils import generate_markup_languages, generate_markup
from DAL.Repository.UserRepository import UserRepository
from Models.main import *


def bot_logic():
    # setup
    bot = telebot.TeleBot(BOT_TOKEN)

    # finish
    def send_survey_finish_message(chat_id, lang):
        if lang == "uz_kiril":
            return bot.send_message(chat_id, f"<b>Сўровномамизда иштирок этганингиз учун ташаккур! Сизнинг фикрингиз биз учун қадрлидир.</b>", parse_mode='HTML')
        elif lang == "uz_latin":
            return bot.send_message(chat_id, f"<b>So'rovnomada ishtiroq etganingiz uchun tashakkur! Sizning fikringiz biz uchun qadrlidir</b>", parse_mode='HTML')
        else:
            return bot.send_message(chat_id, f"<b>Благодарим вас за участие в нашем опросе! Ваше мнение для нас ценно. </b>", parse_mode='HTML')

    @bot.message_handler(commands=["start"])
    def handle_start_command(message: Message):
        user = User(
            user_id=message.from_user.id, 
            language=message.from_user.language_code, 
            join_date=message.date,
            current_question_number=1,
            is_survey_finished=False
        )
        UserRepository.create(user)
        bot.send_message(
            message.chat.id, 
            f"<b>{message.from_user.first_name},</b> Аҳоли қарз юкини аниқлаш бўйича сўровномага хуш келибсиз!\nИлтимос, тилни танланг<b>\n\n{message.from_user.first_name},</b> Добро пожаловать в опросник по определению долговой нагрузки населения!\nПожалуйста, выберите язык", 
            parse_mode='HTML',  
            reply_markup=generate_markup_languages()
        )

    # bot polling
    bot.polling(non_stop=True, interval=0)
