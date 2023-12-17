from fast_bitrix24 import Bitrix
import workYDB
import os
from dataclasses import dataclass
from pprint import pprint
import csv

sql=workYDB.Ydb()
webhook = os.getenv('WEBHOOK')
bit = Bitrix(webhook)

@dataclass
class Typee:
    infoForProject :str = 'ufCrm1683522990823'

def create_task():
    param = {'fields':{
        'TITLE':'',

    }}
    task = bit.call('tasks.task.add',params=param)
    return task

def create_deal(fields):
    param = {'fields':{
        'TITLE': fields['nameProject'],
        'UF_CRM_1683522990823': fields['description'],
        'UF_CRM_1679652371105': [fields['img']],
        'UF_CRM_1683523356895': [fields['document']],
        'UF_CRM_1682092751': fields['bandSize'],
        'UF_CRM_1682092714': fields['hours'],
        'UF_CRM_1681134225889': [fields['date']],
        'OPPORTUNITY': fields['budget'],
        #'': fields[''],
    }}
    deal = bit.call('crm.deal.add', param, raw=True)
    
    
    
    return deal

def update_deal(dealID, fields):
    param = {
        'ID': dealID,
        'fields':{
        'TITLE': fields['nameProject'],
        'UF_CRM_1683522990823': fields['description'],
        'UF_CRM_1679652371105': [fields['img']],
        'UF_CRM_1683523356895': [fields['document']],
        'UF_CRM_1682092751': fields['bandSize'],
        'UF_CRM_1682092714': fields['hours'],
        'UF_CRM_1681134225889': [fields['date']],
        'OPPORTUNITY': fields['budget'],
        #'': fields[''],
    }}
    deal = bit.call('crm.deal.update', param)
    return deal

def find_contact(phone:str):
    contact = bit.get_all(
    'crm.contact.list',
    params={
        'select': ['*', 'UF_*'],
        'filter': {'PHONE': phone}
    },)
    pprint(contact)
    if contact==[]:
        return None
    else:
        return contact[0]

def create_contact(fields):
    """Domofon
NoteAddress 
UrlFileAddress 
FullNameContact
Phone
    """
    params ={
        'fields':{
            'NAME':fields['FullNameContact'],
            'PHONE': [{'VALUE': fields['Phone'], 'VALUE_TYPE': 'WORK'}],
            'UF_CRM_1626798986': fields['Domofon'],
            'UF_CRM_1626799002': fields['NoteAddress'],
            'UF_CRM_1626799017': fields['UrlFileAddress'],
            'UF_CRM_1626799032': fields['FullNameContact'],
            'UF_CRM_1626799047': fields['Phone'],
        }
    }
    contactID = bit.call('crm.contact.add', params=params)
    return contactID

def prepare_parking_size(fields:list)-> int:
    match fields:
        case {'ParkingSize10': True}:
            return 203
        case {'ParkingTracks': True}:
            return 205
        case {'ParkingNot': True}:
            return 207
    
def prepare_parking_distance(fields:list)-> int:
    match fields:
        case {'ParkingDistance': True}:
            return 209
        case {'ParkingDistanceId': True}:
            return 211
        case {'ParkingDistanceMore': True}:
            return 213
        case _:
            return 213
    
def prepare_lift(fields:list)-> int:
    match fields:
        case {'Lift': True}:
            return 415
        case {'LiftLight': True}:
            return 417
        case {'LiftNot': True}:
            return 419
    
def prepare_power_electric(fields:list)-> int:
    if fields['PowerElectric'] < 25:
        return 221
    elif fields['PowerElectric'] < 50:
        return 223
    elif fields['PowerElectric'] < 110:
        return 225
    elif fields['PowerElectric'] > 110:
        return 227
    
def prepare_neighbors(fields:list)-> int:
    match fields:
        case {'NeighborsId': '1'}:
            return 251
        case {'NeighborsId': '2'}:
            return 255
        case {'NeighborsId': '3'}:
            return 349
        case _:
            return None

def prepare_region(fields:list)-> int:
    #"Москва и МО / Санкт-Петербург / Другой"
    match fields:
        case {'Region': 'Москва и МО'}:
            return 409
        case {'Region': 'Санкт-Петербург'}:
            return 411
        case {'Region': 'Другой'}:
            return 413
        case _:
            return 413





def create_item_for_type(fields):
    phone = fields['Phone']
    contact = find_contact(phone)
    if contact is None:
        # contactID = create_contact(fields)
        contactID = 1
        pprint('create contact')
    else:
        contactID = contact['ID']

    param ={
        'entityTypeId': 148, #айди смарт-процесса
        'fields':{
            'TITLE':fields['name'],
            'contact_ids':[contactID],
            'UF_CRM_9_1675171164797':fields['Description'],
            'UF_CRM_9_1682762320540':fields['Floor'],
            'UF_CRM_9_1668085148734':fields['Street'],
            'UF_CRM_9_1682760618':prepare_region(fields),
            'UF_CRM_9_1673343598553':prepare_parking_distance(fields), #Проверить что приходит
            'UF_CRM_9_1673353169991':fields['ParkingPass'],
            'UF_CRM_9_1672215203766':fields['Square'],
            'UF_CRM_9_1682762421905':prepare_lift(fields),
            'UF_CRM_9_1678984393':fields['MinCeilingHeight'],
            'UF_CRM_9_1678984447':fields['MaxCeilingHeight'],
            'UF_CRM_9_1673354082728':prepare_neighbors(fields), #Проверить что приходит
            'UF_CRM_9_1673353720769':fields['MyAnimal'],
            'UF_CRM_9_1673354199125':fields['Animal'],
            'UF_CRM_9_1673343312187':prepare_parking_size(fields),
            'UF_CRM_9_1673351367456':prepare_power_electric(fields),
            'UF_CRM_9_1672215203766':fields['Square'],  
    }}
    pprint(param)
    1/0
    # typee = bit.call('crm.item.add', param, raw=True)
    # print("test answer. "+typee)
    
    
    return typee


def create_type(fields):
    param ={'fields':{
        'title':fields['name'],
        Typee.infoForProject: f"{fields['id']} - {fields['url']}"
    }}
    typee = bit.call('crm.type.add', param)
    print("test answer. "+typee)
    row = {'id': typee,'entity_type':'type'}
    sql.replace_query('entity',row)
    return typee

def get_type_fields():
    param ={
        'entityTypeId': 148, #айди смарт-процесса
    }
    fields = bit.call('crm.item.fields', param, raw=True)
    # pprint(fields['result']['fields'])
    return fields

def prepare_fields(fields):
    fields = fields['result']['fields']
    i = 0
    for fieldID, value in fields.items():
        dictFields = {}
        if not fieldID.startswith('ufCrm'): continue
        title = value['title']
        type = value['type']
        upperName = value['upperName']
        
        dictFields['title'] = title
        dictFields['type'] = type
        dictFields['upperName'] = upperName
        dictFields['fieldID'] = fieldID
        dictFields['value'] = ''

        text =f"{fieldID}/{upperName} - {title} - {type}\n"
        if type == 'enumeration':
            textEnum = ''
            for item in value['items']:
                textEnum += f"{item['ID']} - {item['VALUE']}\n"
            # print(textEnum)
            text += textEnum
            dictFields['value'] = textEnum   

        if type == 'boolean':
            textEnum = ''
            # for item in value['settings']:
                # textEnum += f"{item['ID']} - {item['VALUE']}\n"
            textEnum += f"{'/'.join(value['settings']['LABEL'])} \n"
            # print(textEnum)
            text += textEnum
            dictFields['value'] = textEnum

        if type in ['crm_entity', 'crm_company']:
            textEnum = value['settings']+'\n'
            text += textEnum
            dictFields['value'] = textEnum

        if type == 'crm_status':
            textEnum = value['statusType']+'\n'
            text += textEnum
            dictFields['value'] = textEnum
        print(text)

        fileName = 'fields.csv'
        with open(fileName, 'a', newline='') as csvfile:
            fieldnames = dictFields.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)            
            
            if i != 0:
                writer.writerow(dictFields) 
            else:
                print('create')
                writer.writeheader()
                writer.writerow(dictFields) 
        i+=1      

def handler(event, context):

    print(f'{event=}')
    print(f'{context=}')

    #data = event['headers']['queryStringParameters']
    params = event['queryStringParameters']
    #params = data['params'] #все поля
    
    #method = data['method'] #{'method':'update.task'}
    #print(f'{data=}')
    print(f'{params=}')
    #print(f'{method=}')
    method = params['method']

    deal = '1'
    typee = '1'
    if method == 'deal':
        #task = create_task(params)
        deal = create_deal(params)
        print(deal)
        row = {'id': deal,'entity_type':'deal'}
        sql.replace_query('entity',row)
        
        return {
            'statusCode': 200,
            'body': f'OK для сделки {deal}'
        }

    elif method == 'type':
        typee = create_type(params)
        print(f'{typee=}')
        row = {'id': typee,'entity_type':'type'}
        sql.replace_query('entity',row)
        
        return {
            'statusCode': 200,
            'body': f'OK для процесса {deal}'
        }
    
    elif method == 'dealupdate':
        update_deal(169, params)
        deal = 169
    return {
        'statusCode': 200,
        'body': f'OK для сделки {deal}'
    }



if __name__ == '__main__':
    phone = '+79253792174'
    # a = find_contact(phone)
    # pprint(a)
    fields = {'NeighborsId': '1'}
    a = prepare_neighbors(fields) == 251
    print(a)

# fields = get_type_fields()
# prepare_fields(fields)
# fileName = 'fields.csv'
# a = os.path.exists(fileName)
# print(a)