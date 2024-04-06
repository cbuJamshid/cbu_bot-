from db_session import Session
from Models.main import User


class UserRepository:

    @staticmethod
    def set_question_number(user_id: int, question_number: int) -> None:
        with Session() as session:
            session.query(User).filter_by(id = user_id).update({"current_question_number": question_number})
            session.commit()

    @staticmethod
    def set_language(user_id: int, language: str) -> None:
        with Session() as session:
            session.query(User).filter_by(id = user_id).update({"language": language})
            session.commit()

    @staticmethod
    def get(user_id: int) -> User:
        with Session() as session:
            return session.query(User).get({"id": user_id})

    @staticmethod
    def create(user: User) -> None:
        with Session() as session:
            session.add(user)
            session.commit()
