from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:11111111@localhost:3306/gpt_doc'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class DocsChunks(db.Model):
    __tablename__ = 'docs_chunks'
    id = db.Column(db.Integer, primary_key=True)
    docs_id = db.Column(db.Integer)
    vector_id = db.Column(db.String(80))
    page_content = db.Column(db.Text)
    page_number = db.Column(db.Integer)
    lines_from = db.Column(db.Integer)
    lines_to = db.Column(db.Integer)
    remark = db.Column(db.String(120))
    active = db.Column(db.Boolean)
    created_time = db.Column(db.DateTime)
    updated_time = db.Column(db.DateTime)
    created_by = db.Column(db.String(80))
    updated_by = db.Column(db.String(80))

    def __init__(self, docs_id, vector_id, page_content, page_number, lines_from, lines_to, remark, active, created_time, updated_time, created_by, updated_by):
        self.docs_id = docs_id
        self.vector_id = vector_id
        self.page_content = page_content
        self.page_number = page_number
        self.lines_from = lines_from
        self.lines_to = lines_to
        self.remark = remark
        self.active = active
        self.created_time = created_time
        self.updated_time = updated_time
        self.created_by = created_by
        self.updated_by = updated_by

    def __repr__(self):
        return '<DocsChunks %r>' % self.id

    def to_json(self):
        return {
            'id': self.id,
            'doc_id': self.docs_id,
            'vector_id': self.vector_id,
            'page_content': self.page_content,
            'page_number': self.page_number,
            'lines_from': self.lines_from,
            'lines_to': self.lines_to,
            'remark': self.remark,
            'active': self.active,
            'created_time': self.created_time,
            'updated_time': self.updated_time,
            'created_by': self.created_by,
            'updated_by': self.updated_by
        }

class Docs(db.Model):
    __tablename__ = 'docs'
    id = db.Column(db.Integer, primary_key=True)
    docs_name = db.Column(db.String(80))
    docs_path = db.Column(db.String(120))
    total_page = db.Column(db.Integer)
    remark = db.Column(db.String(120))
    active = db.Column(db.Boolean)
    created_time = db.Column(db.DateTime)
    updated_time = db.Column(db.DateTime)
    created_by = db.Column(db.String(80))
    updated_by = db.Column(db.String(80))

    def __init__(self, docs_name, docs_path, total_page, remark, active, created_time, updated_time, created_by,
                 updated_by):
        self.docs_name = docs_name
        self.docs_path = docs_path
        self.total_page = total_page
        self.remark = remark
        self.active = active
        self.created_time = created_time
        self.updated_time = updated_time
        self.created_by = created_by
        self.updated_by = updated_by

    def to_json(self):
        return {
            'id': self.id,
            'docs_name': self.docs_name,
            'docs_path': self.docs_path,
            'total_page': self.total_page,
            'remark': self.remark,
            'active': self.active,
            'created_time': str(self.created_time),
            'updated_time': str(self.updated_time),
            'created_by': self.created_by,
            'updated_by': self.updated_by
        }

    def __repr__(self):
        return '<Docs %r>' % self.docs_name


@app.route('/add/doc', methods=['POST'])
def add_doc():
    docs_name = request.json.get('docs_name')
    docs_path = request.json.get('docs_path')
    total_page = request.json.get('total_page')
    remark = request.json.get('remark')
    active = request.json.get('active')
    created_time = request.json.get('created_time')
    updated_time = request.json.get('updated_time')
    created_by = request.json.get('created_by')
    updated_by = request.json.get('updated_by')

    temp = Docs(docs_name, docs_path, total_page, remark, active, created_time, updated_time, created_by, updated_by)
    db.session.add(temp)
    db.session.commit()

    return 'success'

@app.route('/add/chunk', methods=['POST'])
def add_chunk():
    docs_id = request.json.get('docs_id')
    vector_id = request.json.get('vector_id')
    page_content = request.json.get('page_content')
    page_number = request.json.get('page_number')
    lines_from = request.json.get('lines_from')
    lines_to = request.json.get('lines_to')
    remark = request.json.get('remark')
    active = request.json.get('active')
    created_time = request.json.get('created_time')
    updated_time = request.json.get('updated_time')
    created_by = request.json.get('created_by')
    updated_by = request.json.get('updated_by')

    temp = DocsChunks(docs_id, vector_id, page_content, page_number, lines_from, lines_to, remark, active, created_time, updated_time, created_by, updated_by)
    db.session.add(temp)
    db.session.commit()

    return 'success'


@app.route('/getAll')
def get_all():
    doc = Docs.query.all()
    doc = list(map(lambda x: x.to_json(), doc))

    return doc

@app.route('/getAll/chunk')
def get_all_chunk():
    doc = DocsChunks.query.all()
    doc = list(map(lambda x: x.to_json(), doc))

    return doc

@app.route('/add/chunk/one')
def add_chunk_one():
    newChunk = DocsChunks(1, "1", 'page_content', 1, 1, 1, 'remark', True, "2023-01-01", "2023-01-01", 'created_by', 'updated_by')
    db.session.add(newChunk)
    db.session.commit()

    return 'success'


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
