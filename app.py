from flask import Flask, request
from flask_restful import Resource, Api
from faccialibro_gcloud import FaccialibroGcloud

app = Flask(__name__,
            static_url_path='/static',
            static_folder='static')
faccialibro_dao = FaccialibroGcloud()

api = Api(app)
basePath = '/api/v1'


class FacciaLibroChirps(Resource):
    def post(self):
        message = request.json
        if 1 <= len(message) <= 100:
            h = faccialibro_dao.add_chirps(message)
            return h, 400
        else:
            return None, 400

    def get(self, ids):
        h = faccialibro_dao.get_chirps(ids)
        if h is not None:
            return h, 200
        else:
            return None, 404


class FacciaLibroTopics(Resource):
    def get(self, topic):
        h = faccialibro_dao.get_topics(topic)
        if h is not None:
            return h, 200
        else:
            return None, 404


class FacciaLibroClean(Resource):
    def post(self):
        faccialibro_dao.clean()
        return None, 200


api.add_resource(FacciaLibroChirps, f'{basePath}/chirp')
api.add_resource(FacciaLibroTopics, f'{basePath}/topic/<string:data>')
api.add_resource(FacciaLibroClean, f'{basePath}/clean')


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
