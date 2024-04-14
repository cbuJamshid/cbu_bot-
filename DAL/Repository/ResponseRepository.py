from db_session import Session
from Models.main import Response


class ResponseRepository:

    @staticmethod
    def update_or_create(user_id: int, question_id: int, option_id: int) -> None:
        """
        For questions with one response. If user has response to question_id. 
        Instead of creating new reponse it updates the existing with new option_id
        """
        with Session() as session:
            response = session.query(Response).filter(
                Response.user_id == user_id,
                Response.question_id == question_id
            ).first()
            if response:
                response = session.query(Response).filter(
                    Response.user_id == user_id,
                    Response.question_id == question_id
                ).update({"option_id": option_id})
            else:
                new_response = Response(
                    user_id=user_id,
                    question_id=question_id,
                    option_id=option_id
                )
                session.add(new_response)
            session.commit()

    @staticmethod
    def delete_or_create(user_id: int, question_id: int, option_id: int) -> None:
        """
        For questions with multiple responses. If option is in response, it gets removed.
        Else new response gets created.
        """
        with Session() as session:
            response = session.query(Response).filter(
                Response.user_id == user_id,
                Response.question_id == question_id,
                Response.option_id == option_id
            ).first()
            if response:
                response = session.query(Response).filter(
                    Response.user_id == user_id,
                    Response.question_id == question_id,
                    Response.option_id == option_id
                ).delete()
            else:
                new_response = Response(
                    user_id=user_id,
                    question_id=question_id,
                    option_id=option_id
                )
                session.add(new_response)
            session.commit()

    @staticmethod
    def get_all() -> list[Response]:
        with Session() as session:
            return session.query(Response).all()

    @staticmethod
    def get_by_question_and_user_id(user_id: int, question_id: int) -> list[Response]:
        with Session() as session:
            return session.query(Response).filter(Response.user_id == user_id, Response.question_id == question_id).order_by(Response.option_id.asc()).all()

    @staticmethod
    def get_single_by_question_user_id(user_id: int, question_id: int) -> Response:
        with Session() as session:
            return session.query(Response).filter(Response.user_id == user_id, Response.question_id == question_id).first()
