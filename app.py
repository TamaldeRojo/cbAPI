from fastapi import FastAPI

from modules.ChatBox import ChatBox



app = FastAPI()


@app.get('/')
def index():
    return {"message":"OLAAAAAAA"}

@app.post('/askQuestion')
def askQuestion(question: str):
    #Añadir validaciones, ids y demas cosas
    #Modificar response del endpoint    
    chatbox = ChatBox()
    response = chatbox.askQuestion(question)
    return response


@app.get('/getSettings')
def getSettings():
    #Debe retornar la configuracion de los propmts, links, responses etc etc
    return NotImplementedError()


@app.post('/updateSettings')
def updateSettings():
    #Debe modificar y luego retornar la configuracion de los propmts, links, responses etc etc
    return NotImplementedError()



