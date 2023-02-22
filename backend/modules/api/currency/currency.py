from flask import Blueprint, jsonify
from modules.models.CurrencyList import CurrencyList;
from mongoengine.errors import FieldDoesNotExist, InvalidQueryError

currency = Blueprint('currency', __name__)

@currency.route("/list", methods=["GET"])
def getCurrencyList():

    try:

        return jsonify({"currency list":CurrencyList.objects.all().values_list('name')})

    except (FieldDoesNotExist, InvalidQueryError):
        return jsonify({"error": "Could not get the currency list"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500