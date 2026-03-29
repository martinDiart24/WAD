"""
Naplní databázi ukázkovými daty: výrobci, modely, motory, kategorie dílů, díly a vazby.
Spusťte jednou před prvním použitím aplikace (po vytvoření tabulek).
"""
from app import create_app, db
from app.models import (
    CarModel,
    Engine,
    EnginePartCompatibility,
    Manufacturer,
    Part,
    PartCategory,
)


def main():
    app = create_app()
    with app.app_context():
        db.create_all()

        if Manufacturer.query.first():
            print("Databáze již obsahuje data. Pro znovunaplnění smažte soubor car_parts.db a spusťte znovu.")
            return

        # Výrobci
        vw = Manufacturer(name="Volkswagen", country="DE")
        skoda = Manufacturer(name="Škoda", country="CZ")
        db.session.add_all([vw, skoda])
        db.session.flush()

        # Modely
        golf = CarModel(
            name="Golf",
            year_from=2008,
            year_to=2012,
            manufacturer_id=vw.id,
        )
        octavia = CarModel(
            name="Octavia",
            year_from=2010,
            year_to=None,
            manufacturer_id=skoda.id,
        )
        db.session.add_all([golf, octavia])
        db.session.flush()

        # Motory
        engine_bxe = Engine(
            code="BXE",
            fuel_type="nafta",
            capacity_l=1.9,
            power_kw=77,
            car_model_id=golf.id,
        )
        engine_caxa = Engine(
            code="CAXA",
            fuel_type="benzín",
            capacity_l=1.4,
            power_kw=90,
            car_model_id=octavia.id,
        )
        db.session.add_all([engine_bxe, engine_caxa])
        db.session.flush()

        # Kategorie dílů
        cat_filter = PartCategory(name="Filtry")
        cat_brzdy = PartCategory(name="Brzdový systém")
        db.session.add_all([cat_filter, cat_brzdy])
        db.session.flush()

        # Díly
        part1 = Part(
            name="Olejový filtr",
            oem_code="03G115561B",
            category_id=cat_filter.id,
        )
        part2 = Part(
            name="Vzduchový filtr",
            oem_code="1K0129620E",
            category_id=cat_filter.id,
        )
        part3 = Part(
            name="Brzdové destičky přední",
            oem_code="1K0698151C",
            category_id=cat_brzdy.id,
        )
        db.session.add_all([part1, part2, part3])
        db.session.flush()

        # Kompatibilita motor – díl
        db.session.add_all([
            EnginePartCompatibility(engine_id=engine_bxe.id, part_id=part1.id),
            EnginePartCompatibility(engine_id=engine_bxe.id, part_id=part2.id),
            EnginePartCompatibility(engine_id=engine_bxe.id, part_id=part3.id),
            EnginePartCompatibility(engine_id=engine_caxa.id, part_id=part1.id),
        ])

        db.session.commit()
        print("Ukázková data byla vložena. Otevřete http://127.0.0.1:5000/ a klikněte na motor BXE nebo CAXA.")


if __name__ == "__main__":
    main()
