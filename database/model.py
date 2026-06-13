from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class TravelManagement(db.Model):
    __tablename__="travel_management"
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    destination=db.Column(
        db.String(300),
        nullable=False
    )
    price=db.Column(
        db.Float,
        nullable=False
    )
    platform=db.Column(
        db.String(100),
        nullable=False
    )
    rating=db.Column(
        db.Float,
        nullable=True
    )
    travel_type=db.Column(
        db.String(50),
        nullable=False
    )
    # convert model object to dictionary
    def to_dic(self):
        return{
            "id":self.id,
            "destination": self.destination,
            "price":self.price,
            "platform":self.platform,
            "rating":self.rating,
            "travel_type":self.travel_type,
        }
        
class RecentView(db.Model):
    __tablename__ = "recent_views"
    id = db.Column(db.Integer, primary_key=True)
    deal_id = db.Column(
        db.Integer,
        db.ForeignKey("travel_management.id"),
        nullable=False,
        unique=True
    )
    viewed_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        nullable=False
    )

    def to_dic(self):
        return {
            "id": self.id,
            "deal_id": self.deal_id,
            "viewed_at": self.viewed_at.isoformat() if self.viewed_at else None,
        }