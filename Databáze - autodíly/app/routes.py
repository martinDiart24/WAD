from flask import Blueprint, render_template, request, abort

from . import db
from .models import CarModel, Engine, EnginePartCompatibility, Part, ShopOffer
from .services.search import find_parts_for_engine
from .services.sync_offers import sync_offers_for_part

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    car_models = CarModel.query.order_by(CarModel.manufacturer_id, CarModel.name).all()
    return render_template("index.html", car_models=car_models)


@main_bp.route("/engine/<int:engine_id>")
def engine_detail(engine_id: int):
    engine = Engine.query.get_or_404(engine_id)
    compatibilities = (
        EnginePartCompatibility.query.filter_by(engine_id=engine.id)
        .join(Part)
        .order_by(Part.name)
        .all()
    )
    return render_template(
        "engine_detail.html",
        engine=engine,
        compatibilities=compatibilities,
    )


@main_bp.route("/search-parts")
def search_parts():
    query = request.args.get("q", "").strip()
    results = []

    if query:
        results = find_parts_for_engine(db.session, query)

    return render_template("search_parts.html", query=query, results=results)


@main_bp.route("/part/<int:part_id>")
def part_detail(part_id: int):
    part = Part.query.get_or_404(part_id)

    # volitelně si můžete před zobrazením spustit synchronizaci s e‑shopy
    # (v produkci spíše přes plánovač typu cron / celery beat)
    try:
        sync_offers_for_part(db.session, part)
    except Exception:
        # v demu chyby z externích API tiše ignorujeme
        pass

    offers = (
        ShopOffer.query.filter_by(part_id=part.id)
        .order_by(ShopOffer.price_czk.asc())
        .all()
    )

    if not offers:
        # může být None, pokud část aplikace ještě není nastavená
        best_price = None
    else:
        best_price = min((o.price_czk for o in offers if o.price_czk is not None), default=None)

    return render_template(
        "part_detail.html",
        part=part,
        offers=offers,
        best_price=best_price,
    )
