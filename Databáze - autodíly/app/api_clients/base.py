from abc import ABC, abstractmethod
from typing import Iterable, Mapping


class ShopAPIClient(ABC):
    """
    Základní rozhraní pro API klienty e‑shopů.

    Konkrétní implementace (Auto Kelly, LKQ, ACI atd.) budou dědit z této
    třídy a implementují metody podle dokumentace daného API.
    """

    def __init__(self, base_url: str, api_key: str | None = None):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    @abstractmethod
    def search_part_by_oem(self, oem_code: str) -> Iterable[Mapping]:
        """
        Vyhledání dílů podle OEM kódu.
        Měla by vracet iterovatelnou kolekci slovníků např.:
        {
            "name": "...",
            "price_czk": 123.45,
            "availability": "Skladem",
            "url": "https://...",
            "shop_name": "Auto Kelly",
        }
        """

    @abstractmethod
    def search_part_by_keyword(self, keyword: str) -> Iterable[Mapping]:
        """
        Vyhledání dílů podle textového názvu / klíčového slova.
        """

