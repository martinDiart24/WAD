from typing import Iterable, Mapping

import requests

from .base import ShopAPIClient


class AutoKellyLikeAPI(ShopAPIClient):
    """
    Velmi zjednodušený příklad klienta pro API podobné Auto Kelly / LKQ.

    POZOR:
    - URL endpointů, hlavičky a parametry je nutné doplnit podle
      skutečné dokumentace API nebo po domluvě s dodavatelem.
    - Pro komerční použití je téměř jistě potřeba smluvní přístup.
    """

    def _request(self, path: str, params: dict) -> dict:
        url = f"{self.base_url}/{path.lstrip('/')}"
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        resp = requests.get(url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def search_part_by_oem(self, oem_code: str) -> Iterable[Mapping]:
        # TODO: nahradit skutečným endpointem a mapováním odpovědi
        data = self._request(
            "/api/parts/search",
            {"oem": oem_code},
        )
        for item in data.get("items", []):
            yield {
                "name": item.get("name"),
                "price_czk": item.get("price"),
                "availability": item.get("availability_text"),
                "url": item.get("url"),
                "shop_name": "Auto Kelly (příklad)",
            }

    def search_part_by_keyword(self, keyword: str) -> Iterable[Mapping]:
        # TODO: nahradit skutečným endpointem a mapováním odpovědi
        data = self._request(
            "/api/parts/search",
            {"q": keyword},
        )
        for item in data.get("items", []):
            yield {
                "name": item.get("name"),
                "price_czk": item.get("price"),
                "availability": item.get("availability_text"),
                "url": item.get("url"),
                "shop_name": "Auto Kelly (příklad)",
            }

