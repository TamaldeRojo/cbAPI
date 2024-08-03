from datetime import date
import json
import time
from bson import ObjectId
from fastapi import HTTPException
from database.conn import database


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
    setting = await database.settings.find_one({"Nombre": setting_name.capitalize()})
    if setting is None:
        raise HTTPException(status_code=404, detail="Setting not found")
    setting['_id'] = str(setting['_id']) 
    return setting


async def count_question(question:str):
    question_splited = question.split()
    question_splited_lowered = [question.lower() for question in question_splited]
    settings_names = await get_settings_names()

    question_words = set(question_splited_lowered)
    settings_names_set = set(settings_names)
 
    if question_words & settings_names_set:
        word = question_words & settings_names_set
        lowered_word = list(word)[0].lower()
        setting_obj = await get_setting_by_name(lowered_word)
        if "fecha" in question_splited_lowered:
            setting_obj["Contador_fecha"] += 1 
            database.settings.update_one({'_id': ObjectId(setting_obj["_id"])},{'$set':{"Contador_fecha":setting_obj["Contador_fecha"]}})
            return            
        else:
            # print("[1]",setting_obj)
            setting_obj["Contador"] += 1 
            # print("[2]",setting_obj["_id"])
            database.settings.update_one({'_id': ObjectId(setting_obj["_id"])},{'$set':{"Contador":setting_obj["Contador"]}})
            # print("Done")
            return
