"""Weather lookup using the free wttr.in service (no API key needed)."""

from __future__ import annotations

import json
import urllib.parse
import urllib.request

_ENDPOINT = "https://wttr.in/{city}?format=j1"
_USER_AGENT = "NomiAI/1.0"


def run(argument: str = "") -> str:
    city = argument.strip()
    if not city:
        return "Which city? Try 'weather in Karachi'."
    url = _ENDPOINT.format(city=urllib.parse.quote(city))
    request = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
        current = data["current_condition"][0]
        area = data["nearest_area"][0]
        place = area["areaName"][0]["value"]
        country = area["country"][0]["value"]
    except Exception:
        return f"I couldn't fetch the weather for '{city}' right now."
    description = current["weatherDesc"][0]["value"]
    return (
        f"Weather in {place}, {country}: {description}, "
        f"{current['temp_C']}°C (feels like {current['FeelsLikeC']}°C), "
        f"humidity {current['humidity']}%, "
        f"wind {current['windspeedKmph']} km/h {current['winddir16Point']}."
    )
