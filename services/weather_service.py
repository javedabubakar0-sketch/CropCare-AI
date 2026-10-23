"""
CropCare AI - Weather & Meteorological Service
Interfaces with the free Open-Meteo REST API, provides memory caching with TTL,
and computes agricultural spray windows and disease risk alerts.
"""

import time
import requests
import config

# Simple in-memory cache: (lat, lon) -> (timestamp, data)
_WEATHER_CACHE = {}

def get_farm_weather(lat="31.5204", lon="74.3587", city_name="Lahore, Pakistan"):
    """
    Fetches real-time farm weather and 5-day forecast from Open-Meteo.
    Uses in-memory caching with TTL to avoid rate limits and survive temporary network drops.
    Calculates chemical spray safety windows, rain alerts, and fungal risk.
    """
    # Sanitize and round coordinates for cache key
    try:
        lat_val = round(float(lat), 3)
        lon_val = round(float(lon), 3)
    except (ValueError, TypeError):
        lat_val = 31.520
        lon_val = 74.359

    cache_key = f"{lat_val}_{lon_val}"
    now = time.time()

    # Check cache freshness
    if cache_key in _WEATHER_CACHE:
        cached_time, cached_data = _WEATHER_CACHE[cache_key]
        if (now - cached_time) < config.WEATHER_CACHE_TTL_SECONDS:
            cached_copy = dict(cached_data)
            cached_copy["city"] = city_name
            cached_copy["cached"] = True
            return cached_copy

    # Fetch from Open-Meteo API
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat_val}&longitude={lon_val}&"
        f"current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m&"
        f"daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max&"
        f"timezone=auto"
    )

    try:
        resp = requests.get(url, timeout=config.WEATHER_REQUEST_TIMEOUT)
        if resp.status_code != 200:
            # If request fails but stale cache exists, serve stale cache with note
            if cache_key in _WEATHER_CACHE:
                _, stale_data = _WEATHER_CACHE[cache_key]
                stale_copy = dict(stale_data)
                stale_copy["cached"] = True
                stale_copy["warning"] = "Serving cached data due to upstream weather server error."
                return stale_copy
            return {
                "success": False,
                "error": f"Open-Meteo API returned status {resp.status_code}",
                "message": "The weather service is temporarily unavailable."
            }

        data = resp.json()
        current = data.get("current", {})
        daily = data.get("daily", {})

        temp = current.get("temperature_2m", 25)
        humidity = current.get("relative_humidity_2m", 50)
        precip = current.get("precipitation", 0)
        wind_speed = current.get("wind_speed_10m", 8)

        # 1. Chemical Spray Window Advisory
        if wind_speed > 20:
            spray_status = "Unsafe - High Wind Drift"
            spray_status_ur = "غیر محفوظ - تیز ہوا"
            spray_advisory = f"Current wind speed ({wind_speed} km/h) exceeds safe threshold (15 km/h). Chemical spraying will cause severe drift damage and wasteful runoff. Postpone application."
            spray_advisory_ur = f"ہوا کی رفتار ({wind_speed} کلومیٹر فی گھنٹہ) زیادہ ہے۔ کیڑے مار ادویات یا کھاد کا اسپرے کرنے سے دوا ضائع ہوگی اور پڑوسی فصلوں کو نقصان پہنچ سکتا ہے۔"
            spray_color = "#991B1B"
        elif precip > 0.5:
            spray_status = "Unsafe - Active Rain"
            spray_status_ur = "غیر محفوظ - بارش جاری"
            spray_advisory = "Active precipitation detected. Pesticides or foliar fertilizers will be washed off immediately. Delay until leaves have dried thoroughly."
            spray_advisory_ur = "بارش جاری ہے۔ اسپرے نہ کریں ورنہ دوا دھل جائے گی۔ پتے خشک ہونے تک انتظار کریں۔"
            spray_color = "#991B1B"
        elif temp > 36:
            spray_status = "Caution - Extreme Heat"
            spray_status_ur = "احتیاط - شدید گرمی"
            spray_advisory = f"High midday temperature ({temp}°C) may cause foliar chemical burn (phytotoxicity). Spray only during early morning (6-8 AM) or late afternoon."
            spray_advisory_ur = f"درجہ حرارت ({temp} ڈگری) بہت زیادہ ہے۔ دن کی دھوپ میں اسپرے سے پتے جھلس سکتے ہیں۔ صبح سویرے یا عصر کے وقت اسپرے کریں۔"
            spray_color = "#B45309"
        else:
            spray_status = "Safe Spray Window"
            spray_status_ur = "اسپرے کے لیے سازگار"
            spray_advisory = f"Favorable conditions: Wind is calm ({wind_speed} km/h) and temperature is moderate ({temp}°C). Suitable for foliar nutrient and fungicide applications."
            spray_advisory_ur = f"موسم سازگار ہے: ہوا کی رفتار مناسب ({wind_speed} کلومیٹر) ہے اور بارش کا خطرہ نہیں۔ حفاظتی اسپرے کیا جا سکتا ہے۔"
            spray_color = "#2E6930"

        # 2. Disease / Blight Fungal Risk
        if humidity >= 80 and (16 <= temp <= 30):
            risk_level = "High Fungal Risk"
            risk_level_ur = "فنگس کا شدید خطرہ"
            risk_color = "#991B1B"
            disease_advisory = "Warm and damp atmosphere greatly accelerates Early Blight, Late Blight, and Downy Mildew spores. Scout vulnerable crops closely and check drainage."
            disease_advisory_ur = "زیادہ نمی اور معتدل گرمی سے جھلساؤ اور پھپھوندی کا خطرہ بہت زیادہ ہے۔ کھیت سے اضافی پانی نکالیں اور پودوں کا بغور معائنہ کریں۔"
        elif humidity >= 65 and (14 <= temp <= 32):
            risk_level = "Moderate Fungal Risk"
            risk_level_ur = "درمیانہ خطرہ"
            risk_color = "#B45309"
            disease_advisory = "Moderate humidity. Regular scouting recommended. Inspect undersides of lower leaves for early lesions."
            disease_advisory_ur = "درمیانی نمی۔ فصل کا معمول کا معائنہ جاری رکھیں اور نچلے پتوں کی نچلی سطح پر نظر رکھیں۔"
        else:
            risk_level = "Low Fungal Risk"
            risk_level_ur = "کم خطرہ"
            risk_color = "#2E6930"
            disease_advisory = "Low relative humidity and dry conditions inhibit fungal spore germination."
            disease_advisory_ur = "ہوا خشک ہے اور فنگل بیماریوں کا پھیلاؤ کم ہے۔"

        # 3. Weather alerts (Rain, Frost, Heatwave)
        alerts = []
        if daily.get("precipitation_sum") and daily["precipitation_sum"][0] > 5:
            alerts.append({
                "type": "rain",
                "text": f"Heavy rain forecasted today ({daily['precipitation_sum'][0]} mm). Postpone irrigation.",
                "text_ur": f"آج تیز بارش ({daily['precipitation_sum'][0]} ملی میٹر) متوقع ہے۔ نہری یا ٹیوب ویل کا پانی روک دیں۔"
            })
        if temp >= 38:
            alerts.append({
                "type": "heat",
                "text": "Extreme heat advisory. Ensure adequate soil moisture to prevent terminal heat stress.",
                "text_ur": "شدید گرمی کی لہر۔ پودوں کو مرجھانے سے بچانے کے لیے ہلکا پانی دیں۔"
            })
        elif temp <= 4:
            alerts.append({
                "type": "frost",
                "text": "Frost warning. Young seedlings and nursery beds may require protective cover or smoking.",
                "text_ur": "کورا پڑنے کا خطرہ۔ نرسری اور نازک فصلوں کو پولی تھین یا ہلکے پانی سے محفوظ رکھیں۔"
            })

        result = {
            "success": True,
            "city": city_name,
            "lat": lat_val,
            "lon": lon_val,
            "current": current,
            "daily": daily,
            "spray_status": spray_status,
            "spray_status_ur": spray_status_ur,
            "spray_advisory": spray_advisory,
            "spray_advisory_ur": spray_advisory_ur,
            "spray_color": spray_color,
            "risk_level": risk_level,
            "risk_level_ur": risk_level_ur,
            "risk_color": risk_color,
            "disease_advisory": disease_advisory,
            "disease_advisory_ur": disease_advisory_ur,
            "alerts": alerts,
            "cached": False
        }

        # Save to memory cache
        _WEATHER_CACHE[cache_key] = (now, result)
        return result

    except requests.exceptions.Timeout:
        # Timeout handling
        if cache_key in _WEATHER_CACHE:
            _, stale_data = _WEATHER_CACHE[cache_key]
            stale_copy = dict(stale_data)
            stale_copy["cached"] = True
            stale_copy["warning"] = "Serving cached weather data due to connection timeout."
            return stale_copy
        return {
            "success": False,
            "error": "Weather Service Timeout",
            "message": "Connection to the Open-Meteo weather service timed out. Please check your internet connection."
        }

    except Exception as e:
        # General network / upstream exception handling
        if cache_key in _WEATHER_CACHE:
            _, stale_data = _WEATHER_CACHE[cache_key]
            stale_copy = dict(stale_data)
            stale_copy["cached"] = True
            stale_copy["warning"] = "Serving cached weather data due to network error."
            return stale_copy
        return {
            "success": False,
            "error": "Weather Service Unavailable",
            "message": f"Unable to reach the Open-Meteo weather API: {str(e)}"
        }

def get_upcoming_rainfall_sum(lat="31.5204", lon="74.3587", days=3):
    """
    Helper to fetch forecast rainfall total (mm) over the next N days.
    """
    weather = get_farm_weather(lat, lon)
    if weather.get("success") and weather.get("daily", {}).get("precipitation_sum"):
        precip_list = weather["daily"]["precipitation_sum"][:days]
        return round(sum(precip_list), 1)
    return 0.0
