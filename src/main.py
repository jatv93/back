"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Payment, Invoice
#from models import Person

BASEDIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASEDIR, "test.db")
app.config["DEBUG"] =True
app.config["ENV"] = "development"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
@app.route('/user/<int:id>', methods=['GET'])
def users(id = None):

    if request.method == 'GET':
        if id is not None:
            user = User.query.get(id) 
            if user:
                return jsonify(user.serialize()), 200
            return jsonify({"msg": "User not found"}), 404
        else:
            user = User.query.all()
            user = list(map(lambda user: user.serialize(), user))
            return jsonify(user), 200


@app.route('/payment', methods=['GET'])
@app.route('/payment/<int:id>', methods=['GET', 'POST'])
def payments(id = None):

    if request.method == 'GET':
        if id is not None:
            payment = Payment.query.get(id) 
            if payment:
                return jsonify(payment.serialize()), 200
            return jsonify({"msg": "Payment not found"}), 404
        else:
            payment = Payment.query.all()
            payment = list(map(lambda payment: payment.serialize(), payment))
            return jsonify(payment), 200

    if request.method == 'POST':

        amount = request.json.get("amount", None)
        receipt_name = request.json.get("receipt_name", None)
        subject = request.json.get("subject", None)
        payment_file = request.json.get("payment_file", None)

        if not amount:
            return jsonify({"msg": "Amount is required"}), 400
        if not receipt_name:
            return jsonify({"msg": "Name is required"}), 400
        if not subject:
            return jsonify({"msg": "Subject is required"}), 400
        if not payment_file:
            return jsonify({"msg": "Payment File is required"}), 400
        
        payment = Payment()
        payment.amount = amount
        payment.receipt_name = receipt_name
        payment.subject = subject
        payment.payment_file = payment_file

        payment.save()

        return jsonify({"success": "Payment Register Successfully"}), 200

@app.route('/invoice', methods=['GET'])
@app.route('/invoice/<int:id>', methods=['GET', 'POST'])
def invoices(id = None):

    if request.method == 'GET':
        if id is not None:
            invoice = Invoice.query.get(id) 
            if invoice:
                return jsonify(invoice.serialize()), 200
            return jsonify({"msg": "Invoice not found"}), 404
        else:
            invoice = Invoice.query.all()
            invoice = list(map(lambda invoice: invoice.serialize(), invoice))
            return jsonify(invoice), 200

    if request.method == 'POST':

        files = request.json.get("files", None)

        if not files:
            return jsonify({"msg": "File is required"}), 400
        
        invoice = Invoice()
        invoice.files = files

        invoice.save()

        return jsonify({"success": "Invoice Register Successfully"}), 200

@app.route("/download/<int:id>", methods=['GET'])
def download_blob(id):
    _image = Image.query.get_or_404(id)
    return send_file(
        io.BytesIO(_image.blob),
        attachment_filename=_image.filename,
        mimetype=_image.mimetype
    )


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
