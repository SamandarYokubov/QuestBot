from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup, KeyboardButton
from utils import *


def get_module_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Knowledge"))
    builder.add(KeyboardButton(text="Questions"))
    builder.add(KeyboardButton(text=str(back_title)))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

