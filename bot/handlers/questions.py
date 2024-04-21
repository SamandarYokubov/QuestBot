from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery,ReplyKeyboardRemove 
import time 
from states import QuestionStates, ModuleStates, CourseStates
from keyboards import *
from utils import *
import requests
import logging

BASE_URL = "http://api:80"
ENDPOINT = "generate_questions/"

router = Router()

@router.message(ModuleStates.Questions, F.text == "🔡 Multiple Choice")
async def generate_multiple_questions(message: Message, state: FSMContext):
    await state.set_state(QuestionStates.Multiple)  
    await state.update_data(question_type="mcq")

    user_data = await state.get_data()
    user_id = user_data["user_id"]
    course = user_data["course"]
    module = user_data["module"]
    module_id = course_modules[course].index(module)
    
    await message.answer("Please wait, questions are generating...", reply_markup=back_keyboard())

    response = requests.post(BASE_URL+"/"+ENDPOINT,
                              params={"id":str(user_id),
                                    "course_name": str(course),
                                    "course_module": module_id,
                                    "question_type":"multiple_choice",
                                    "content_type":"text"})
    
    counter = 5
    while counter > 0 and response.status_code == 500 : 
        logging.info("ai service 500")
        time.sleep(2)
        response = requests.post(BASE_URL+"/"+ENDPOINT,
                        params={"id":str(user_id),
                            "course_name": str(course),
                            "course_module": module_id,
                            "question_type":"multiple_choice",
                            "content_type":"text"})
        counter = counter - 1

    if response.status_code == 500:
        logging.info("ai service doesn't work")
        await state.set_state(ModuleStates.Questions)
        await state.update_data(questions=[], question_type="", answers=[], mcq_answers=[], cur_question_index=0)

        return await message.answer(
            text="AI service currently unavailabel, please ttry later!\n\nChoose option",
            reply_markup=get_question_types_keyboard()
        )
    response_data = response.json()

    logging.info(response_data["mcq_questions"])
    await state.update_data(questions=response_data["mcq_questions"], mcq_answers=response_data["answers"])
    await state.update_data(answers=[])
    await message.answer("Are you ready?", reply_markup=get_question_start_inkeyboard())


@router.message(ModuleStates.Questions, F.text == "🅰️ Short Answer")
async def generate_short_questions(message: Message, state: FSMContext):
    await state.set_state(QuestionStates.Short)    
    await state.update_data(question_type="saq")

    user_data = await state.get_data()
    user_id = user_data["user_id"]
    course = user_data["course"]
    module = user_data["module"]
    module_id = course_modules[course].index(module)

    await message.answer("Please wait, questions are generating...", reply_markup=back_keyboard())

    response = requests.post(BASE_URL+"/"+ENDPOINT,
                                params={"id":str(user_id),
                                        "course_name": str(course),
                                        "course_module": module_id,
                                        "question_type":"multiple_choice",
                                        "content_type":"short_answer"})
        
    counter = 5
    while counter > 0 and response.status_code == 500 : 
        logging.info("ai service 500")
        time.sleep(2)
        response = requests.post(BASE_URL+"/"+ENDPOINT,
                        params={"id":str(user_id),
                            "course_name": str(course),
                            "course_module": module_id,
                            "question_type":"multiple_choice",
                            "content_type":"short_answer"})
        counter = counter - 1

    if response.status_code == 500:
        logging.info("ai service doesn't work")
        await state.set_state(ModuleStates.Questions)
        await state.update_data(questions=[], question_type="", answers=[], mcq_answers=[], cur_question_index=0)

        return await message.answer(
            text="AI service currently unavailabel, please ttry later!\n\nChoose option",
            reply_markup=get_question_types_keyboard()
        )
    response_data = response.json()

    
    await state.update_data(questions=response_data["mcq_questions"])
    await state.update_data(answers=[])
    await message.answer("Are you ready?", reply_markup=get_question_start_inkeyboard())


@router.message(QuestionStates.Short, F.text == back_title)
@router.message(QuestionStates.Multiple, F.text == back_title)
@router.message(QuestionStates.Answering, F.text == back_title)
async def go_back(message: Message, state: FSMContext):
    await state.set_state(ModuleStates.Questions)
    await state.update_data(questions=[], question_type="", answers=[], mcq_answers=[], cur_question_index=0)

    await message.answer(
        text="Cancelled\n\nChoose option",
        reply_markup=get_question_types_keyboard()
    )


@router.callback_query(F.data == "answering_start")
async def game_start(callback: CallbackQuery, state: FSMContext):

    await state.update_data(cur_question_index=0)

    user_data = await state.get_data()
    question_type = user_data["question_type"]
    questions = user_data["questions"]

    question = questions[0]["question"]
    if(question_type == "mcq"):
        choices = questions[0]["choices"]
        await callback.message.answer(
            text=f"Question:\n\n{question}",
            reply_markup = get_mcq_question_inkeyboard(choices=choices)
        )
    else:
        await state.set_state(QuestionStates.Answering)
        await callback.message.answer(
            text=f"Question:\n\n{question}"
        )
    await callback.answer()


@router.callback_query(F.data == "answering_stop")
async def game_stop(callback: CallbackQuery, state: FSMContext):    
    await state.set_state(ModuleStates.Questions)
    await state.update_data(questions=[], question_type="", answers=[], mcq_answers = [], cur_question_index=0)
    
    await callback.message.answer(
        text="Cancelled\n\nChoose option",
        reply_markup=get_question_types_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data.startswith("mcq_"))
async def mcq_answered(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    callback_data_chunk = callback.data.split('_')
    answer = callback_data_chunk[1]
    user_data["answers"].append(answer)
    await state.update_data(answers=user_data["answers"])
                            
    next_question_index = user_data["cur_question_index"] + 1

    questions_count = len(user_data["questions"])
    if(next_question_index == questions_count):
        await state.set_state(QuestionStates.Assessment)
        await callback.message.answer(text="Assessing...",
                                             reply_markup=assess_keyboard())
        return await callback.answer()
    
    question = user_data["questions"][next_question_index]["question"]
    choices = user_data["questions"][next_question_index]["choices"] 

    if(question == '' or len(choices) == 0):
        await state.set_state(QuestionStates.Assessment)
        await callback.message.answer(text="Assessing...",
                                             reply_markup=assess_keyboard())
        return await callback.answer()

    await state.update_data(cur_question_index=next_question_index)    
    await callback.message.answer(
        text=f"Question:\n\n{question}",
        reply_markup = get_mcq_question_inkeyboard(choices=choices)
    )
    await callback.answer()    


@router.message(QuestionStates.Answering, F.text)
async def answer_short(message: Message, state: FSMContext):
    user_data = await state.get_data()

    await state.update_data(user_data["answers"].append(message.text))
                            
    next_question_index = user_data["cur_question_index"] + 1
    questions_count = len(user_data["questions"])
    if(next_question_index == questions_count):
        await state.set_state(QuestionStates.Assessment)
        return await message.answer("Assessing...", reply_markup=assess_keyboard())

    question = user_data["questions"][next_question_index]["question"]

    if(question == ''):
        await state.set_state(QuestionStates.Assessment)
        return await message.answer(text="Assessing...",
                            reply_markup=assess_keyboard())
    
    await state.update_data(cur_question_index=next_question_index)

    await message.answer(
        text=f"Question:\n\n{question}",
        reply_markup=back_keyboard()
    )

    


@router.message(QuestionStates.Assessment, F.text == "➡️ Show Results ⬅️")
async def assess(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await state.update_data(user_data["answers"].append(message.text))

    course = user_data["course"]
    module = user_data["module"]
    modules = course_modules[course]
    user_progres = user_data["user_progress"]
    # answer assessing proccess

    if user_data["question_type"] == "saq":
        await state.update_data(questions=[], question_type="", answers=[], mcq_answers = [], cur_question_index=0)
        await state.set_state(CourseStates.Module)

        return  await message.answer(
            text = f"Well done!\nSorry, but short answer assessment process is under technical developement.",
            reply_markup=get_modules_keyboard(modules)
        )
    

    user_answers = user_data["answers"]
    right_answers = user_data["mcq_answers"]
    

    total_mark = 0
    for user_answer, right_answer in zip(user_answers, right_answers):
        if(user_answer == right_answer):
            total_mark = total_mark + 10

    total_mark = total_mark / len(right_answers)

    if(user_progres[course][module] < total_mark):
        await message.answer(
            text = f"Excellent\n\nYour mark for {module} is {total_mark}",
            reply_markup=get_modules_keyboard(modules)
        )
    elif(user_progres[course][module] > total_mark):
        await message.answer(
            text = f"Need to repeat\n\nYour mark for {module} is {total_mark}",
            reply_markup=get_modules_keyboard(modules)
        )
    else:
        await message.answer(
            text = f"Not bad\n\nYour mark for {module} is {total_mark}",
            reply_markup=get_modules_keyboard(modules)
        ) 

    user_progres[course][module] = total_mark

    await state.update_data(questions=[], question_type="", answers=[], mcq_answers = [], cur_question_index=0, user_progress=user_progres)

    await state.set_state(CourseStates.Module)

