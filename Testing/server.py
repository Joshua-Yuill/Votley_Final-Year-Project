from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
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
#------------------------------------------------
# Every websocket connection will need its own unique queue

q = Queue()

responses = defaultdict(int)

questions = {}



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
    
    

@app.post("/question")
async def make_question(question: Question):
    print("start")

    questionTitle = question.dict()
    
    print(question.dict())
    print(questionTitle["qTitle"])

    return "Success"


@app.post("/response")
async def accept_vote(vote: Vote):
    
    responses[vote.qResponse] += 1

    await q.put(responses)
    print(responses)
    return "Success"




@app.websocket("/wss")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True: #ques put and get
            data = await q.get()
            await websocket.send_json(data)
            print("websocket", data)
    except:
        pass