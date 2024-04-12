from telebot import TeleBot
from utils import generate_option_markup, generate_next_markup
from DAL.Repository.UserRepository import UserRepository
from DAL.Repository.QuestionRepository import QuestionRepository
from DAL.Repository.OptionRepository import OptionRepository
from DAL.Repository.ResponseRepository import ResponseRepository
from Models.main import Question, Option, User
from data.options import jump_options_question4


class QuestionHandler:
    _instance = None

    @staticmethod
    def get_instance():
        if QuestionHandler._instance is None:
            QuestionHandler._instance = QuestionHandler()
        return QuestionHandler._instance

    def send_question4(self, bot: TeleBot, user: User) -> None:
        user_language = user.language
        question_id = QuestionRepository.getByLanguageNumber(user_language, 3).id
        responses = ResponseRepository.get_by_question_and_user_id(user.id, question_id)

        for response in responses:
            option = OptionRepository.getById(response.option_id)
            jump_question_number = jump_options_question4.get(user_language).get(option.option_text)
            jump_question = self._get_question(jump_question_number, user_language)
            options = self._get_options(jump_question.id)
            bot.send_message(
                user.id,
                jump_question.title, 
                reply_markup=generate_option_markup(options, jump_question.number, jump_question.id, jump_question.is_single_option)
            )

    def send_question(self, bot: TeleBot, user_id: int) -> None:
        user = UserRepository.get(user_id)
        question_number = user.current_question_number

        if question_number == 4:
            user_language = user.language
            question_id = QuestionRepository.getByLanguageNumber(user_language, question_number).id
            question3_responses = ResponseRepository.get_by_question_and_user_id(user.id, question_id)
            for response in question3_responses:
                option = OptionRepository.getById(response.option_id)
                jump_question_number = jump_options_question4.get(user_language).get(option.option_text)
                if jump_question_number == 4:
                    jump_question = self._get_question(jump_question_number, user_language)
                    options = self._get_options(jump_question.id)
                    bot.send_message(
                        user.id,
                        jump_question.title, 
                        reply_markup=generate_option_markup(options, jump_question.number, jump_question.id, jump_question.is_single_option)
                    )
                    self.set_user_question_number(user, question_number)
                    return

        question = self._get_question(user.current_question_number, user.language)        
        options = self._get_options(question.id)
        if question.is_single_option:  # multiple
            bot.send_message(
                user_id, 
                question.title,
                reply_markup=generate_option_markup(
                    options, question.number, question.id, question.is_single_option
                )
            )
            self._send_next_question_menu(bot, user_id, question.language, question.number)
        else:
            bot.send_message(
                user_id,
                question.title, 
                reply_markup=generate_option_markup(options, question.number, question.id, question.is_single_option)
            )

        self.set_user_question_number(user, question_number)

    def set_user_question_number(self, user: User, question_number: int) -> None:
        # if question_number == user.current_question_number:
        # question = QuestionRepository.getAll()
        UserRepository.set_question_number(user.id, question_number + 1)
        # QuestionHandler.get_instance().send_question(bot, user.id)

    def _get_question(self, number: int, language: str) -> Question:
        return QuestionRepository.getByLanguageNumber(language, number)
    
    def _get_options(self, question_id: int) -> list[Option]:
        return OptionRepository.getByQuestionId(question_id)

    def _send_next_question_menu(self, bot: TeleBot, user_id: int, lang: str, number: int) -> None:
        description = "Перейти следующего вопроса"
        if lang == "uzlatin":
            description = "Keyingi savolga o'tish"
        elif lang == "uzkiril":
            description = "Кейинги саволга отиш"
        return bot.send_message(user_id, description, reply_markup=generate_next_markup(lang, number))
