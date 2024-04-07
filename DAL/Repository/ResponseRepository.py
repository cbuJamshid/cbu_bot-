from db_session import Session
from Models.main import Response


class ResponseRepository:

    @staticmethod
    def create(user_id: int, question_id: int, option_id: int) -> list:
        try:
            session = Session()
            response = Response(
                user_id=user_id,
                question_id=question_id,
                option_id=option_id
            )
            session.add(response)
            session.commit()
        finally:
            # Close the session in finally block to ensure it's always closed
            if session:
                session.close()
