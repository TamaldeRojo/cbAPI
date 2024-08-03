import json
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from modules.ChatBox import ChatBox
from bson import ObjectId
from database.models.settings import Additional_info, Setting 
from database.database import count_question, get_settings_from_db, post_settings_to_db, trucate_settings_from_db, update_settings_in_db, set_additional_info, get_additional_info

html = """
<!-- index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chatbox</title>
    <style>
        body { font-family: Arial, sans-serif; }
        #chatbox { width: 300px; height: 400px; border: 1px solid #ccc; overflow-y: scroll; padding: 10px; }
        #inputContainer { display: flex; }
        #inputContainer input { flex: 1; padding: 10px; }
        #inputContainer button { padding: 10px; }
    </style>
</head>
<body>
    <div id="chatbox"></div>
    <div id="inputContainer">
        <input type="text" id="messageInput" placeholder="Type your message here...">
        <button onclick="sendMessage()">Send</button>
    </div>

    <script>
        const ws = new WebSocket("ws://localhost:8000/chatbox");

        ws.onmessage = function(event) {
            const chatbox = document.getElementById('chatbox');
            const message = document.createElement('div');
            message.textContent = event.data;
            chatbox.appendChild(message);
            chatbox.scrollTop = chatbox.scrollHeight;
        };

        function sendMessage() {
            const input = document.getElementById('messageInput');
            ws.send(input.value);
            input.value = '';
        }
    </script>
</body>
</html>

"""

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def index():
    return HTMLResponse(html)

@app.get('/settings')
async def get_settings():
    # await database.settings.insert_one({"uwu":"second_test"})
    settings = await get_settings_from_db()
    for setting in settings:
        setting["_id"] = str(setting["_id"])
    return settings

@app.post('/settings')
async def post_settings(settings: Setting):
    settings_json = settings.json()
    # print(f"{settings_json}")  
    #trucates collection
    new_settings = await post_settings_to_db(settings_json)
    return new_settings

@app.get('/trucate_settings')
async def trucate_settings():
    settings = await trucate_settings_from_db()
    return settings

@app.put('/settings')
async def update_settings(settings: Setting):
    dict_settings = settings.dict()

    updated_settings = await update_settings_in_db(dict_settings)
    return updated_settings

@app.post('/additional_info')
async def set_addional_info_endpoint(additional_info:Additional_info):
    additional_info_json = additional_info.json()
    # print(additional_info_json)
    current_additional_info = await set_additional_info(additional_info_json)
    return current_additional_info

@app.get('/additional_info')
async def get_addional_info_endpoint():
    current_additional_info = await get_additional_info()
    return current_additional_info
 

@app.post('/askQuestion')
async def askQuestion(question: str):
    chatbox = ChatBox()
    response = chatbox.askQuestion(question)
    if response:
        await count_question(question)
    
    return response


@app.websocket("/chatbox")
async def chatbox_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        chatbox = await ChatBox.start()
        data = await websocket.receive_text()

        await websocket.send_text(f"[You] {data}")
        res =  await chatbox.askQuestion(data)
        if res:
            await count_question(data)

        # print(res)
        await websocket.send_text(f"[ChatBox] {res}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000) 


