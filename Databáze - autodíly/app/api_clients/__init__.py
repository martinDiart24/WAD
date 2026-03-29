"""
API klienti pro české e-shopy s autodíly.

Zde jsou pouze jednoduché obálky / rozhraní – každé API má většinou
vlastní autentizaci a formát dotazů, které je potřeba doplnit podle
konrétní dokumentace nebo dohody s dodavatelem.
"""

from .base import ShopAPIClient  # noqa: F401
from .autokelly_like import AutoKellyLikeAPI  # noqa: F401
