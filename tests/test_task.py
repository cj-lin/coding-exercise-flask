from flask import url_for

from myapi.extensions import pwd_context
from myapi.models import Task


def test_get_task(client, db, task, admin_headers):
    # test 404
    task_url = url_for('api.task_by_id', task_id="100000")
    rep = client.get(task_url, headers=admin_headers)
    assert rep.status_code == 404

    db.session.add(task)
    db.session.commit()

    # test get_task
    task_url = url_for('api.task_by_id', task_id=task.id)
    rep = client.get(task_url, headers=admin_headers)
    assert rep.status_code == 200

    data = rep.get_json()["task"]
    assert data["name"] == task.name
    assert data["status"] == task.status


def test_put_task(client, db, task, admin_headers):
    # test 404
    task_url = url_for('api.task_by_id', task_id="100000")
    rep = client.put(task_url, headers=admin_headers)
    assert rep.status_code == 404

    db.session.add(task)
    db.session.commit()

    data = {"name": "買早餐", "status": 1}

    task_url = url_for('api.task_by_id', task_id=task.id)
    # test update task
    rep = client.put(task_url, json=data, headers=admin_headers)
    assert rep.status_code == 200

    data = rep.get_json()["task"]
    assert data["name"] == "買早餐"
    assert data["status"] == 1


def test_delete_task(client, db, task, admin_headers):
    # test 404
    task_url = url_for('api.task_by_id', task_id="100000")
    rep = client.delete(task_url, headers=admin_headers)
    assert rep.status_code == 404

    db.session.add(task)
    db.session.commit()

    # test get_task

    task_url = url_for('api.task_by_id', task_id=task.id)
    rep = client.delete(task_url,  headers=admin_headers)
    assert rep.status_code == 200
    assert db.session.query(Task).filter_by(id=task.id).first() is None


def test_create_task(client, db, admin_headers):
    # test bad data
    tasks_url = url_for('api.tasks')
    data = {"taskname": "created"}
    rep = client.post(tasks_url, json=data, headers=admin_headers)
    assert rep.status_code == 400

    data["name"] = "買晚餐"

    rep = client.post(tasks_url, json=data, headers=admin_headers)
    assert rep.status_code == 201

    data = rep.get_json()
    task = db.session.query(Task).filter_by(id=data["task"]["id"]).first()

    assert task.name == "買晚餐"
    assert task.status == 0


def test_get_all_task(client, db, task_factory, admin_headers):
    tasks_url = url_for('api.tasks')
    tasks = task_factory.create_batch(30)

    db.session.add_all(tasks)
    db.session.commit()

    rep = client.get(tasks_url, headers=admin_headers)
    assert rep.status_code == 200

    results = rep.get_json()
    for task in tasks:
        assert any(u["id"] == task.id for u in results["results"])
