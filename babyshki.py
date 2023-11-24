from fast_bitrix24 import Bitrix
import workYDB
import os
from dataclasses import dataclass


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
    deal = bit.call('crm.deal.add', param)
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
    })
    
    print(f'{contact=}')
    return contact



def create_type(fields):
    param ={'fields':{
        'title':fields['name'],
        Typee.infoForProject: f"{fields['id']} - {fields['url']}"
    }}
    typee = bit.call('crm.type.add', param)
    print("test answer. "+typee)
    return typee

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