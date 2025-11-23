import requests

API_KEY = "5b80491f498853dc8bb53a741b2463c6"  # Öğretmen tarafından verilebilir
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city: str) -> float:
    """
    Verilen şehir için anlık sıcaklığı (°C) döndürür.
    Hata kontrolü bu aşamada basit tutulmuştur.
    """
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "tr",
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    # OpenWeatherMap için sıcaklık bilgisi:
    # main -> temp
    temperature = data["main"]["temp"]
    return temperature


def main():
    print("=== Simple Weather App ===")
    city = input("Şehir adını giriniz: ").strip()

    temperature = get_weather(city)
    print(f"{city} için sıcaklık: {temperature}°C")


if __name__ == "__main__":
    main()

