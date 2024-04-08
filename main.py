import telebot
from config import BOT_TOKEN
from telebot.types import Message, CallbackQuery
from utils import generate_markup_languages, generate_option_markup
from DAL.Repository.UserRepository import UserRepository
from DAL.Repository.QuestionRepository import QuestionRepository
from DAL.Repository.OptionRepository import OptionRepository
from Models.main import *
from datetime import datetime


bot = telebot.TeleBot(BOT_TOKEN)
    
@bot.message_handler(commands=["start"])
def handle_start_command(message: Message):
    user_id = message.chat.id
    user = UserRepository.get(user_id)
    if not user:        
        user_data = User(
            id=user_id, 
            language="ru", 
            join_date=datetime.fromtimestamp(message.date),
            current_question_number=1,
            is_survey_finished=False
        )
        UserRepository.create(user_data)
    bot.send_message(
        message.chat.id, 
        f"<b>{message.from_user.first_name},</b> Аҳоли қарз юкини аниқлаш бўйича сўровномага хуш келибсиз!\nИлтимос, тилни танланг<b>\n\n{message.from_user.first_name},</b> Добро пожаловать в опросник по определению долговой нагрузки населения!\nПожалуйста, выберите язык", 
        parse_mode='HTML',  
        reply_markup=generate_markup_languages()
    )

@bot.callback_query_handler(func=lambda call: call.data in ["ru", "uzlatin", "uzkiril"])
def handle_language_change_callback(call: CallbackQuery):
    user_id = call.message.chat.id
    UserRepository.set_language(user_id, call.data)
    user = UserRepository.get(user_id)    
    send_question(user_id)
    

def get_question(number: int, language: str):
    question = QuestionRepository.getByLanguageNumber(language, number)
    options = OptionRepository.getByQuestionId(question.id)
    return (question, options)

def send_question(user_id):
    user = UserRepository.get(user_id) 
    question, options = get_question(user.current_question_number, user.language)
    bot.send_message(user_id, question.title, reply_markup=generate_option_markup(options, question.number))

@bot.callback_query_handler(func=lambda call: "_" in call.data)
def handle_response_callback(call: CallbackQuery):
    user_id = call.message.chat.id
    user = UserRepository.get(user_id)    
    question_number, option_id, select = call.data.split("_")
    question_number_int = int(question_number)
    bot.send_message(user_id, f"q: {question_number_int} - c: {user.current_question_number}")
    if question_number_int == user.current_question_number:
        UserRepository.set_question_number(user_id, question_number_int + 1)
        send_question(user_id)
    else:    
        return bot.send_message(call.message.chat.id, f"Editing: {call.data}")


bot.infinity_polling()
