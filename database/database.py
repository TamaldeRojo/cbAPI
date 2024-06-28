import json
from bson import ObjectId
from database.conn import database


async def get_additional_info()->dict:
    adional_info_cursor = database.additionalInfo.find()
    adional_info = await adional_info_cursor.to_list(1) 
    for info in adional_info:
        info['_id'] = str(info["_id"]) 
    return adional_info

async def set_additional_info(additional_info: json):
    await database.additionalInfo.delete_many({})
    await database.additionalInfo.insert_one(json.loads(additional_info))
    return await get_additional_info()

async def get_settings_from_db() -> dict:
    settings_cursor = database.settings.find()
    settings = await settings_cursor.to_list(1) 
    for setting in settings:
        setting['_id'] = str(setting['_id'])
    return settings

async def post_settings_to_db(settings_json: json) -> dict:

    await database.settings.delete_many({})
    #inserts the new settings
    await database.settings.insert_one(json.loads(settings_json))

    return await get_settings_from_db()

async def update_settings_in_db(settings_json:json):

    settings_cursor = database.settings.find()
    current_settings = await settings_cursor.to_list(1) 
    print(f'[+] {current_settings[0]['_id']}')

    await database.settings.update_one(
        {"_id": ObjectId(current_settings[0]['_id'])}, #settings_id
        {'$set': json.loads(settings_json)})
    # print('a')
    updated_settings = await get_settings_from_db()
    updated_settings[0]['_id'] = str(updated_settings[0]['_id']) 
    return updated_settings

async def get_settings_keys() -> list[str]:
    questions_in_db = await get_settings_from_db()
    question_keys = [list(question.keys()) for  question in questions_in_db][0]
    return question_keys

async def count_question(question:str):
    question_splited = question.split()
    settings_keys = await get_settings_keys()
    settings_keys_set = set(settings_keys)
    question_words = set(question_splited)
    
    if question_words & settings_keys_set:
        print(question_words & settings_keys_set)
        

# async def sum_question_counter(word:str):
#     settings_keys = await get_settings_keys()



    