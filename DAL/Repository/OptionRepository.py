from db_session import Session
from Models.main import Option
from functools import cached_property


class OptionRepository:
    _option_cache = {}

    @staticmethod
    @cached_property
    def getByQuestionId(question_id: int) -> list[Option]:
        options: list[Option] = OptionRepository._option_cache.get(question_id)
        if options: 
            print("OPTION: CACHE HIT ->>>>>>>>")
            return options
        with Session() as session:
            options = session.query(Option).filter(Option.question_id == question_id).all()
            OptionRepository._option_cache[question_id] = options
            return options
