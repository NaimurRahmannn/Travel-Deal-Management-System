from flask import Blueprint, jsonify, request
from services.deals_service import (
    create_deal,
    get_all_deal,
    get_deal_by_id,
    search_deals,
)
from utils.logger import logger

deals_bp = Blueprint("deals", __name__)


@deals_bp.route("/", methods=["POST"])
def add_deals():
    data = request.get_json(silent=True)
    if data is None:
        return (
            jsonify(
                {
                    "error": "Request body must be valid JSON with Content-Type: application/json"
                }
            ),
            400,
        )
    deal, error = create_deal(data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(deal.to_dic()), 201


@deals_bp.route("/", methods=["GET"])
def list_deals():
    deals = get_all_deal()
    return jsonify([d.to_dic() for d in deals]), 200


@deals_bp.route("/<deal_id>", methods=["GET"])
def single_deal(deal_id):
    if not deal_id.isdigit():
        return jsonify({"error": "deal_id must be an integer"}), 400
    deal = get_deal_by_id(int(deal_id))
    if not deal:
        return jsonify({"error": "Deal not found"}), 404
    return jsonify(deal.to_dic()), 200


@deals_bp.route("/search", methods=["GET"])
def search():
    destination = request.args.get("destination")

    if not destination:
        logger.warning("Search called with no destination")
        return jsonify({"error": "Provide a destination to search"}), 400

    logger.info(f"Search request: destination={destination}")
    deals = search_deals(destination)
    logger.info(f"Search successful: {len(deals)} deal(s) found")
    results = []
    for d in deals:
        results.append(d.to_dic())

    return jsonify({
        "count": len(deals),
        "results": results
    }), 200
