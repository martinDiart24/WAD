"""
Rychlé naplnění tabulky Shop ukázkovými obchody (dealers + vrakoviště).

Tyto záznamy jsou pouze ilustrativní – base_url a api_type si
upravte podle toho, jaké reálné API máte k dispozici.
"""

from app import create_app, db
from app.models import Shop


def main():
    app = create_app()
    with app.app_context():
        examples = [
            # e‑shopy s novými díly (příkladné API typy)
            ("Auto Kelly", "https://api-mobile.autokelly.cz", "autokelly"),
            ("LKQ CZ", "https://api.lkq.cz", "lkq"),
            ("ACI Autodíly", "https://api.aci.cz", "aci"),
            ("MROAuto", "https://api.mroauto.cz", "generic"),
            ("CC Autodíly", "https://api.cc-autodily.cz", "generic"),
            ("Autodíly Cardion", "https://api.cardion.cz", "generic"),
            # vrakoviště – předpoklad případného API / feedu
            ("Vrakoviště Morava", "https://api.vrakovistemorava.cz", "wreck"),
            ("Vrakoviště Praha", "https://api.vrakovistepraha.cz", "wreck"),
            ("Autovrakoviště Brno", "https://api.autovrakovistebrno.cz", "wreck"),
            ("Vrakoviště Sever", "https://api.vrakovistesever.cz", "wreck"),
            ("Vrakoviště Jih", "https://api.vrakovistejih.cz", "wreck"),
        ]

        for name, base_url, api_type in examples:
            exists = Shop.query.filter_by(name=name).first()
            if exists:
                continue
            shop = Shop(name=name, base_url=base_url, api_type=api_type)
            db.session.add(shop)

        db.session.commit()
        print("Shopy byly vloženy / aktualizovány.")


if __name__ == "__main__":
    main()

