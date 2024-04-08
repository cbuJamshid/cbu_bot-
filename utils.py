from telebot import types
from Models.main import Option


# Helper function to generate inline keyboard markup
def generate_markup_languages():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(f"O'zbek Tili", callback_data=f"uzlatin")
    btn2 = types.InlineKeyboardButton(f"Ўзбек тили", callback_data=f"uzkiril")
    btn3 = types.InlineKeyboardButton(f"Русский язык", callback_data=f"ru")
    markup.add(btn1, btn2, btn3)
    return markup


# Helper function to generate inline keyboard markup
def generate_option_markup(options: list[Option], question_number: int, question_id: int, is_single_option: bool) -> types.InlineKeyboardMarkup:
    select_symbol = "⚪️"
    if is_single_option:
        select_symbol = "◻️"

    markup = types.InlineKeyboardMarkup(row_width=2)
    for option in options:
        markup.add(types.InlineKeyboardButton(text=f"{select_symbol} {option.option_text}", callback_data=f"{question_id}_{question_number}_{option.id}_{is_single_option}_none"))
    return markup


def generate_next_markup(lang, number):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_text = "Следующий вопрос"
    if lang == "uzlatin":
        description = "Keyingi savolga o'tish"
        btn_text = "Keyingi savol"
    elif lang == "uzkiril":
        description = "Кейинги саволга отиш"
        btn_text = "Кейинги савол"

    button = types.InlineKeyboardButton(text=f">> {btn_text}", callback_data=f"next_{number}")
    markup.add(button)
    return markup


def str_to_bool(text) -> bool:
    if text == "False":
        return False
    else:
        return True