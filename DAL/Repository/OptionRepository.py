from db_session import Session
from Models.main import Option


class OptionRepository:
    _option_cache = {}

    @staticmethod
    def getByQuestionId(question_id: int) -> list[Option]:
        options: list[Option] = OptionRepository._option_cache.get(question_id)
        if options: 
            print("OPTION: CACHE HIT ->>>>>>>>")
            return options
        with Session() as session:
            options = session.query(Option).filter(Option.question_id == question_id).all()
            OptionRepository._option_cache[question_id] = options
            return options

    @staticmethod
    def getById(id: int) -> Option:
        with Session() as session:
            return session.query(Option).get({"id": id})
