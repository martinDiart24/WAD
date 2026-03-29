from sqlalchemy.orm import Session

from ..api_clients import AutoKellyLikeAPI
from ..models import Part, Shop, ShopOffer


def _client_for_shop(shop: Shop):
    """
    Vytvoří vhodného API klienta podle typu obchodu.

    Pro reálné použití:
    - doplňte další větve pro konkrétní typy (např. 'aci', 'lkq', 'vrakoviste_x')
    - načtěte API klíče z prostředí / konfigurace
    """
    api_type = (shop.api_type or "").lower()

    if api_type in {"autokelly", "lkq"}:
        # base_url může být např. https://api-mobile.autokelly.cz/ apod. – nutno ověřit v dokumentaci
        return AutoKellyLikeAPI(base_url=shop.base_url, api_key=None)

    # výchozí – zatím žádný konkrétní klient
    return None


def sync_offers_for_part(session: Session, part: Part) -> None:
    """
    Projde registrované obchody a pokusí se pro daný díl načíst nabídky.

    POZOR:
    - pro skutečný provoz je potřeba doplnit konkrétní API klienty,
      endpointy a autentizaci.
    - ideálně spouštět přes plánovač (cron, Celery), ne při každém requestu.
    """
    if not part.oem_code:
        return

    shops = session.query(Shop).all()
    if not shops:
        return

    for shop in shops:
        client = _client_for_shop(shop)
        if client is None:
            continue

        try:
            results = client.search_part_by_oem(part.oem_code)
        except Exception:
            # v demu chyby ignorujeme; v produkci logovat
            continue

        for r in results:
            offer = (
                session.query(ShopOffer)
                .filter_by(part_id=part.id, shop_id=shop.id, product_url=r.get("url"))
                .first()
            )
            if offer is None:
                offer = ShopOffer(part_id=part.id, shop_id=shop.id)

            offer.price_czk = r.get("price_czk")
            offer.availability = r.get("availability")
            offer.product_url = r.get("url")

            session.add(offer)

    session.commit()

