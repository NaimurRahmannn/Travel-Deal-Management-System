from sqlalchemy.exc import SQLAlchemyError

from database.model import db, TravelManagement
from utils.validators import validate_deal
from sqlalchemy import asc, desc


def create_deal(data):
    error = validate_deal(data)
    if error:
        return None, error
    deal = TravelManagement(
        destination=data["destination"],
        price=data["price"],
        platform=data["platform"],
        rating=data.get("rating"),
        travel_type=data["travel_type"],
    )
    try:
        db.session.add(deal)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return None, "Could not save the deal, please try again"
    return deal, None


def get_all_deal():
    return TravelManagement.query.all()


def get_deal_by_id(deals_id):
    return TravelManagement.query.get(deals_id)

#shared filtering helper
def apply_filters(
    query,
    destination=None,
    platform=None,
    travel_type=None,
    min_price=None,
    max_price=None,
):
    if destination:
        query = query.filter(TravelManagement.destination.ilike(f"%{destination}%"))
    if platform:
        query = query.filter(TravelManagement.platform.ilike(f"%{platform}%"))
    if travel_type:
        query = query.filter(TravelManagement.travel_type.ilike(f"%{travel_type}%"))
    if min_price is not None:
        query = query.filter(TravelManagement.price >= min_price)
    if max_price is not None:
        query = query.filter(TravelManagement.price <= max_price)
    return query


def search_deals(destination=None, platform=None, travel_type=None):
    query = apply_filters(
        TravelManagement.query,
        destination=destination,
        platform=platform,
        travel_type=travel_type,
    )
    return query.all()

def filter_deals_by_budget(min_price=None, max_price=None):
    query = apply_filters(
        TravelManagement.query,
        min_price=min_price,
        max_price=max_price,
    )
    return query.all()

def sort_deals(sort_by, order):
    column = getattr(TravelManagement, sort_by)
    direction = asc(column) if order == "asc" else desc(column)
    return TravelManagement.query.order_by(direction).all()

