from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker


url_object = URL.create(
    "postgresql+psycopg2",
    username="abbossth",
    password="PythonBot2024.",  # plain (unescaped) text
    host="cbusurvey.postgres.database.azure.com",
    database="mbSurveyBotDb",
    port=5432
)


engine = create_engine(url=url_object, echo=True)

# Create a sessionmaker
Session = sessionmaker(bind=engine)
