from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove, BotCommand
from states import CourseStates, ModuleStates
from keyboards import *
from utils import *


router = Router()


# modules
@router.message(CourseStates.Module, F.text != back_title)
async def get_module(message: Message, state: FSMContext):
    user_data = await state.get_data()
    course = user_data["course"]
    modules = course_modules[course]
    
    if F.text not in modules :
        return await message.answer(
                    text = "Sorry, this course does not exist!\n",
                    reply_markup = get_modules_keyboard(modules)
                )

    await state.set_state(ModuleStates.Module)
    await state.update_data(module=message.text)    
    await message.answer("Choose option",
                         reply_markup=get_module_keyboard())

@router.message(CourseStates.Module, F.text == back_title)
async def get_module_back(message: Message, state: FSMContext):
    await state.set_state(CourseStates.Course)    
    await message.answer("Choose option", reply_markup=get_course_keyboard())

@router.message(ModuleStates.Module, F.text == "📄 Knowledge")
async def get_knowledge(message: Message, state: FSMContext):
    await state.set_state(ModuleStates.Knowledge)
    user_data = await state.get_data()
    module = user_data["module"]
    module_info = modules_data[module]    
    await message.answer(f"Here is your treasure:\n\n{module_info}",
                         reply_markup=back_keyboard())

@router.message(ModuleStates.Module, F.text == "❓ Questions")
async def get_questions(message: Message, state: FSMContext):
    await state.set_state(ModuleStates.Questions)    
    await message.answer("Choose question type", reply_markup=get_question_types_keyboard())

@router.message(ModuleStates.Module, F.text == back_title)
async def get_module_back(message: Message, state: FSMContext):
    user_data = await state.get_data()
    course = user_data["course"]
    modules = course_modules[course]
    await state.update_data(module="")
    await state.set_state(CourseStates.Module)
    await message.answer("Choose module",
                            reply_markup=get_modules_keyboard(modules))

@router.message(ModuleStates.Knowledge, F.text == back_title)
async def get_knowledge_back(message: Message, state: FSMContext):
    await state.set_state(ModuleStates.Module)    
    await message.answer("Choose option", reply_markup=get_module_keyboard())

@router.message(ModuleStates.Questions, F.text == back_title)
async def get_qestions_back(message: Message, state: FSMContext):
    await state.set_state(ModuleStates.Module)    
    await message.answer("Choose option", reply_markup=get_module_keyboard())