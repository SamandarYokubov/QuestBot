
## Run Locally
In order to run the project, you need to have docker-compose and docker installed.

Clone the project

```bash
  git clone https://github.com/SamandarYokubov/QuestBot.git
```

Go to the project directory

```bash
  docker-compose up -d --build
```


## Documentation

For the backend, we used microservice architecture with gRPC. So, there are 2 services and one proxy api.

#### Question Generation Service
We used OpenAI's GPT 3.5-turbo as question generation. Service accepts content(video, text or audio) and question type (multiple choice or short text), reads prompt file from local directory and sends it to OpenAI. Response from GPT 3.5-turbo is sent back to API.

#### Speech2Text
We began implementing the service, but could not finish it because of time constraints. Idea was to extract audio from video files and send it to Whisper model of OpenAI to get transcribed text and send it to Question Generation Service as content.


## API Reference

Posts parameters to the Question Generation Service or Speech2text service and parses response as json and send back it to Telegram Bot.

```http
  POST /generate_questions/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `id` | `string` | **Required**. User ID |
| `course_name` | `string` | **Required**. Name of the course |
| `course_module` | `int` | **Required**. Course module number |
| `question_type` | `string` | **Required**. Multiple choice or short answer |
| `content_type` | `string` | **Required**. Text, video or audio |



## Telegram Bot
Bot address: @questbyaibot (t.me/questbyaibot)

Telegram Bot has been used to represent the functionality of the AI system that generates pesonal course-module based questionnaire. Courses and their content were provided only for the testing purposing.

Technical stack:
- aiogram v3 package to interact with Telegram Bot APIs
- redis NoSQL database to store the context of Finite State Machine and user's dynamic data (user name, ratings and etc)
- requests package to interact with main backend app that generates questions
- Docker to containerize application

How to use bot?
1) Choose Course
2) Choose Module
3) Move to Knowledge part to read module's content
4) Move to Questions part
5) Choose either Multiple Choice (MCQ) or Short Answer (SAQ) questions
6) Wait until questions are generated by AI model
7) Start answering questions
8) Check your progress
