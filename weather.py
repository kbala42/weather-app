API_KEY = "5b80491f498853dc8bb53a741b2463c6"  # Öğretmen tarafından verilebilir
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def main():
    print("=== Simple Weather App ===")
    city = input("Şehir adını giriniz: ").strip()

    print(f"Girdiğiniz şehir: {city!r}")


if __name__ == "__main__":
    main()
