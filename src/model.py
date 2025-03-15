from . import db
from datetime import datetime, timezone

class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    qty_in_stock = db.Column(db.Integer, nullable=False)
    reorder_point = db.Column(db.Integer, nullable=False)
    reorder_quantity = db.Column(db.Integer, nullable=False)
    restock_date = db.Column(db.Date, default=datetime.now(timezone.utc))
    lead_time = db.Column(db.Integer, nullable=False)
    ordering_cost = db.Column(db.Float, nullable=False, default=0)
    holding_cost = db.Column(db.Float, nullable=False, default=0)
    setup_cost = db.Column(db.Float, nullable=False, default=0)