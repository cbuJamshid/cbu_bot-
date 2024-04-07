from db_session import Session
from Models.main import Option


class OptionRepository:

    @staticmethod
    def getByQuestionId(question_id: int) -> list:
        try:
            session = Session()
            return session.query(Option).filter(Option.question_id == question_id).all()
        finally:
            # Close the session in finally block to ensure it's always closed
            if session:
                session.close()
