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


# progress

@router.message(CourseStates.Progress, F.text == back_title)
async def get_module_back(message: Message, state: FSMContext):
    await state.set_state(CourseStates.Course)    
    await message.answer("Choose option", reply_markup=get_course_keyboard())