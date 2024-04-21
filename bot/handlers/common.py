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

@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state:FSMContext):
    await state.clear()
    await state.update_data(id=message.from_user.id, first_name=message.from_user.first_name, user_progress=course_progress) 
    await message.answer(
        text = f"Welcome {message.from_user.first_name} {message.from_user.last_name}",
        reply_markup = menu_items_keyboard(menu_items=menu_items.values())
    )
    await state.set_state(InitialStates.Menu)

@router.message(InitialStates.Menu,
                F.text.in_(menu_items.values()))
async def choose_menu(message: Message, state: FSMContext):
    print(message.text)   
    if(message.text == menu_items["courses"]):
        await message.answer("Choose Courses",
                             reply_markup=get_courses_keyboard())
        return await state.set_state(InitialStates.Courses)
    elif(message.text == menu_items["about"]):
        await message.answer("We aim to check your progress",
                             reply_markup=back_keyboard())
        return await state.set_state(InitialStates.About)

@router.message(InitialStates.Menu)
async def choose_menu_incorrect(message: Message):
    await message.answer(
        text = "Sorry, this option does not exist!\n",
        reply_markup = menu_items_keyboard(menu_items=menu_items.values())
    )

@router.message(InitialStates.Courses,
                F.text.in_(courses_list))
async def choose_course(message: Message, state: FSMContext):
    await  state.update_data(course=message.text)
    await message.answer("Choose option",
                         reply_markup=get_course_keyboard())
    await state.set_state(CourseStates.Course)

@router.message(InitialStates.Courses,
                F.text == back_title)
async def choose_courses_back(message: Message, state: FSMContext):
    await state.set_state(InitialStates.Menu)
    await message.answer("Choose menu", reply_markup=menu_items_keyboard(menu_items=menu_items.values()))

@router.message(InitialStates.Courses)
async def choose_courses_incorrect(message: Message):
    await message.answer(
        text = "Sorry, this course does not exist!\n",
        reply_markup = get_courses_keyboard()
    )
