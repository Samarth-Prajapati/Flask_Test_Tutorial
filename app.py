from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///flask_1.db'
db=SQLAlchemy(app)

class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(50),nullable=False)
    description=db.Column(db.String(100),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.id} - {self.title}"
    
    # def __str__(self) -> str:
    #     return f"{self.id} - {self.title}"

@app.route('/',methods=['GET','POST'])
def home():
    # return 'Hello World!!'
    # todo=Todo(title='Python',description='Learn Basics')
    # db.session.add(todo)
    # db.session.commit()
    if request.method=='POST':
        if not request.form['title'] or not request.form['description']:
            return redirect('/')
        else:
            title=request.form['title']
            description=request.form['description']
            todo=Todo(title=title,description=description)
            db.session.add(todo)
            db.session.commit()
    todo=Todo.query.all()
    return render_template('index.html',todo=todo)


# @app.route('/show')
# def show():
#     # todo=Todo.query.all()
#     # print(todo)
#     return 'About Page'

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    if request.method=='POST':
        title=request.form['title']
        description=request.form['description']
        todo=Todo.query.filter_by(id=id).first()
        todo.title=title
        todo.description=description    
        # db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo=Todo.query.filter_by(id=id).first()
    return render_template('update.html',todo=todo)

@app.route('/delete/<int:id>')
def delete(id):
    todo=Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

if __name__=='__main__':
    app.run(debug=True, port=8080)   # port=8080 is the custom port number



