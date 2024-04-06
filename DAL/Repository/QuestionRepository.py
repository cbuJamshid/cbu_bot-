from db_session import Session
from Models.main import Question


class QuestionRepository:

    def getAll(language: str):
        try:
            session = Session()
            return session.query(Question).filter_by(language == language)
        finally:
            # Close the session in finally block to ensure it's always closed
            if session:
                session.close()
