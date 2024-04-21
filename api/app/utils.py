import logging

async def parse_as_json(request: str):
    
    alist = []
    questions, answers = request.split("Answers")
    logging.info(questions)
    for quest in questions.split("\n\n"):
        logging.info(quest)
        response = quest.split("\n")
        alist.append({"question": response[0], "choices": response[1:]})
    return {"mcq_questions": alist,
            "answers": answers.split("\n")}