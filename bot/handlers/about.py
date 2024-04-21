from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, BotCommand
from states import *
from keyboards import *
from utils import *


router = Router()


@router.message(InitialStates.About, 
                F.text == back_title)
async def about_back(message: Message, state: FSMContext):
    await state.set_state(InitialStates.Menu)
    await message.answer("Choose menu", reply_markup=menu_items_keyboard(menu_items=menu_items.values()))

