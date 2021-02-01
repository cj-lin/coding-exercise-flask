from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from myapi.api.schemas import TaskSchema
from myapi.models import Task
from myapi.extensions import db
from myapi.commons.pagination import paginate


class TaskResource(Resource):

    method_decorators = [jwt_required]

    def get(self, task_id):
        schema = TaskSchema()
        task = Task.query.get_or_404(task_id)
        return {"task": schema.dump(task)}

    def put(self, task_id):
        schema = TaskSchema(partial=True)
        task = Task.query.get_or_404(task_id)
        task = schema.load(request.json, instance=task)

        db.session.commit()

        return {"msg": "task updated", "task": schema.dump(task)}

    def delete(self, task_id):
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()

        return {"msg": "task deleted"}


class TaskList(Resource):

    method_decorators = [jwt_required]

    def get(self):
        schema = TaskSchema(many=True)
        query = Task.query
        return paginate(query, schema)

    def post(self):
        schema = TaskSchema()
        task = schema.load(request.json)

        db.session.add(task)
        db.session.commit()

        return {"msg": "task created", "task": schema.dump(task)}, 201
