from pydantic import BaseModel, Field


class Additional_info(BaseModel):
    Additional_info: str = Field(...,examples="Saluda antes de responder")

class Setting(BaseModel):
    Nombre: str = Field(None,examples="Titulo")
    Hora: str = Field(None,examples="7:00 AM")
    Costo: str = Field(None, example="5000 Mxn")
    Fecha_limite: str = Field(None, example="3/6/2067")
    Tiempo_entrega: str = Field(None, example="2 dias")
    Medio_entrega: str = Field(None, example="Por correo")
    Lugar: str = Field(None,examples="UTCH BIS")
    Item: bool = Field(False,examples=True)
    Contador: int = Field(None,examples=0)
    Contador_fecha: int = Field(None,examples=0)
    Comment: str = Field(None,examples="Only weekends")