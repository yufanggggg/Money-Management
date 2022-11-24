from flask_restful import Resource, Api

#Restful API
api=Api(app)
class TEST(Resource):
    def get(self):
        return {'message':'hello world'}
api.add_resource(TEST, '/test')