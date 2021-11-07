from flask import Flask, render_template, request, url_for, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://admin:<password>@cluster0.2dfke.mongodb.net/mydb?retryWrites=true&w=majority'
mongo = PyMongo(app)

todos = mongo.db.todos

@app.route('/')
def index():
    saved_todos = todos.find()
    return render_template('index.html', todos=saved_todos)

@app.route('/update/<oid>')
def update(oid):
    saved_todos = todos.find()
    edit_todo=todos.find_one({'_id': ObjectId(oid)})
    return render_template('index.html', edit_todo=edit_todo, todos=saved_todos)

@app.route('/add', methods=['POST'])
def add_todo():
    new_todo = request.form.get('new-todo')
    todos.insert_one({'text' : new_todo, 'complete' : False})
    return redirect(url_for('index'))

@app.route('/complete/<oid>')
def complete(oid):
    todo_item = todos.find_one({'_id': ObjectId(oid)})
    todo_item['complete'] = True
    todos.save(todo_item)
    return redirect(url_for('index'))

@app.route('/update',methods=['POST'])
def update_todo():
    oid=request.form.get('oid')
    edit = request.form.get('edit')
    todo_item = todos.find_one({'_id': ObjectId(oid)})
    todo_item['text'] = edit
    todos.save(todo_item)
    return redirect(url_for('index'))

@app.route('/delete/<oid>')
def delete(oid):
    todos.delete_one({'_id': ObjectId(oid)})
    return redirect(url_for('index'))

@app.route('/delete_completed')
def delete_completed():
    todos.delete_many({'complete' : True})
    return redirect(url_for('index'))

@app.route('/delete_all')
def delete_all():
    todos.delete_many({})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
   
