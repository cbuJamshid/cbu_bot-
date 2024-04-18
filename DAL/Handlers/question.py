from telebot import TeleBot
from utils import generate_option_markup, generate_next_markup, send_survey_finish_message
from DAL.Repository.UserRepository import UserRepository
from DAL.Repository.QuestionRepository import QuestionRepository
from DAL.Repository.OptionRepository import OptionRepository
from DAL.Repository.ResponseRepository import ResponseRepository
from Models.main import Question, Option, User
from data.options import jump_options_question4, jump_options_no, jump_options_question9


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

        # if user answered all questions, it ends survey
        if user.current_question_number > 53:
            UserRepository.set_is_survey_finished(user_id)
            return send_survey_finish_message(user_id, user.language, bot)

        if user.current_question_number == 4:
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
            self.set_user_question_number(user, 16)
            return

        # question 4 with index of 18
        q10_index = 23
        if user.current_question_number == q10_index + 1:
            question_id = QuestionRepository.getByLanguageNumber(user.language, q10_index).id
            question_responses = ResponseRepository.get_by_question_and_user_id(user.id, question_id)
            for r in question_responses:
                option = OptionRepository.getById(r.option_id)
                if option.option_text in jump_options_no.get(user.language):
                    self.skip_next_question(user, 25)  # increments
                    # bot.send_message(user_id, f"23 -> incremented to 25")
                    user.current_question_number = 25

        if user.current_question_number == 25:
            user_language = user.language
            question_id = QuestionRepository.getByLanguageNumber(user_language, 22).id
            responses = ResponseRepository.get_by_question_and_user_id(user.id, question_id)
            for response in responses:
                option = OptionRepository.getById(response.option_id)
                jump_question_number = jump_options_question9.get(user_language).get(option.option_text)
                next_jump_question_number = jump_question_number + 1
                jump_question = self._get_question(jump_question_number, user_language)
                next_jump_question = self._get_question(next_jump_question_number, user_language)
                options = self._get_options(jump_question.id)
                next_options = self._get_options(next_jump_question.id)
                bot.send_message(
                    user.id,
                    jump_question.title,
                    reply_markup=generate_option_markup(options, jump_question.number, jump_question.id, jump_question.is_single_option)
                )
                bot.send_message(
                    user.id,
                    next_jump_question.title,
                    reply_markup=generate_option_markup(next_options, next_jump_question.number, next_jump_question.id, next_jump_question.is_single_option)
                )
            self.set_user_question_number(user, 34)
            return


        # question 4 with index of 18
        q4_index = 18
        if user.current_question_number == q4_index + 1:
            question_id = QuestionRepository.getByLanguageNumber(user.language, q4_index).id
            question_responses = ResponseRepository.get_by_question_and_user_id(user.id, question_id)
            for r in question_responses:
                option = OptionRepository.getById(r.option_id)
                if option.option_text in jump_options_no.get(user.language):
                    self.skip_next_question(user, question_number) # increments
        
        # question 7 with index of 21
        q7_index = 21
        if user.current_question_number == q7_index + 1:
            question_id = QuestionRepository.getByLanguageNumber(user.language, q7_index).id
            question_responses = ResponseRepository.get_by_question_and_user_id(user.id, question_id)
            for r in question_responses:
                option = OptionRepository.getById(r.option_id)
                if option.option_text in jump_options_no.get(user.language):
                    self.skip_next_question(user, 34) # increments till 34
        
        # question 9 with index of 23
        q9_index = 23
        if user.current_question_number == q9_index + 1:
            question_id = QuestionRepository.getByLanguageNumber(user.language, q9_index).id
            question_responses = ResponseRepository.get_by_question_and_user_id(user.id, question_id)
            for r in question_responses:
                option = OptionRepository.getById(r.option_id)
                if option.option_text in jump_options_no.get(user.language):
                    self.skip_next_question(user, question_number) # increments
        
        # question 21 with index of 35
        q21_index = 35
        if user.current_question_number == q21_index + 1:
            question_id = QuestionRepository.getByLanguageNumber(user.language, q21_index).id
            question_responses = ResponseRepository.get_by_question_and_user_id(user.id, question_id)
            for r in question_responses:
                option = OptionRepository.getById(r.option_id)
                if option.option_text in jump_options_no.get(user.language):
                    self.skip_next_question(user, 40) # increments
        
        # question 23 with index of 37
        q23_index = 37
        if user.current_question_number == q23_index + 1:
            question_id = QuestionRepository.getByLanguageNumber(user.language, q23_index).id
            question_responses = ResponseRepository.get_by_question_and_user_id(user.id, question_id)
            for r in question_responses:
                option = OptionRepository.getById(r.option_id)
                if option.option_text in jump_options_no.get(user.language):
                    self.skip_next_question(user, user.current_question_number) # increments
        
        # question 27 with index of 41
        q27_index = 41
        if user.current_question_number == q27_index + 1:
            question_id = QuestionRepository.getByLanguageNumber(user.language, q27_index).id
            question_responses = ResponseRepository.get_by_question_and_user_id(user.id, question_id)
            for r in question_responses:
                option = OptionRepository.getById(r.option_id)
                if option.option_text in jump_options_no.get(user.language):
                    self.skip_next_question(user, 44) # increments
        
        # question 31 with index of 45
        q31_index = 45
        if user.current_question_number == q31_index + 1:
            question_id = QuestionRepository.getByLanguageNumber(user.language, q31_index).id
            question_responses = ResponseRepository.get_by_question_and_user_id(user.id, question_id)
            for r in question_responses:
                option = OptionRepository.getById(r.option_id)
                if option.option_text in jump_options_no.get(user.language):
                    self.skip_next_question(user, 47) # increments
        
        # question 33 with index of 47
        q33_index = 47
        if user.current_question_number == q33_index + 1:
            question_id = QuestionRepository.getByLanguageNumber(user.language, q33_index).id
            question_responses = ResponseRepository.get_by_question_and_user_id(user.id, question_id)
            for r in question_responses:
                option = OptionRepository.getById(r.option_id)
                if option.option_text in jump_options_no.get(user.language):
                    self.skip_next_question(user, user.current_question_number) # increments
        
        # question 35 with index of 49
        q35_index = 49
        if user.current_question_number == q35_index + 1:
            question_id = QuestionRepository.getByLanguageNumber(user.language, q35_index).id
            question_responses = ResponseRepository.get_by_question_and_user_id(user.id, question_id)
            for r in question_responses:
                option = OptionRepository.getById(r.option_id)
                if option.option_text in jump_options_no.get(user.language):
                    self.skip_next_question(user, user.current_question_number) # increments
        
        # question 38 with index of 52
        q38_index = 52
        if user.current_question_number == q38_index + 1:
            question_id = QuestionRepository.getByLanguageNumber(user.language, q38_index).id
            question_responses = ResponseRepository.get_by_question_and_user_id(user.id, question_id)
            for r in question_responses:
                option = OptionRepository.getById(r.option_id)
                if option.option_text in jump_options_no.get(user.language):
                    self.skip_next_question(user, user.current_question_number) # increments
                    UserRepository.set_is_survey_finished(user_id)
                    return send_survey_finish_message(user_id, user.language, bot)


        user = UserRepository.get(user_id)
        question_number = user.current_question_number
        question = self._get_question(question_number, user.language)        
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
        UserRepository.set_question_number(user.id, question_number + 1)
    
    def skip_next_question(self, user: User, question_number: int) -> None:
        UserRepository.set_question_number(user.id, question_number + 1)

    def _get_question(self, number: int, language: str) -> Question:
        return QuestionRepository.getByLanguageNumber(language, number)
    
    def _get_options(self, question_id: int) -> list[Option]:
        return OptionRepository.getByQuestionId(question_id)

    def _send_next_question_menu(self, bot: TeleBot, user_id: int, lang: str, number: int) -> None:
        description = "Перейти к следующему вопросу"
        if lang == "uzlatin":
            description = "Keyingi savolga o'tish"
        elif lang == "uzkiril":
            description = "Кейинги саволга ўтиш"
        return bot.send_message(user_id, description, reply_markup=generate_next_markup(lang, number))