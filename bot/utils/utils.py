menu_items = {
    "courses": "Courses",
    "progress": "My Progress",
    "about": "About Us",
}

back_title = "Go Back"

courses_list = ["Python", "Project Management", "System Design"]

course_modules = {
    "Python" : ["Variables", "Control flow", "Functions"],
    "Project Management": ["Agile", "Scrum"],
    "System Design": ["Distributed Message Queue" ,"Load Balancer", "API Gateway"]
}

course_progress = {
    "Python" : {
        "Variables": 0,
        "Control flow": 0,
        "Functions": 0
    },
    "Project Management": {
        "Agile": 0,
        "Scrum": 0
    },
    "System Design": {
        "Distributed Message Queue": 0,
        "Load Balancer": 0,
        "API Gateway": 0
    }
}

# user_id: id
# course_name: python
# module: variables
# question_type: ['multiple choice', 'short question']
# connection_type: ["video", "text"]

# userdata: {questions: [], answers: {}}
# userState.Answering until answer.length == questions.length

# short question -> answer -> api(answers) -> assessment_answer -> user
# multiple -> calculate correct/incorrect -> show user

modules_data = {
    "Variables": "Lorem ipsum lorem ipsum novus ordus seclorum" ,
    "Control flow": "Lorem ipsum lorem ipsum novus ordus seclorum",
    "Functions": "Lorem ipsum lorem ipsum novus ordus seclorum",
    "Agile": "Lorem ipsum lorem ipsum novus ordus seclorum",
    "Scrum": "Lorem ipsum lorem ipsum novus ordus seclorum",
    "Distributed Message Queue" : "Lorem ipsum lorem ipsum novus ordus seclorum",
    "Load Balancer": "Lorem ipsum lorem ipsum novus ordus seclorum",
    "API Gateway": "Lorem ipsum lorem ipsum novus ordus seclorum"
}



mcq_questions = [
    {
        "question": "How are you Alex?",
        "choices": ["good", "very good", "bad"]
    },
        {
        "question": "How are you Tom?",
        "choices": ["good", "very good", "bad"]
    },
        {
        "question": "How are you Jenny?",
        "choices": ["good", "very good", "bad"]
    },
        {
        "question": "How are you Bob?",
        "choices": ["good", "very good", "bad"]
    }
]

saq_questions = [
        {"question": "Describe me Alex?"},
        {"question": "Describe me Tom?"},
        {"question": "Describe me Jenny?"},
        {"question": "Describe me Bob?"}
]

answers_marks = [
    1.0,
    0.5,
    0.0,
    1.0
]