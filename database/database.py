from datetime import date
import json
import time
from bson import ObjectId
from fastapi import HTTPException
from database.conn import database
from utils.log import log_message
from utils.prompt import get_gpt_Response


async def get_additional_info()->dict:
    adional_info_cursor = database.additionalinfos.find()
    adional_info = await adional_info_cursor.to_list(100) 
    for info in adional_info:
        del info['_id']  
    return adional_info

async def set_additional_info(additional_info: json):
    await database.additionalInfo.delete_many({})
    await database.additionalInfo.insert_one(json.loads(additional_info))
    return await get_additional_info()

async def get_settings_from_db() -> dict:
    settings_cursor = database.settings.find()
    settings = await settings_cursor.to_list(1000) 
    for setting in settings:
        del setting['_id'] 
        # del setting['__v']  

    return settings

async def trucate_settings_from_db() -> dict:
    await database.settings.delete_many({})
    settings = await get_settings_from_db()
    return settings


async def post_settings_to_db(settings_json: json) -> dict:
    await database.settings.insert_one(json.loads(settings_json))
    return await get_settings_from_db()

async def update_settings_in_db(new_settings_dict :dict):
    current_setting = await get_setting_by_name(new_settings_dict["Nombre"])
  
    database.settings.update_one({"_id": ObjectId(current_setting["_id"])},{"$set":new_settings_dict})
   
    updated_settings = await get_settings_from_db()
    updated_settings[0]['_id'] = str(updated_settings[0]['_id']) 
    return updated_settings


async def get_settings_names() -> list[str]:

    questions_in_db = await get_settings_from_db()
    question_names = [question["Nombre"].lower() for question in questions_in_db]
    return question_names


async def get_setting_by_name(setting_name:str)->json:
    setting = await database.settings.find_one({"Nombre": setting_name})
    if setting is None:
        raise HTTPException(status_code=404, detail="Setting not found")
    setting['_id'] = str(setting['_id']) 
    return setting


async def count_question(question:str):
    try:
        settings_names = await get_settings_names()

        context = """
            Eres un validador el cual recibe una pregunta y una lista de nombres, si la pregunta busca algo relacionado sobre algun elemento de la lista de nombres responde (SIEMPRE EN ESPAÑOL) de la siguiente forma: Nombre;(palabra clave de que quiere saber, fecha, precio etc..); , de lo contrario responde con un 0 
            """
        prompt = f"pregunta : '{question}'. Lista de nombres: {settings_names}."
        res = await get_gpt_Response(prompt,context)
        print(res)
        res_splited = res.split(";")


        if res != "0":
            print("a")
            setting_obj = await get_setting_by_name(res_splited[0])
            print(setting_obj)
            
            if res_splited[1] == "fecha":    
                setting_obj["Contador_fecha"] += 1 
                await database.settings.update_one({'_id': ObjectId(setting_obj["_id"])},{'$inc':{"Contador_fecha":setting_obj["Contador_fecha"]}})
                log_message("Done")
                return
            else:
                print("Pregunto por precio")
                await database.settings.update_one({'_id': ObjectId(setting_obj["_id"])},{'$inc':{"Contador": 1}})
                # setting_obj["Contador"] += 1 
                log_message("Done")
                return
        return
    
    except Exception as e:
        return
  