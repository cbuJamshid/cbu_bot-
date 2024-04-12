import telebot
from config import BOT_TOKEN
from telebot.types import Message, CallbackQuery
from utils import generate_markup_languages, generate_option_markup, str_to_bool
from DAL.Repository.UserRepository import UserRepository
from DAL.Repository.OptionRepository import OptionRepository
from DAL.Repository.ResponseRepository import ResponseRepository
from DAL.Handlers.question import QuestionHandler
from DAL.Handlers.response import ResponseHandler
from Models.main import *
from datetime import datetime


bot = telebot.TeleBot(BOT_TOKEN)


# Message handlers
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


@bot.message_handler(commands=["users"])
def handle_users_command(message: Message):
    user_id = message.chat.id
    users = UserRepository.get_all()
    for user in users:
        bot.send_message(user_id, f"ID: {user.id}, Language: {user.language}, Question: {user.current_question_number}")


@bot.message_handler(commands=["responses"])
def handle_responses_command(message: Message):
    user_id = message.chat.id
    responses = ResponseRepository.get_all()
    for r in responses:
        bot.send_message(user_id, f"ID: {r.id}, USER_ID: {r.user_id}, QUESTION_ID: {r.question_id}, OPTION_ID: {r.option_id}")



# Callback handlers
@bot.callback_query_handler(func=lambda call: call.data in ["ru", "uzlatin", "uzkiril"])
def handle_language_change_callback(call: CallbackQuery):
    user_id = call.message.chat.id
    UserRepository.set_language(user_id, call.data)
    UserRepository.set_question_number(user_id, 1)
    QuestionHandler.get_instance().send_question(bot, user_id)


@bot.callback_query_handler(func=lambda call: "none" in call.data or "selected" in call.data)
def handle_response_callback(call: CallbackQuery):
    user_id = call.message.chat.id
    user = UserRepository.get(user_id)
    question_id, question_number, option_id, is_single_option, select = call.data.split("_")
    options = OptionRepository.getByQuestionId(question_id)
    question_number = int(question_number)
    question_id = int(question_id)
    is_single_option = str_to_bool(is_single_option)
    selected_symbol = "🔘"
    if is_single_option:
        selected_symbol = "☑️"
        ResponseRepository.delete_or_create(user_id, question_id, option_id)
        responses = ResponseRepository.get_response_by_question_and_user_ids(user_id, question_id)
        selected_options = []
        for r in responses:
            selected_options.append(r.option_id)
        markup = generate_option_markup(options, question_number, question_id, is_single_option)
        for row in markup.keyboard:
            for button in row:
                question_id, question_number, option_id_, is_single_option, select = button.callback_data.split("_")
                if option_id_ in selected_options:
                    option = OptionRepository.get_by_id(option_id_)
                    button.text = f"{selected_symbol} {option.option_text}"
                    button.callback_data = f"{question_id}_{question_number}_{option_id}_selected"
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)
    else:
        ResponseHandler.set_response(user_id, question_id, option_id)
        markup = generate_option_markup(options, question_number, question_id, is_single_option)
        for row in markup.keyboard:
            for button in row:
                if button.callback_data == call.data:
                    option = OptionRepository.get_by_id(option_id)
                    button.text = f"{selected_symbol} {option.option_text}"
                    button.callback_data = f"{question_id}_{question_number}_{option_id}_selected"
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)
        if question_number == user.current_question_number:
            UserRepository.set_question_number(user_id, question_number + 1)
            QuestionHandler.get_instance().send_question(bot, user_id)


@bot.callback_query_handler(func=lambda call: "next" in call.data)
def handle_next_question_callback(call: CallbackQuery):
    user_id = call.message.chat.id
    user = UserRepository.get(user_id)
    _, question_number = call.data.split("_")
    question_number = int(question_number)
    if user.current_question_number == question_number:
        UserRepository.set_question_number(user_id, question_number + 1)
        QuestionHandler.get_instance().send_question(bot, user_id)
    return


bot.infinity_polling()
