from db_session import Session
from Models.main import Option


class OptionRepository:
    @staticmethod
    def getByQuestionId(question_id: int) -> list[Option]:
        session = Session()
        return session.query(Option).filter(Option.question_id == question_id).all()

    @staticmethod
    def get_by_id(id: int) -> Option:
        with Session() as session:
            return session.query(Option).get({"id": id})
