from aiogram.fsm.state import StatesGroup, State

class InitialStates(StatesGroup):
    Menu = State()
    Courses = State()
    About = State()


class CourseStates(StatesGroup):
    Course = State()
    Module = State()
    Progress = State()


class ModuleStates(StatesGroup):
    Module = State()
    Knowledge = State()
    Questions = State()


class QuestionStates(StatesGroup):
    Qeustion = State()
    Multiple = State()
    Short = State()
    Answering = State()
    Assessment = State()
