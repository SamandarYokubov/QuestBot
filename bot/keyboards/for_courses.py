from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup, KeyboardButton
from utils import *


def get_courses_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for course_name in courses_list:
        builder.add(KeyboardButton(text=str(course_name)))
    builder.adjust(3)   
    builder.add(KeyboardButton(text=str(back_title)))
    return builder.as_markup(resize_keyboard=True)


def get_course_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="📖 Modules"))
    builder.add(KeyboardButton(text="📈 My Progress"))
    builder.add(KeyboardButton(text=str(back_title)))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def get_modules_keyboard(modules: list) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for module in modules:
        builder.add(KeyboardButton(text=str(module)))
    builder.add(KeyboardButton(text=str(back_title)))
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=True)