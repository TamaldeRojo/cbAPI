import g4f
from unidecode import unidecode

class ChatBox:
    def __init__(self) -> None:
        self.webLink = "www.utch.edu.mx"
        self.defaultRes = f"No se ha encontrado una respuesta a tu pregunta. Por favor revisa la página oficial para más información {self.webLink}"


    def askQuestion(self,question: str) -> str:
        # questionData = self._parseQuestion(question)
        if type(question) == str:
            try:
                dbData = self._getDataFromDB()
                prompt =  f"Responde a esta pregunta en el mismo idioma en el que se hace: [{question}] ; Pero basandote exclusivamente en la siguiente información: {dbData}. Si con la información no se puede responder a la pregunta entonces devuelve la siguiente frase en el mismo idoma en la que ha sido hecha la pregunta: {self.defaultRes}"
                
                res = self.writePrompt(prompt)
                if res is not None:
                    print(res)
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
    
    def writePrompt(self,prompt) -> str:
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_35_turbo,
            messages=[{'role':'user','content':prompt}]
        )
        self._logMessage("Got response Successfully")
        return response
    
    def _getDataFromDB(self) -> object:
        try:
            #retrieve data from the
            data = {
            "Constancia" : {
                "Costo": "5000 Mxn",
                "fecha limite":"3/6/2067",
                "Tiempo entrega":"2 dias",
                "Medio entrega":"Por correo",
                }
            }
            return data
        
        except Exception as e:
            self._logError('There has been an error: ',e)
            return None
    
    
    
    # OPTIONAL
    @staticmethod
    def _parseQuestion(question:str):
        unidecodedQuestion = unidecode(question)
        questionFormated = unidecodedQuestion.lower()
        questionData = questionFormated.split()
        return questionData
    
    
        
    