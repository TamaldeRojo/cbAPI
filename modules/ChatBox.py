import os
import g4f
from dotenv import load_dotenv
from openai import OpenAI, api_key
from unidecode import unidecode
from database.database import get_additional_info, get_settings_from_db
from langdetect import detect,detect_langs
from dotenv import load_dotenv

load_dotenv()
MODEL = os.getenv('MODEL')


class ChatBox:
    def __init__(self) -> None:
        
        self.entityData = None  
        self.questionsData = None 
        self.additional_Info = None 

        self.defaultRes = None 
        self.globalPrompt = None

        self.client = None

    async def askQuestion(self,question: str) -> str:
        self._logMessage("Asking Question...")
        if not type(question) == str:
            raise TypeError("[-] Question needs to be in string format")
        try:
            prompt = question   
            self._logMessage(prompt)
            res = await self.writePrompt(prompt)
            return res
            
        except Exception as e:
            self._logError('',e)
            return
    
    @staticmethod
    def _logMessage(msg:str):
        print(f"[+] {msg}")
    
    @staticmethod  
    def _logError(message,error):
        redColor = "\033[91m"
        resetColor = "\033[0m"
        
        print(f"{redColor}[-] {message}{resetColor}\n{error}\n")
    
    async def writePrompt(self,prompt) -> str:

        while True:
            response = self.client.chat.completions.create(
                model=MODEL,
                temperature=0.5,
                max_tokens=100,
                messages=[
                    {"role": "system", "content": self.globalPrompt},
                    {"role":"user","content":prompt}
                    ],
                # stream=True,
            )
            res = response.choices[0].message.content
            print(res)
            return res
           
             
    async def _getQuestionsDataFromDB(self) -> dict:
        try:   
            data = await get_settings_from_db()
            if not data:
                return None
            return data
        
        except Exception as e:
            self._logError("Failed at retrieving Question Data From Database",e)
               
    def _getEntityDataFromDB(self)-> dict:
        try:
            entityData = {
                "name" : "UTCH",
                "webLink" : "www.utch.edu.mx",
                "director/a" : "Vianey" 
                }

            return entityData
        
        except Exception as e:
            self._logError("Failed at retrieving Entity Data From Database",e)
            
    async def _getAdditional_InfoFromDb(self) -> dict:
        try:
            additional_info = await get_additional_info()
            if not additional_info:
                return None

            return additional_info
        except Exception as e:
            self._logError('There has been an error of type: ',e)

    async def async_init(self) -> 'ChatBox':
        self.entityData = self._getEntityDataFromDB()
        self.questionsData = await self._getQuestionsDataFromDB()

        self.additional_Info = f"Traduce todo al idioma de la pregunta, incluyendo lo que ordene lo siguiente: {await self._getAdditional_InfoFromDb() or None}" 
        self.defaultRes = f'No se ha encontrado una respuesta a tu pregunta. Por favor revisa la página oficial para más información {self.entityData["webLink"]} o intentalo más tarde.'        
        self.globalPrompt = f"Se te haran varias preguntas responde basandote en la siguiente información {self.questionsData}. Si con la información no se puede responder a la pregunta entonces devuelve la siguiente frase : {self.defaultRes}. Jamás respondas algo que no sea lo que se te pide pero brinda mas informacion como fechas,costos,medios de entrega, etc. Cumple las siguientes ordenes: {self.additional_Info}."

        API_KEY = os.getenv('OPENAI_API_KEY')
        api_key = API_KEY
        self.client = OpenAI()
        return self
    
    @classmethod
    async def start(cls) -> 'ChatBox':
        self = cls()
        await self.async_init()
        return self 

    # OPTIONAL
    @staticmethod
    def _parseQuestion(question:str):
        unidecodedQuestion = unidecode(question)
        questionFormated = unidecodedQuestion.lower()
        questionData = questionFormated.split()
        return questionData
    
    
    