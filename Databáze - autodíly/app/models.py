from datetime import datetime

from . import db


class Manufacturer(db.Model):
    __tablename__ = "manufacturers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    country = db.Column(db.String(80))

    car_models = db.relationship("CarModel", back_populates="manufacturer")


class CarModel(db.Model):
    __tablename__ = "car_models"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    year_from = db.Column(db.Integer, nullable=False)
    year_to = db.Column(db.Integer, nullable=True)

    manufacturer_id = db.Column(db.Integer, db.ForeignKey("manufacturers.id"), nullable=False)
    manufacturer = db.relationship("Manufacturer", back_populates="car_models")

    engines = db.relationship("Engine", back_populates="car_model")


class Engine(db.Model):
    __tablename__ = "engines"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), nullable=False)
    fuel_type = db.Column(db.String(30))  # benzín, nafta, LPG...
    capacity_l = db.Column(db.Float)  # objem v litrech
    power_kw = db.Column(db.Integer)

    car_model_id = db.Column(db.Integer, db.ForeignKey("car_models.id"), nullable=False)
    car_model = db.relationship("CarModel", back_populates="engines")

    engine_parts = db.relationship("EnginePartCompatibility", back_populates="engine")


class PartCategory(db.Model):
    __tablename__ = "part_categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    parts = db.relationship("Part", back_populates="category")


class Part(db.Model):
    __tablename__ = "parts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    oem_code = db.Column(db.String(120), index=True)
    description = db.Column(db.Text)

    category_id = db.Column(db.Integer, db.ForeignKey("part_categories.id"), nullable=False)
    category = db.relationship("PartCategory", back_populates="parts")

    compatibilities = db.relationship("EnginePartCompatibility", back_populates="part")
    offers = db.relationship("ShopOffer", back_populates="part")


class EnginePartCompatibility(db.Model):
    __tablename__ = "engine_part_compatibility"

    id = db.Column(db.Integer, primary_key=True)
    engine_id = db.Column(db.Integer, db.ForeignKey("engines.id"), nullable=False)
    part_id = db.Column(db.Integer, db.ForeignKey("parts.id"), nullable=False)

    engine = db.relationship("Engine", back_populates="engine_parts")
    part = db.relationship("Part", back_populates="compatibilities")


class Shop(db.Model):
    __tablename__ = "shops"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    base_url = db.Column(db.String(255), nullable=False)
    api_type = db.Column(db.String(50), nullable=True)  # např. 'autokelly', 'custom'

    offers = db.relationship("ShopOffer", back_populates="shop")


class ShopOffer(db.Model):
    __tablename__ = "shop_offers"

    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey("parts.id"), nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey("shops.id"), nullable=False)

    price_czk = db.Column(db.Numeric(10, 2), nullable=False)
    availability = db.Column(db.String(120))
    product_url = db.Column(db.String(255))
    last_synced_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    part = db.relationship("Part", back_populates="offers")
    shop = db.relationship("Shop", back_populates="offers")
