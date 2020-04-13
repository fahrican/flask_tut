from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
# app is needed for routes
# Api works with resources and every resource needs to be a class
api = Api(app)

items = []


class Student(Resource):

    def get(self, name):
        return {'student': name}


api.add_resource(Student, '/item/<string:name>')  # http://127.0.0.1:5000/student/Fahri

app.run(port=5000)
