from flask import Flask, request, render_template
from loguru import logger
from flask_restx import Api, Resource, fields
from dotenv import load_dotenv
from babyshki import *

load_dotenv()

app = Flask(__name__)
api = Api(app, version='1.0', title='Итнеграция с битриксом', description="Bitrix API", default_label='Запросы')





create_deal_model = api.model('Create deal', {
    'nameProject': fields.String(description='nameProject', required=True),
    'description': fields.String(description='description', required=True),
    'img': fields.Url(description='imgUrl', required=True),
    'document': fields.Url(description='documentUrl', required=True),
    'bandSize': fields.String(description='bandSize', required=True),
    'hours': fields.String(description='hours', required=True),
    'date': fields.String(description='date', required=True),
    'budget': fields.String(description='budget', required=True),
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
    'budget': fields.String(description='budget', required=True),
})

create_type_model = api.model('Create type', {
    'name': fields.String(description='name', required=True),
    'id': fields.String(description='id', required=True),
    'url': fields.Url(description='url', required=True),
})


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
        dealID = create_deal(data) 
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
        dealID = create_type(data) 
        return f'{dealID}'


# Запуск приложения
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5002')
    # 0000 позволяет получать запросы не только по localhost