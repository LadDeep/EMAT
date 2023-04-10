from flask import Blueprint, jsonify
from modules.models.CurrencyList import CurrencyList
from mongoengine.errors import FieldDoesNotExist, InvalidQueryError

currency = Blueprint('currency', __name__)

@currency.route("/list", methods=["GET"])
def get_currency_list():
    """
    gets the currency list from the Database
    
    Returns:
        A python dictionary containing  status & a currency list key-value pair on a successful response
    """
    try:

        return jsonify({"status": True, "currency list":CurrencyList.objects.all().values_list('name')}), 200

    except (FieldDoesNotExist, InvalidQueryError):
        return jsonify({"status": False, "error": "Could not get the currency list"}), 400
    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500
    

@currency.route("/details", methods=["GET"])
def get_currency():
    """
    gets the currency list from the Database along with name, symbol & code fields only
    
    Returns:
        A python dictionary containing status & a message key-value pair on a successful response
    """
    try:

        details = CurrencyList.objects.fields(name=1, symbol=1, code=1)
        
        return jsonify({"status": True, "message": list(details)}), 200

    except (FieldDoesNotExist, InvalidQueryError):
        return jsonify({"status": False, "error": "Could not get the currency details"}), 400
    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500