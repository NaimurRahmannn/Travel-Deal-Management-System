from sqlalchemy.exc import SQLAlchemyError

from database.model import db, TravelManagement
from utils.validators import validate_deal

def create_deal(data):
    error=validate_deal(data)
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

def apply_filters(query,destination=None):
    if destination:
       query = query.filter(TravelManagement.destination.ilike(f"%{destination}%"))
    return query

def search_deals(destination=None):
    query=apply_filters(TravelManagement.query,destination=destination)
    return query.all()