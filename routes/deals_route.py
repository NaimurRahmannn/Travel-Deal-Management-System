from flask import Blueprint
from flask import jsonify

deals_bp = Blueprint("deals", __name__)


@deals_bp.route("/", methods=["POST"])
def add_deals():
    return {"msg": "Add deals"}


@deals_bp.route("/", methods=["GET"])
def list_deals():
    return {"msg": "Get all deals"}


@deals_bp.route("/<int:deal_id>", methods=["GET"])
def single_deals(deal_id):
    return {"msg": "Get single deals"}
