from telebot import TeleBot
from utils import generate_option_markup, generate_next_markup
from DAL.Repository.UserRepository import UserRepository
from DAL.Repository.QuestionRepository import QuestionRepository
from DAL.Repository.OptionRepository import OptionRepository
from Models.main import Question, Option


class QuestionHandler:
    _instance = None

    @staticmethod
    def get_instance():
        if QuestionHandler._instance is None:
            QuestionHandler._instance = QuestionHandler()
        return QuestionHandler._instance

    def send_question(self, bot: TeleBot, user_id: int) -> None:
        user = UserRepository.get(user_id) 
        question, options = self._get_question(user.current_question_number, user.language)
        if question.is_single_option:
            bot.send_message(
                user_id, 
                question.title,
                reply_markup=generate_option_markup(
                    options, question.number, question.id, question.is_single_option
                )
            )
            self._send_next_question_menu(user_id, question.language, question.number)
        else:
            bot.send_message(
                user_id, 
                question.title, 
                reply_markup=generate_option_markup(options, question.number, question.id, question.is_single_option)
            )

    def _get_question(self, number: int, language: str) -> tuple[Question, list[Option]]:
        question = QuestionRepository.getByLanguageNumber(language, number)
        options = OptionRepository.getByQuestionId(question.id)
        return question, options

    def _send_next_question_menu(self, bot: TeleBot, user_id: int, lang: str, number: int) -> None:
        description = "Перейти следующего вопроса"
        if lang == "uzlatin":
            description = "Keyingi savolga o'tish"
        elif lang == "uzkiril":
            description = "Кейинги саволга отиш"
        return bot.send_message(user_id, description, reply_markup=generate_next_markup(lang, number))
