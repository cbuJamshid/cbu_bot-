from db_session import Session
from Models.main import Question


class QuestionRepository:

    @staticmethod
    def getAll(language: str) -> list:
        session = Session()
        return session.query(Question).filter(Question.language == language).order_by(Question.number.asc()).all()


    @staticmethod
    def getQuestionByNumber(number: int) -> Question:
        questions = QuestionRepository.getAll()
        try:
            return questions[number]
        except Exception:
            pass

    @staticmethod
    def getByLanguageNumber(language: str, number: int) -> Question:
        session = Session()
        return session.query(Question).filter(Question.language == language, Question.number == number).first()