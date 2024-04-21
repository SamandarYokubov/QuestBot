from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove, BotCommand
from states import InitialStates, CourseStates
from keyboards import *
from utils import *


router = Router()

# courses  

@router.message(CourseStates.Course, F.text == "📖 Modules")
async def choose_course_modules(message: Message, state: FSMContext):
    user_data = await state.get_data()
    course = user_data["course"]
    modules = course_modules[course]
    await state.set_state(CourseStates.Module)
    await message.answer("Choose module",
                            reply_markup=get_modules_keyboard(modules))

@router.message(CourseStates.Course, F.text == "📈 My Progress")
async def choose_course_progress(message: Message, state: FSMContext):
    await state.set_state(CourseStates.Progress)

    user_data = await state.get_data()
    user_progres = user_data["user_progress"]
    course = user_data["course"]
    course_marks = user_progres[course]
    progress_result = "Your progress for Multiple Choice Questions:\n\n"
    for key, value in course_marks.items():
        progress_result += f"{key} -> {value}\n"
    await message.answer(progress_result, reply_markup=back_keyboard())

@router.message(CourseStates.Course, F.text == back_title)
async def choose_course_back(message: Message, state: FSMContext):
    await state.set_state(InitialStates.Courses)
    await message.answer("Choose course", reply_markup=get_courses_keyboard())

@router.message(CourseStates.Course)
async def choose_course_incorrect(message: Message):
    await message.answer(
        text = "Sorry, this course does not exist!\n",
        reply_markup = get_course_keyboard()
    )

