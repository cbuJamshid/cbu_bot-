import telebot
from config import BOT_TOKEN
from telebot.types import Message, CallbackQuery
from utils import generate_markup_languages, extract_values_from_callback_data, generate_option_markup
from DAL.Repository.UserRepository import UserRepository
from DAL.Repository.OptionRepository import OptionRepository
from DAL.Repository.ResponseRepository import ResponseRepository
from DAL.Repository.QuestionRepository import QuestionRepository
from DAL.Handlers.question import QuestionHandler
from Models.main import *
from datetime import datetime
from constants import (
    SINGLE_OPTION_SELECTED_SYMBOL,
    MULTIPLE_OPTION_SELECTED_SYMBOL,
)


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




@bot.message_handler(commands=["questions"])
def handle_responses_command(message: Message):
    user_id = message.chat.id
    qs = QuestionRepository.getAll()
    for q in qs:
        bot.send_message(user_id, f"ID: {q.id} NUM: {q.number} QUESTION: {q.title}")


@bot.message_handler(commands=["options"])
def handle_responses_command(message: Message):
    user_id = message.chat.id
    user = UserRepository.get(user_id)
    question = QuestionRepository.getByLanguageNumber("uzlatin", user.current_question_number)
    options = OptionRepository.getByQuestionId(3)
    # for q in qs:
    #     bot.send_message(user_id, f"ID: {q.number}, QUESTION: {q.title}")
    for option in options:
        bot.send_message(user_id, f"ID: {option.option_text}")


# Callback handlers
@bot.callback_query_handler(func=lambda call: call.data in ["ru", "uzlatin", "uzkiril"])
def handle_language_change_callback(call: CallbackQuery):
    user_id = call.message.chat.id
    UserRepository.set_language(user_id, call.data)
    UserRepository.set_question_number(user_id, 1)
    QuestionHandler.get_instance().send_question(bot, user_id)


@bot.callback_query_handler(func=lambda call: "questions" in call.data)
def handle_response_callback(call: CallbackQuery):
    user_id = call.message.chat.id
    user = UserRepository.get(user_id)
    question_id, question_number, option_id, is_multiple_option = extract_values_from_callback_data(
        call.data
    )
    options = OptionRepository.getByQuestionId(question_id)
    markup = generate_option_markup(options, question_number, question_id, is_multiple_option)

    if is_multiple_option:
        ResponseRepository.delete_or_create(user_id, question_id, option_id)
        users_responses = ResponseRepository.get_by_question_and_user_id(user_id, question_id)
        selected_option_ids = [response.option_id for response in users_responses]
        # Showing selected options with 'selected_symbol'
        for row in markup.keyboard:
            for button in row:
                _, _, response_option_id, _, _ = button.callback_data.split("_")
                if int(response_option_id) in selected_option_ids:
                    button.text = MULTIPLE_OPTION_SELECTED_SYMBOL + button.text[1:]
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)
    else:
        ResponseRepository.update_or_create(user_id, question_id, option_id)
        # Showing selected options with 'selected_symbol'
        for row in markup.keyboard:
            for button in row:
                _, _, response_option_id, _, _ = button.callback_data.split("_")
                if int(response_option_id) == option_id:
                    button.text = SINGLE_OPTION_SELECTED_SYMBOL + button.text[1:]
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)
        if user.current_question_number - 1 == question_number:
            QuestionHandler.get_instance().send_question(bot, user.id)


@bot.callback_query_handler(func=lambda call: "next" in call.data)
def handle_next_question_callback(call: CallbackQuery):
    user_id = call.message.chat.id
    user = UserRepository.get(user_id)
    _, question_number = call.data.split("_")
    question_number = int(question_number)
    if user.current_question_number - 1 == question_number:
        QuestionHandler.get_instance().send_question(bot, user.id)
    return


bot.infinity_polling()
