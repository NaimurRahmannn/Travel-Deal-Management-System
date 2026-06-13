from flask import Blueprint, jsonify, request
from services.deals_service import (
    create_deal,
    get_all_deal,
    get_deal_by_id,
    search_deals,
    filter_deals_by_budget,
    sort_deals,
    get_recent_deals,
    track_recent,
)
from utils.logger import logger
from utils.validators import validate_price_range, validate_sort_params

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
    track_recent(deal)
    logger.info(f"Deal {deal_id} viewed")
    return jsonify(deal.to_dic()), 200


@deals_bp.route("/search", methods=["GET"])
def search():
    destination = request.args.get("destination")
    platform = request.args.get("platform")
    travel_type = request.args.get("travel_type")
    if not any([destination, platform, travel_type]):
        return (
            jsonify(
                {
                    "error": "Provide at least one search parameter "
                    "(destination, platform, or travel_type)"
                }
            ),
            400,
        )

    logger.info(
        f"Search request: destination={destination},"
        f"platform={platform}, travel_type={travel_type}"
    )
    deals = search_deals(destination, platform, travel_type)
    logger.info(f"Search successful: {len(deals)} deal(s) found")
    results = []
    for d in deals:
        results.append(d.to_dic())

    return jsonify({"count": len(deals), "results": results}), 200


@deals_bp.route("/filter", methods=["GET"])
def filter_deals():
    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)

    error = validate_price_range(min_price, max_price)
    if error:
        logger.warning(f"Invalid filter request: {error}")
        return jsonify({"error": error}), 400

    logger.info(f"Filter request: min_price={min_price}, max_price={max_price}")
    deals = filter_deals_by_budget(min_price, max_price)
    logger.info(f"Filter successful: {len(deals)} deal(s) found")
    return jsonify({"count": len(deals), "results": [d.to_dic() for d in deals]}), 200


@deals_bp.route("/sort", methods=["GET"])
def sort():
    sort_by = request.args.get("sort_by", "price")
    order = request.args.get("order", "asc")

    error = validate_sort_params(sort_by, order)
    if error:
        logger.warning(f"Invalid sort request: {error}")
        return jsonify({"error": error}), 400

    logger.info(f"Sort request: sort_by={sort_by}, order={order}")
    deals = sort_deals(sort_by, order)
    results = []
    for d in deals:
        results.append(d.to_dic())

    return jsonify({"count": len(deals), "results": results}), 200


@deals_bp.route("/recent", methods=["GET"])
def recent():
    logger.info("Recent deals requested")
    deals = get_recent_deals()
    return jsonify({"count": len(deals), "results": deals}), 200
