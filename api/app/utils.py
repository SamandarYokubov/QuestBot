async def parse_as_json(request: str):
    data = {
        "question": 1,
        "choices": []
    }
    alist = []
    for quest in request.split("\n\n"):
        response = quest.split("\n")
        data["question"] = response[0]
        data["choices"] = response[1:]
        alist.append(data)
    return {"mcq_questions": alist}
        