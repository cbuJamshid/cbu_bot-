from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, BigInteger, Integer, String, Boolean, DateTime, ForeignKey

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    language = Column(String(16))
    current_question_number = Column(Integer)
    is_survey_finished = Column(Boolean)
    join_date = Column(DateTime)

    # back ForeignKey
    responses = relationship("Response", backref="user")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(256))
    is_single_option = Column(Boolean)
    number = Column(Integer)
    language = Column(String(16))

    responses = relationship("Response", backref="question")
    options = relationship("Option", backref="question")


class Option(Base):
    __tablename__ = "options"

    id = Column(Integer, primary_key=True, autoincrement=True)
    option_text = Column(String(256))
    question_id = Column(Integer, ForeignKey('questions.id'))

    responses = relationship("Response", backref="option")


class Response(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id'))
    question_id = Column(Integer, ForeignKey('questions.id'))
    option_id = Column(Integer, ForeignKey('options.id'))

    def __repr__(self):
        return f"User: {self.user_id} Question: {self.question_id} Option: {self.option_id}"

    def __str__(self):
        return f"User: {self.user_id} Question: {self.question_id} Option: {self.option_id}"
