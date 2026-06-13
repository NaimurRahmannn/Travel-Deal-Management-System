from sqlalchemy.exc import SQLAlchemyError

from database.model import db, TravelManagement,RecentView
from utils.validators import validate_deal
from utils.logger import logger
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



def track_recent(deal):

    try:
        # Remove the old deal first to avoid duplicates
        RecentView.query.filter_by(deal_id=deal.id).delete()
        db.session.add(RecentView(deal_id=deal.id))
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        logger.warning(f"Could not track recent view for deal {deal.id}")

def get_recent_deals():
    recents = RecentView.query.order_by(RecentView.viewed_at.desc()).limit(10).all()
    deals = []
    for r in recents:
        deal = TravelManagement.query.get(r.deal_id)
        if deal:
            deals.append(deal.to_dic())
    return deals

