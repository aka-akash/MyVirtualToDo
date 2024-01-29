#doing changes for git


from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = "you-will-never-guess"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Default.db"
app.config['SQLALCHEMY_BINDS'] = {
    'first': "sqlite:///ToDo_Database.db",
    'second': "sqlite:///ToDo_Login.db"
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Database(db.Model):
    __bind_key__ = 'first'
    sno = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    dateCreation = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.name} {self.description} {self.dateCreation}"


class Records(db.Model):
    __bind_key__ = 'second'
    sno = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    userId = db.Column(db.String(30), nullable=False)
    pwd = db.Column(db.String(30), nullable=False)

    def __repr__(self) -> str:
        return f"{self.sno} {self.fname} {self.lname} {self.userId} {self.pwd}"


@app.route('/ToDoLogin')
def ToDoLogin():
    return render_template("ToDo_Login.html")


@app.route('/Login_Records', methods=['POST'])
def Login_Records():
    uid = request.form['userId']
    paswrd = request.form['pwd']
    user = Records.query.filter_by(userId=uid).first()
    if(user == None):
        flash("Incorrect Credentials.")
        return redirect(url_for('ToDoLogin'))
    else:
        if(user.pwd == paswrd):
            session['user'] = uid
            session['uname'] = user.fname + ' ' + user.lname
            return redirect(url_for('ShowListToDo'))
        else:
            flash("Incorrect Credentials.")
            return redirect(url_for('ToDoLogin'))


@app.route('/ToDoSignUp')
def ToDoSignUp():
    return render_template('ToDo_SignUp.html')


@app.route('/SignUp_Records', methods=['POST'])
def SignUp_Records():
    fnam = request.form['fname']
    lnam = request.form['lname']
    uid = request.form['userId']
    paswrd = request.form['pwd']
    cnfpwd = request.form['cnfpwd']
    user = Records.query.filter_by(userId=uid).first()
    if(user == None):
        if(paswrd == cnfpwd):
            log = Records(fname=fnam, lname=lnam, userId=uid, pwd=paswrd)
            db.session.add(log)
            db.session.commit()
            return redirect(url_for('ToDoLogin'))
        else:
            flash("PassWord And Confirm PassWord Didn't Matched.")
            return redirect(url_for('ToDoSignUp'))
    else:
        flash("UserID Registered.")
        return redirect(url_for('ToDoSignUp'))


# @app.route('/ToDoList')
# def ToDoList():
#     uname = session['uname']
#     return render_template('ToDo_List.html', Name=uname)


@app.route('/ListToDo', methods=['POST'])
def ListToDo():
    user = session['user']
    nam = request.form['name']
    des = request.form['description']
    log = Database(userId=user, name=nam, description=des)
    db.session.add(log)
    db.session.commit()
    return redirect(url_for('ShowListToDo'))


@app.route('/ShowListToDo')
def ShowListToDo():
    uname = session['uname']
    user = session['user']
    alltodo = Database.query.filter_by(userId=user).all()
    return render_template('ToDo_List.html', Name=uname, alltodo=alltodo)


@app.route('/DeleteToDo/<string:na>')
def DeleteToDo(na):
    user = session['user']
    dele = Database.query.filter_by(name=na, userId=user).first()
    db.session.delete(dele)
    db.session.commit()
    return redirect(url_for('ShowListToDo'))


@app.route('/ToDoLogout')
def ToDoLogout():
    session.pop('user', None)
    session.pop('uname', None)
    return redirect(url_for('ToDoLogin'))


if (__name__ == "__main__"):
    app.run(debug=True)
