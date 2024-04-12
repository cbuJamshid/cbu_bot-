from db_session import Session
from Models.main import Question
from constants import RU, UZLATIN, UZKIRIL

class QuestionRepository:
    _question_cache = {"ru": {}, "uzlatin": {}, "uzkiril": {}}

    @staticmethod
    def getByLanguageNumber(language: str, number: int) -> Question:
        question = QuestionRepository._question_cache.get(language).get(number)
        if question: 
            print("QUESTION: CACHE HIT ->>>>>>>>")
            return question
        with Session() as session:
            db_question = session.query(Question).filter(
                Question.language == language, 
                Question.number == number
            ).first()
            QuestionRepository._question_cache[language][number] = db_question
            return db_question

    @staticmethod
    def getAll():
        with Session() as session:
            return session.query(Question).filter(Question.language == UZLATIN).all()
