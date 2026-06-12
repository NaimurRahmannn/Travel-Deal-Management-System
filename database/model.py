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
    platform=db.coloumn(
        db.String(100),
        nullable=False
    )
    rating=db.column(
        db.Float,
        nullable=True
    )
    travel_type=db.column(
        db.String(50),
        nullable=False
    )
    
    def to_dic(self):
        return{
            "id":self.id,
            "destination": self.destination,
            "price":self.price,
            "platform":self.platform,
            "rating":self.rating,
            "travel_type":self.travel_type,
        }