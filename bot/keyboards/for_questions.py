from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardBuilder,InlineKeyboardButton
from utils import *



def get_question_types_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Multiple Choice"))
    builder.add(KeyboardButton(text="Short Answer"))
    builder.add(KeyboardButton(text=str(back_title)))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def get_question_start_inkeyboard() -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Let's Go",
        callback_data="answering_start")
    )

    builder.add(InlineKeyboardButton(
        text="Cancel",
        callback_data="answering_stop")
    )

    return builder.as_markup()

def get_mcq_question_inkeyboard(choices: list) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for choice in choices:
        call_data = "mcq_" + choice
        builder.add(InlineKeyboardButton(
            text=choice,
            callback_data=call_data)
        )

    return builder.as_markup()


def assess_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Show Results"))
    return builder.as_markup(resize_keyboard=True)