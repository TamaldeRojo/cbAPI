from pydantic import BaseModel, Field

class DocumentDetails(BaseModel):
    Costo: str = Field(..., example="5000 Mxn")
    fecha_limite: str = Field(..., example="3/6/2067")
    Tiempo_entrega: str = Field(..., example="2 dias")
    Medio_entrega: str = Field(..., example="Por correo")

class SettingsSchema(BaseModel):
    Constancia: DocumentDetails
    Titulo: DocumentDetails

class Additional_info(BaseModel):
    Additional_info: str = Field(...,examples="Saluda antes de responder")