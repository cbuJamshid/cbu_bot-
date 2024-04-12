from DAL.Repository.ResponseRepository import ResponseRepository


class ResponseHandler:

    @staticmethod
    def set_response(user_id, question_id, option_id) -> None:
        ResponseRepository.update_or_create(user_id, question_id, option_id)
