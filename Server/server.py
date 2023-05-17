# Importing Libraries -----------------------------
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from collections import defaultdict
from asyncio import Queue

app = FastAPI() # Create a FastAPI instance

#Pydantic Class Model ---------------------------
class Question(BaseModel):
    qTitle: str
    qAnswers: list[str]
    
class Vote(BaseModel):
    qResponse: int

q = Queue() # Create a queue for the websocket connections

responses = defaultdict(int) # Create a dictionary to store the responses
questions = {}

# Default Route ---------------------------------
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
    
    
# Post Question Route ----------------------------------------
@app.post("/question")
async def make_question(question: Question):
    print("start")

    questionTitle = question.dict() # Convert the question to a dictionary and store it in a variable
    
    max_value = max(questions, key=questions.get, default=0)
    max_value = max_value + 1
    questions[max_value] = dict(questionTitle) # Add the question to the questions dictionary
    
    return "Success",questions

# Get Question Route ----------------------------------------
@app.get("/question/")
async def return_items():
    print(questions)
    return questions


# Vote Acceptance Route ----------------------------------------
@app.post("/response")
async def accept_vote(vote: Vote):
    
    responses[vote.qResponse] += 1

    await q.put(responses)
    print(responses)
    return "Success"

# Websocket Route ----------------------------------------
@app.websocket("/wss")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True: #ques put and get
            data = await q.get() # Get the data from the queue
            await websocket.send_json(data) # Send the data to the client
            print("websocket", data)
    except:
        pass
