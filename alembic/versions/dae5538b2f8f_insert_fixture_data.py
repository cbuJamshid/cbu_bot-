"""insert fixture data

Revision ID: dae5538b2f8f
Revises: 16521b89c1d0
Create Date: 2024-04-07 12:38:03.293361

"""
from typing import Sequence, Union
from data.questions import questions_ru, questions_uz_kiril, questions_uz_latin

from alembic import op
import sqlalchemy as sa
from sqlalchemy import MetaData, Table


# revision identifiers, used by Alembic.
revision: str = 'dae5538b2f8f'
down_revision: Union[str, None] = '16521b89c1d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def bulk_create_ru_questions(questions_table: sa.Table):
    ru_number = 1
    ru_questions_data = []
    for q in questions_ru:
        ru_questions_data.append({
            'number': ru_number,
            'title': q['question'], 
            'is_single_option': q['multiple_option_selection'],
            'language': "ru"
        })
        ru_number += 1
    op.bulk_insert(questions_table, ru_questions_data)


def bulk_create_uzkiril_questions(questions_table: sa.Table):
    uz_kiril_number = 1
    uz_kiril_questions_data = []
    for q in questions_uz_kiril:
        uz_kiril_questions_data.append({
            'number': uz_kiril_number,
            'title': q['question'], 
            'is_single_option': q['multiple_option_selection'],
            'language': "uzkiril"
        })
        uz_kiril_number += 1
    op.bulk_insert(questions_table, uz_kiril_questions_data)


def bulk_create_uzlatin_questions(questions_table: sa.Table):
    uz_latin_number = 1
    uz_latin_questions_data = []
    for q in questions_uz_latin:
        uz_latin_questions_data.append({
            'number': uz_latin_number,
            'title': q['question'], 
            'is_single_option': q['multiple_option_selection'],
            'language': "uzlatin"
        })
        uz_latin_number += 1
    op.bulk_insert(questions_table, uz_latin_questions_data)


def upgrade() -> None:
    meta = MetaData()
    questions_table = Table('questions', meta, autoload_with=op.get_bind())
    #options_table = Table('options', meta, autoload_with=op.get_bind())
    bulk_create_ru_questions(questions_table)
    bulk_create_uzkiril_questions(questions_table)
    bulk_create_uzlatin_questions(questions_table)



def downgrade() -> None:
    op.execute("TRUNCATE TABLE questions CASCADE")
