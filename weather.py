import requests

API_KEY = "5b80491f498853dc8bb53a741b2463c6"  # Öğretmen tarafından verilebilir
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


class WeatherError(Exception):
    """Hava durumu ile ilgili özel hata tipimiz."""
    pass


def get_weather(city: str) -> float:
    """
    Verilen şehir için anlık sıcaklığı (°C) döndürür.
    Hata olması durumunda WeatherError fırlatır.
    """
    if not city:
        raise WeatherError("Şehir adı boş olamaz.")

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "tr",
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
    except requests.exceptions.RequestException as e:
        raise WeatherError(f"API isteği başarısız oldu: {e}") from e

    if response.status_code != 200:
        # Örn. 404 (city not found) veya 401 (invalid API key)
        raise WeatherError(
            f"API, beklenmeyen bir durum döndürdü: {response.status_code}"
        )

    data = response.json()

    # Beklenen yapı yoksa:
    if "main" not in data or "temp" not in data["main"]:
        raise WeatherError("API yanıtı beklenen formatta değil.")

    temperature = data["main"]["temp"]
    return temperature


def main():
    print("=== Simple Weather App ===")

    city = input("Şehir adını giriniz: ").strip()

    try:
        temperature = get_weather(city)
    except WeatherError as e:
        print(f"[Hata] {e}")
        return

    print(f"{city} için sıcaklık: {temperature}°C")


if __name__ == "__main__":
    main()
