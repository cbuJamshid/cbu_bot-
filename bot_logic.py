import telebot
from telebot import types
from config import BOT_TOKEN
from db import select_users, new_user, select_user, set_language, select_question, select_options, increment_order_num
from utils import generate_markup_languages, generate_markup


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

    # send question
    def send_question(user_id):
        user = select_user(user_id)
        print(user)
        current_question_order = user[0][3]
        chosen_language = user[0][2]
        question = select_question(current_question_order, chosen_language)
        options = select_options(current_question_order, chosen_language)
        question_text = question[0][1]
        print(question)
        bot.send_message(user_id, f"{question_text}", reply_markup=generate_markup(options, question[0][3]))

    # start command
    @bot.message_handler(commands=['start', 'survey'])
    def start(message):
        # sending welcome message
        bot.send_message(message.chat.id, f"<b>{message.from_user.first_name},</b> Аҳоли қарз юкини аниқлаш бўйича сўровномага хуш келибсиз!\nИлтимос, тилни танланг<b>\n\n{message.from_user.first_name},</b> Добро пожаловать в опросник по определению долговой нагрузки населения!\nПожалуйста, выберите язык", parse_mode='HTML',  reply_markup=generate_markup_languages())

    # Handler for inline keyboard button clicks
    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback_query(call):
        chat_id = call.message.chat.id
        user = select_user(chat_id)
        current_question_order = user[0][3]
        lang = user[0][2]
        # is_survey_finished = user[0][3]
        try:    
            if call.data in ["ru", "uz_latin", "uz_kiril"]:
                user = select_user(chat_id)
                if user:
                    increment_order_num(chat_id, 0)
                else:
                    new_user(chat_id)
                set_language(chat_id, call.data)
                send_question(chat_id)

            if "_" in call.data:
                question_idx, answer, select = call.data.split('_')
                question_id = int(question_idx)
                print(question_id, "-", current_question_order)

                # Here we will write code when survey end is done
                if question_id > 51:
                    print("Yes")
                    return send_survey_finish_message(chat_id, lang)

                # if current question is pressed, send next question
                if current_question_order == question_id:
                    increment_order_num(chat_id, current_question_order + 1)
                    return send_question(chat_id)
                # else, edit question response
                else:
                    bot.send_message(chat_id, "Editing question response..")

            print(f"{call.data} is not recognized")
            # bot.send_message(chat_id, call.data)
        except Exception as ex:
            print(f"Error in callback data handling. {ex}")

    # data command
    @bot.message_handler(commands=['data'])
    def send_data(message):
        users = select_users()
        bot.send_message(message.chat.id, f"Users: {users}")

    # bot polling
    bot.polling(non_stop=True, interval=0)
