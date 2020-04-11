import config
from datetime import datetime
from flask import Flask, url_for, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)


class Todo(db.Model):
    __tablename__ = 'Todo list'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(101), unique=True)
    content = db.Column(db.String(255), unique=True)
    # creat_time = db.Column(db.DateTime, default=datetime.now, index=True)
    status = db.Column(db.Boolean)

    def __init__(self, title, content, status):
        self.title = title
        self.content = content
        self.status = status

    def get_title(self):
        return self.title

    def __repr__(self):
        return "<Todo %r>" % self.title


@app.before_first_request
def create_db():
    db.drop_all()
    db.create_all()

    tasks = [Todo('sleep', 'just sleep', False),
            Todo('learing', 'just learning', False),
            Todo('flask', 'more flask', False)]
    db.session.add_all(tasks)
    db.session.commit()


@app.route('/')
def index():
    return 'Hello World!'


def replace_id_to_uri(task):
    return dict(uri=url_for('get_task', task_id=task.id, _external=True),
                title=task.title,
                content=task.content,
                status=task.status)


@app.route('/todo/api/tasks/', methods=['GET'])
def get_tasks():
    tasks = Todo.query.all()
    return jsonify({'tasks': list(map(replace_id_to_uri, tasks))})


@app.route('/todo/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Todo.query.filter_by(id=task_id).first()
    if task is None:
        abort(404)

    return jsonify({'task': replace_id_to_uri(task)})


# 添加
@app.route('/todo/api/tasks/', methods=['POST'])
def create_task():
    # 没有数据，或者数据缺少 title 项，返回 400，表示请求无效
    if not request.json or not 'title' in request.json:
        abort(400)

    task = Todo(request.json['title'], request.json.get('content', ""), False)

    db.session.add(task)
    db.session.commit()
    return jsonify({'task': replace_id_to_uri(task)}), 201


# 更新
@app.route('/todo/api/tasks/<string:task_title>', methods=['PUT'])
def update_task(task_title):
    task = Todo.query.filter_by(title=task_title).first()
    if task is None:
        abort(404)

    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'content' in request.json and type(request.json['content']) is not unicode:
        abort(400)
    if 'status' in request.json and type(request.json['status']) is not bool:
        abort(400)

    task['title'] = request.json.get('title', task['title'])
    task['content'] = request.json.get('content', task['content'])
    task['status'] = request.json.get('status', task['status'])

    db.session.update(task)
    db.session.commit()
    return jsonify({'task': replace_id_to_uri(task)})


# 删除
@app.route('/todo/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Todo.query.filter_by(id=task_id).first()
    if task is None:
        abort(404)

    db.session.delete(task)
    db.session.commit()
    return jsonify({'result': True})


# 定制404出错页面
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
