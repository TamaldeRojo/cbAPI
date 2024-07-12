import os
import g4f
from dotenv import load_dotenv
# from openai import OpenAI
from unidecode import unidecode
from database.database import get_additional_info, get_settings_from_db
from langdetect import detect,detect_langs

class ChatBox:
    def __init__(self) -> None:

        self.entityData = None  
        self.questionsData = None 
        self.additional_Info = None 

        self.defaultRes = None 
        self.globalPrompt = None

    async def askQuestion(self,question: str) -> str:
        self._logMessage("Asking Question...")
        if not type(question) == str:
            raise TypeError("[-] Question needs to be in string format")
        try:
            prompt = self.globalPrompt + question   
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
            response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_35_turbo,
            messages=[{'role':'user','content':prompt}]
            )
            self._logMessage("Got response Successfully")
            
            self._logMessage(detect(response))
            
            if not response:
                return await self.writePrompt(prompt)
            
            if detect(response) in ['zh-cn','zh-tw','ko','ca']:
                self._logMessage('[-] bad response, trying again')
                print(response)
                continue
                # print(await self.writePrompt(prompt))
                
            print("Respuesta sin chino",response)
            return response
             
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
            # print('aquiiiiiiiiiiiiiiiiiiiiiiii',additional_info)
            if not additional_info:
                return None

            return additional_info
        except Exception as e:
            self._logError('There has been an error of type: ',e)

    async def async_init(self) -> 'ChatBox':
        self.entityData = self._getEntityDataFromDB()
        self.questionsData = await self._getQuestionsDataFromDB()

        self.additional_Info = None
        self.defaultRes = f"No se ha encontrado una respuesta a tu pregunta. Por favor revisa la página oficial para más información {self.entityData["webLink"]} o intentalo más tarde."        
        self.globalPrompt = f"Se te hara una pregunta respondela en Español basandote en la siguiente información {self.questionsData}. Si con la información no se puede responder a la pregunta entonces devuelve la siguiente frase en el mismo idoma en la que ha sido hecha la pregunta: {self.defaultRes}. Jamás respondas algo que no sea lo que se te pide. Cumple la siguiente orden u ordenes: {self.additional_Info}. La pregunta es: "

        return self
    
    @classmethod
    async def start(cls) -> 'ChatBox':
        self = cls()
        await self.async_init()
        return self 

    # async def get_settings(self):
        
        settings_setup = {
            "entity_data" : self.entityData,
            "question_data" : self.questionsData,
            "additional_info" : self.additional_Info,
            "default_response" : self.defaultRes,
            "global_prompt":self.globalPrompt,
        }

        return settings_setup
    
    # async def update_settings(self,defaultPrompt=None):
        
    #     self.defaultRes = self._update_defaultPrompt(self,defaultPrompt)

    #     settings_setup = {
    #         "entity_data" : self.entityData,
    #         "question_data" : self.questionsData,
    #         "additional_info" : self.additional_Info,
    #         "default_response" : self.defaultRes,
    #         "global_prompt":self.globalPrompt,
    #     }

    #     return settings_setup
    
    # def _update_defaultPrompt(self,defaultPrompt=None):
    #     #update database
    #     self.defaultRes = defaultPrompt
    #     return self.defaultRes

    # OPTIONAL
    @staticmethod
    def _parseQuestion(question:str):
        unidecodedQuestion = unidecode(question)
        questionFormated = unidecodedQuestion.lower()
        questionData = questionFormated.split()
        return questionData
    
    
    