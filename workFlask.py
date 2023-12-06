from flask import Flask, request, render_template
from loguru import logger
from flask_restx import Api, Resource, fields
from dotenv import load_dotenv
from babyshki import *

load_dotenv()

app = Flask(__name__)
api = Api(app, version='1.0', title='Итнеграция с битриксом', description="Bitrix API", default_label='Запросы',  default='⬇️')


create_deal_model = api.model('Create deal', {
    'nameProject': fields.String(description='nameProject', required=True),
    'description': fields.String(description='description', required=True),
    'img': fields.Url(description='imgUrl', required=True),
    'document': fields.Url(description='documentUrl', required=True),
    'bandSize': fields.String(description='bandSize', required=True),
    'hours': fields.String(description='hours', required=True),
    'date': fields.String(description='date', required=True),
    # 'budget': fields.Integer(description='budget', required=True),
    'budget': fields.Float(description='budget', required=True),
})

update_deal_model = api.model('Update deal', {
    'id': fields.String(description='id', required=True),
    'nameProject': fields.String(description='nameProject', required=True),
    'description': fields.String(description='description', required=True),
    'img': fields.Url(description='imgUrl', required=True),
    'document': fields.Url(description='documentUrl', required=True),
    'bandSize': fields.String(description='bandSize', required=True),
    'hours': fields.String(description='hours', required=True),
    'date': fields.String(description='date', required=True),
    'budget': fields.Float(description='budget', required=True),
})

"""Domofon
NoteAddress 
UrlFileAddress 
FullNameContact
Phone
    """
create_type_model = api.model('Create type', {
    'name': fields.String(description='name', required=True),
    'id': fields.String(description='id', required=True),
    'Description': fields.String(description='Description', required=True),

    'Street': fields.String(description='Street', required=True),
    'Region': fields.String(description='Region', required=True),
    'City': fields.String(description='City', required=True),
    'Country': fields.String(description='Country', required=True),
    'HousNumber': fields.String(description='HousNumber', required=True),
    'OfficeNumber': fields.String(description='OfficeNumber', required=True),

    'Domofon': fields.String(description='Domofon', required=True),
    'NoteAddress': fields.String(description='NoteAddress', required=True),
    'UrlFileAddress': fields.String(description='UrlFileAddress', required=True),
    'FullNameContact': fields.String(description='FullNameContact', required=True),
    'Phone': fields.String(description='Phone', required=True),



    'Floor': fields.String(description='Floor', required=True),
    'Square': fields.Float(description='Square', required=True),
    'Lift': fields.Boolean(description='Lift', required=True),
    'LiftLight': fields.Boolean(description='LiftLight', required=True),
    'LiftNot': fields.Boolean(description='LiftNot', required=True, default=True),

    'MinCeilingHeight': fields.String(description='MinCeilingHeight', required=True),
    'MaxCeilingHeight': fields.String(description='MaxCeilingHeight', required=True),
    'NeighborsId': fields.String(description='NeighborsId', required=True),
    'MyAnimal': fields.String(description='MyAnimal', required=True),
    'PowerElectric': fields.Float(description='PowerElectric', required=True),
    'NeighborsId': fields.String(description='NeighborsId', required=True),
    'Neighbors': fields.String(description='Neighbors', required=True),
    'Animal': fields.String(description='Animal', required=True),
    

    'ParkingDistanceId': fields.String(description='ParkingDistanceId', required=True),
    'ParkingDistance': fields.String(description='ParkingDistance', required=True),
    'ParkingDistanceMore': fields.String(description='ParkingDistanceMore', required=True),
    'ParkingPass': fields.Boolean(description='ParkingPass', required=True),
    'ParkingSize10': fields.Boolean(description='ParkingSize10', required=True),
    'ParkingTracks': fields.Boolean(description='ParkingTracks', required=True),
    'ParkingNot': fields.Boolean(description='ParkingNot', required=True, default=True),

    
    # 'Description': fields.String(description='UF_CRM_9_1675171164797', required=True),
    'url': fields.List(fields.String(required=False, description='')),
})

#TODO
#update_type_model = api.model('Update type', {


@api.route('/deal')
class Deal(Resource):
    @api.expect(create_deal_model,description='sad')
    @api.doc(description='Создает сделку', default_label='Запросы',title='tst')
    def post(self) -> str:
        """
        Создает сделку
        """
        data = request.get_json() 
        logger.debug(f'{data=}')
        dealID = create_deal(data)['result']
        row = {'id': dealID,'entity_type':'deal'}
        sql.replace_query('entity',row) 
        return f'{dealID}'
    
    @api.expect(update_deal_model) 
    @api.doc(description='Обновляет сделку')
    def put(self):
        """
        Обновляет сделку
        """
        data = request.get_json() 
        logger.debug(f'{data=}')
        dealID = data['id']
        dealID = update_deal(dealID=dealID, fields=data)
         
        return f'{dealID}'

@api.route('/type')
@api.doc(description='Создает смарт-процесс')
class Type(Resource):
    @api.expect(create_type_model)
    def post(self):
        """
        Создает смарт-процесс
        """
        data = request.get_json() 
        logger.debug(f'{data=}')
        pprint(data)
        typeID = create_item_for_type(data)['result']['item']['id']
        # dealID = create_type(data) 
        row = {'id': typeID,'entity_type':'item'}
        sql.replace_query('entity',row)
        return f'{typeID}'


# Запуск приложения
if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port='5005')
    # 0000 позволяет получать запросы не только по localhostсв