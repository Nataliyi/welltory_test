import os
import json
import logging
import jsonschema
from jsonschema import validate


def json_open(num):
    """ открытие json файла"""
    with open('task_folder/event/{}'.format(json_list[num]), 'r', encoding='utf-8') as file:
        js_file = json.load(file)
        return js_file


def check_id(js_file, json_name):
    """проверка на валидность id в json"""
    json_split = json_name.split('.')
    try:
        if js_file['id'] == json_split[0]:
            return True
        elif js_file['id'] != json_split[0]:
            return False
    except:
        return False


# очищаем файл log.txt
os.system(r'cat /dev/null>log.txt')

# инициализируем файл log.txt
logging.basicConfig(filename="log.txt", level=logging.INFO)

# получаем список названий файлов json и schema
json_list = os.listdir('task_folder/event')
schema_list = os.listdir('task_folder/schema')

# создадим список схем с именами event:
event_name = []
for ev in range(len(schema_list)):
    name_split = schema_list[ev].split('.')
    event_name.append(name_split[0])

# создаем список, где после запишем не валидные json
json_not_valid = []

# запускаем проверку схем и файлов
# запишем все возникающие ошибки в файл log.txt
for j in range(len(schema_list)):
    with open('task_folder/schema/{}'.format(schema_list[j]),
              'r', encoding='utf-8') as f:
        schema_file = json.load(f)
        i = 0
        for i in range(len(json_list)):
            if json_list[i] not in json_not_valid:
                json_file = json_open(i)
                try:
                    result = check_id(json_file, json_list[i])
                    if result is True:
                        if json_file['event'] in event_name:
                            if json_file['event'] == event_name[j]:
                                validate(json_file, schema_file)
                        else:
                            raise ValueError
                    elif result is False:
                        raise KeyError
                except ValueError as v:
                    logging.warning(str(v) + " 'event': event does not match ")
                    logging.info('JSON: {}\n'.format(json_list[i]))
                    json_not_valid.append(json_list[i])
                except KeyError as k:
                    logging.warning(str(k) + " 'id': id does not match ")
                    logging.info('JSON: {}\n'.format(json_list[i]))
                    json_not_valid.append(json_list[i])
                except jsonschema.ValidationError as e:
                    error = str(e)
                    error = error.split('\n')
                    logging.error(error[0])
                    logging.info('JSON: {}'.format(json_list[i]))
                    logging.info('Schema: {}\n'.format(schema_list[j]))
                except Exception as exc:
                    error = str(exc)
                    error = error.split('\n')
                    logging.debug(error[0])
                    logging.info('JSON: {}'.format(json_list[i]))
                    logging.info('Schema: {}\n'.format(schema_list[j]))
