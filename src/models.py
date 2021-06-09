from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Float

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), unique=False, nullable=False)
    payments = db.relationship('Payment', backref='user', lazy=True)
    invoices = db.relationship('Invoice', backref='user', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name
        }

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String, db.ForeignKey('user.email'), nullable=False)
    amount = db.Column(db.Float(8), unique=False, nullable=False)
    receipt_name = db.Column(db.String(120), unique=False, nullable=False)
    subject = db.Column(db.String(120), unique=False, nullable=False)
    payment_file = db.Column(db.String(120), unique=False, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "receipt_name": self.receipt_name,
            "subject": self.subject,
            "payment_file": self.payment_file,
            "email": self.email.serialize()
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String, db.ForeignKey('user.email'), nullable=False)
    files = db.Column(db.String(120), unique=False, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "files": self.files,
            "email": self.email.serialize()
        }

    def save(self):
        db.session.add(self)
        db.session.commit()