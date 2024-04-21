from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup, KeyboardButton
from utils import *


def menu_items_keyboard(menu_items: list) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in menu_items]    
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


def back_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text=str(back_title)))
    return builder.as_markup(resize_keyboard=True)