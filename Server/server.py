from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from collections import defaultdict
from asyncio import Queue

app = FastAPI()

#Pydantic Class Model ---------------------------

class Question(BaseModel):
    qTitle: str
    qAnswers: list[str]
    
class Vote(BaseModel):
    qResponse: int

# This is used to validate the incoming data and error check it
#------------------------------------------------
# Every websocket connection will need its own unique queue

#----------------------------------------------------
app.add_middleware( # https://fastapi.tiangolo.com/tutorial/cors/
CORSMiddleware,
allow_origins=["*"], # Allows all origins
allow_credentials=True,
allow_methods=["*"], # Allows all methods
allow_headers=["*"], # Allows all headers
)
#----------------------------------------------------

#- Creating a queue to store responses
q = Queue()
responses = defaultdict(int)
questions = {}

#- Default Page
@app.get("/",response_class=HTMLResponse,status_code=200)
async def Default():
    return """
    <html>
        <head>
            <title>I'm Sorry I think You're Lost....</title>
        </head>
        <body>
            <h1>I'm Sorry I think You're Lost....</h1>
            <h2>This is not the page you are looking for</h2>
        </body>
    </html>
    """

#- Question submission endpoint 
@app.post("/question")
async def make_question(question: Question):

    questionTitle = question.dict()
    
    max_value = max(questions, key=questions.get, default=0)
    max_value = max_value + 1
    questions[max_value] = dict(questionTitle)
    
    return "Success",questions

#- Question retrieval endpoint
@app.get("/question/")
async def return_items():
    return questions

#- Vote submission endpoint
@app.post("/response")
async def accept_vote(vote: Vote):
    responses[vote.qResponse] += 1

    await q.put(responses)
    return "Success"

#- Websocket endpoint
@app.websocket("/wss") #https://fastapi.tiangolo.com/advanced/websockets/
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True: #ques put and get
            data = await q.get()
            await websocket.send_json(data)
    except:
        pass
