from db_session import Session
from Models.main import Response


class ResponseRepository:

    @staticmethod
    def update_or_create(user_id: int, question_id: int, option_id: int) -> None:
        """
        For questions with one response. If user has response to question_id. 
        Instead of creating new reponse it updates the existing with new option_id
        """
        session = Session()
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
        For questions with one response. If user has response to question_id.
        Instead of creating new reponse it updates the existing with new option_id
        """
        session = Session()
        response = session.query(Response).filter(
            Response.user_id == user_id,
            Response.question_id == question_id,
            Response.option_id == option_id
        ).first()
        if response:
            response = session.query(Response).filter(
                Response.user_id == user_id,
                Response.question_id == question_id
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
    def delete_all(user_id: int, question_id: int) -> None:
        """
        For questions with multiple responses. Deletes all responses of user for question_id
        """
        session = Session()
        session.query(Response).filter(
            Response.user_id == user_id,
            Response.question_id == question_id
        ).delete()
        session.commit()

    @staticmethod
    def create_multiple(user_id: int, question_id: int, option_ids: list[int]) -> None:
        """
        Creates multiple responses for a question using options_ids which is a list of ids
        """
        responses = [
            Response(user_id=user_id, question_id=question_id, option_id=option_id)
            for option_id in option_ids
        ]
        session = Session()
        session.add_all(responses)
        session.commit()

    @staticmethod
    def get_all() -> []:
        with Session() as session:
            return session.query(Response).all()

    @staticmethod
    def get_response_by_question_and_user_ids(user_id: int, question_id: int) -> list:
        session = Session()
        return session.query(Response).filter(Response.user_id == user_id, Response.question_id == question_id).all()
