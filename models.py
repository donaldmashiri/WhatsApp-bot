from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_marshmallow import Marshmallow
from marshmallow import fields
from sqlalchemy.orm import backref
import datetime

#initialize DB and Marshmallow
db = SQLAlchemy()
ma = Marshmallow()


#from .models import User
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    role = db.Column(db.Integer)

    def __init__(self, email, password, name, role):
        self.email=email
        self.password=password
        self.name=name
        self.role=role


# table Model Class
class Bot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    fname = db.Column(db.String(80))
    lname = db.Column(db.String(80))
    accnum = db.Column(db.String(80))
    phone = db.Column(db.String(20))
    menu = db.Column(db.String(80))
    balance = db.Column(db.Numeric(precision=10, scale=2))
    pin = db.Column(db.Integer)
    newpin = db.Column(db.Integer, nullable=True)

    def __init__(self, name, fname, lname, accnum, phone, menu, balance, pin, newpin):
        self.name=name
        self.fname=fname
        self.lname=lname
        self.accnum=accnum
        self.phone=phone
        self.menu=menu
        self.balance=balance
        self.pin=pin
        self.newpin=newpin


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    botid = db.Column(db.Integer)
    balance = db.Column(db.Numeric(precision=10, scale=2))

    def __init__(self, botid, balance):
        self.botid=botid
        self.balance=balance


class LoanCache(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    botid = db.Column(db.Integer)
    option = db.Column(db.Integer, nullable=True)
    amount = db.Column(db.Numeric(precision=10, scale=2), nullable=True)

    def __init__(self, botid, option, amount):
        self.botid=botid
        self.option=option
        self.amount=amount


class RepayCache(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    botid = db.Column(db.Integer)
    phone = db.Column(db.String(20), nullable=True)
    amount = db.Column(db.Numeric(precision=10, scale=2), nullable=True)

    def __init__(self, botid, phone, amount):
        self.botid=botid
        self.phone=phone
        self.amount=amount


class FeesCache(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    botid = db.Column(db.Integer)
    schoolid = db.Column(db.String(20), nullable=True)
    amount = db.Column(db.Numeric(precision=10, scale=2), nullable=True)

    def __init__(self, botid, schoolid, amount):
        self.botid=botid
        self.schoolid=schoolid
        self.amount=amount

class ZesaToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    botid = db.Column(db.Integer)
    watts = db.Column(db.Integer)
    token = db.Column(db.String(20), nullable=True)
    amount = db.Column(db.Numeric(precision=10, scale=2), nullable=True)

    def __init__(self, botid, watts, token, amount):
        self.botid=botid
        self.watts=watts
        self.token=token
        self.amount=amount


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    botid = db.Column(db.Integer)
    action = db.Column(db.String(80))
    method = db.Column(db.String(80))
    amount = db.Column(db.Numeric(precision=10, scale=2))
    accdebited = db.Column(db.String(80))
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now())

    def __init__(self, botid, action, method, amount, accdebited, created_at):
        self.botid=botid
        self.action=action
        self.method=method
        self.amount=amount
        self.accdebited=accdebited
        self.created_at=created_at


class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    fees = db.Column(db.Numeric(precision=10, scale=2))

    def __init__(self, name, fees):
        self.name=name
        self.fees=fees


class Zesa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kilowatts = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Numeric(precision=10, scale=2))

    def __init__(self, kilowatts, price):
        self.kilowatts=kilowatts
        self.price=price



#User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'password', 'role')


#initilize schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)

#Bot Schema
class BotSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'phone', 'menu', 'balance', 'pin')

#Bot schema
bot_schema = BotSchema()
bots_schema = BotSchema(many=True)

#loan Schema
class LoanSchema(ma.Schema):
    class Meta:
        fields = ('id', 'botid', 'balance')

#initilize schema
loan_schema = LoanSchema()
loans_schema = LoanSchema(many=True)

#transaction Schema
class TransactionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'botid', 'action', 'method', 'amount', 'accdebited' 'created_at')

#initialize transaction schema
transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)


#school Schema
class SchoolSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'fees')

#initialize school schema
school_schema = SchoolSchema()
schools_schema = SchoolSchema(many=True)

#zesa Schema
class ZesaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'kilowatts', 'amount')

#initialize zesa schema
zesa_schema = ZesaSchema()
zesas_schema = ZesaSchema(many=True)