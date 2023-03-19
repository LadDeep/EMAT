from flask import Blueprint, jsonify
from modules.models.CurrencyList import CurrencyList;
from mongoengine.errors import FieldDoesNotExist, InvalidQueryError

currency = Blueprint('currency', __name__)

@currency.route("/list", methods=["GET"])
def getCurrencyList():

    try:

        return jsonify({"status": True, "currency list":CurrencyList.objects.all().values_list('name')}), 200

    except (FieldDoesNotExist, InvalidQueryError):
        return jsonify({"status": False, "error": "Could not get the currency list"}), 400
    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500
    

@currency.route("/details", methods=["GET"])
def getCurrency():

    try:

        details = CurrencyList.objects().values("name", "symbol", "code")
        
        return jsonify({"status": True, "message": list(details)}), 200

    except (FieldDoesNotExist, InvalidQueryError):
        return jsonify({"status": False, "error": "Could not get the currency details"}), 400
    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500