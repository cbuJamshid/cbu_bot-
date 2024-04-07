from db_session import Session
from Models.main import Question


class QuestionRepository:

    @staticmethod
    def getAll(language: str) -> list:
        try:
            session = Session()
            return session.query(Question).filter(Question.language == language).order_by(Question.number.asc()).all()
        finally:
            # Close the session in finally block to ensure it's always closed
            if session:
                session.close()

    @staticmethod
    def getQuestionByNumber(number: int) -> Question:
        questions = QuestionRepository.getAll()
        try:
            return questions[number]
        except Exception:
            pass

    @staticmethod
    def getByLanguageNumber(language: str, number: int) -> Question:
        try:
            session = Session()
            return session.query(Question).filter(Question.language == language, Question.number == number).first()
        finally:
            # Close the session in finally block to ensure it's always closed
            if session:
                session.close()
