import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL_CURRENT = "https://api.openweathermap.org/data/2.5/weather"
BASE_URL_FORECAST = "https://api.openweathermap.org/data/2.5/forecast"


class WeatherError(Exception):
    """Hava durumu ile ilgili özel hata tipimiz."""
    pass


if not API_KEY:
    raise RuntimeError("OPENWEATHER_API_KEY .env dosyasında bulunamadı.")


def choose_city() -> str:
    cities = ["Ankara", "Istanbul", "Izmir", "Yalova", "Bursa"]

    print("Şehir seç:")
    for i, c in enumerate(cities, start=1):
        print(f"{i}) {c}")
    print("0) Farklı bir şehir gir")

    choice = input("Seçiminiz: ").strip()

    if choice.isdigit():
        num = int(choice)
        if 1 <= num <= len(cities):
            return cities[num - 1]

    manual = input("Şehir adını yazın: ").strip()
    return manual


def get_weather(city: str) -> dict:
    if not city:
        raise WeatherError("Şehir adı boş olamaz.")

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "tr",
    }

    try:
        response = requests.get(BASE_URL_CURRENT, params=params, timeout=5)
    except requests.exceptions.RequestException as e:
        raise WeatherError(f"API isteği başarısız oldu: {e}") from e

    if response.status_code != 200:
        raise WeatherError(
            f"API, beklenmeyen bir durum döndürdü: {response.status_code}"
        )

    data = response.json()

    if "main" not in data or "weather" not in data:
        raise WeatherError("API yanıtı beklenen formatta değil.")

    main = data["main"]
    weather_list = data["weather"]
    description = weather_list[0]["description"] if weather_list else "bilinmiyor"

    return {
        "temp": main.get("temp"),
        "feels_like": main.get("feels_like"),
        "humidity": main.get("humidity"),
        "description": description,
    }


def get_forecast(city: str, limit: int = 4) -> list[dict]:
    if not city:
        raise WeatherError("Şehir adı boş olamaz (forecast).")

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "tr",
    }

    try:
        response = requests.get(BASE_URL_FORECAST, params=params, timeout=5)
    except requests.exceptions.RequestException as e:
        raise WeatherError(f"Forecast isteği başarısız oldu: {e}") from e

    if response.status_code != 200:
        raise WeatherError(
            f"Forecast API beklenmedik kod döndürdü: {response.status_code}"
        )

    data = response.json()
    if "list" not in data:
        raise WeatherError("Forecast yanıtı beklenen formatta değil.")

    items = []
    for entry in data["list"][:limit]:
        dt_txt = entry.get("dt_txt", "bilinmeyen zaman")
        main = entry.get("main", {})
        weather_list = entry.get("weather", [])
        desc = weather_list[0]["description"] if weather_list else "bilinmiyor"

        items.append(
            {
                "time": dt_txt,
                "temp": main.get("temp"),
                "description": desc,
            }
        )

    return items


def main():
    print("=== Advanced Weather App (v1.1) ===")

    city = choose_city()

    try:
        info = get_weather(city)
        forecast_items = get_forecast(city, limit=4)
    except WeatherError as e:
        print(f"[Hata] {e}")
        return

    print(f"\n{city} için anlık hava durumu:")
    print(f"- Sıcaklık        : {info['temp']}°C")
    print(f"- Hissedilen      : {info['feels_like']}°C")
    print(f"- Nem             : %{info['humidity']}")
    print(f"- Açıklama        : {info['description']}")

    print("\nÖnümüzdeki saatler için tahmin:")
    for item in forecast_items:
        print(f"  {item['time']}: {item['temp']}°C, {item['description']}")


if __name__ == "__main__":
    main()
