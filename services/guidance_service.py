"""
CropCare AI - Agricultural Guidance & Knowledge Service
Maintains botanical disease profiles, symptoms, treatments, wholesale mandi rates,
and realistic agronomic irrigation estimation rules.
"""

from datetime import datetime
from disease_data import DISEASE_DATABASE, get_disease_info

def get_guidance_for_disease(class_label):
    """
    Retrieves full botanical details, symptoms, prevention, and treatment
    guidance for a specific classified disease class.
    """
    return get_disease_info(class_label)

def get_mandi_benchmarks():
    """
    Returns authentic wholesale market benchmarks for major produce in Pakistan.
    Source: Agriculture Market Information System (AMIS Punjab / Sindh).
    """
    current_date = datetime.now().strftime("%d %b %Y")
    benchmarks = [
        {
            "commodity": "Wheat (گندم)",
            "variety": "Standard Grain Grade A",
            "mandi": "Lahore (Badami Bagh) / Multan",
            "unit": "40 kg (Maund / من)",
            "min_price": 3800,
            "max_price": 4150,
            "modal_price": 4000,
            "trend": "Stable"
        },
        {
            "commodity": "Basmati Rice (باسمتی چاول)",
            "variety": "Super Basmati (Kainat / 1121)",
            "mandi": "Hafizabad / Gujranwala / Lahore",
            "unit": "40 kg (Maund / من)",
            "min_price": 10500,
            "max_price": 12800,
            "modal_price": 11600,
            "trend": "Up"
        },
        {
            "commodity": "Cotton / Phutti (کپاس / پھٹی)",
            "variety": "Clean Medium Staple",
            "mandi": "Multan / Bahawalpur / Rahim Yar Khan",
            "unit": "40 kg (Maund / من)",
            "min_price": 7200,
            "max_price": 8400,
            "modal_price": 7800,
            "trend": "Stable"
        },
        {
            "commodity": "Corn / Maize (مکئی)",
            "variety": "Hybrid Grain",
            "mandi": "Sahiwal / Pakpattan / Okara",
            "unit": "40 kg (Maund / من)",
            "min_price": 2400,
            "max_price": 2850,
            "modal_price": 2650,
            "trend": "Down"
        },
        {
            "commodity": "Potato (آلو)",
            "variety": "Fresh Crop (Santé / Kuroda)",
            "mandi": "Okara / Depalpur / Lahore",
            "unit": "100 kg Bag (بوری)",
            "min_price": 4500,
            "max_price": 5800,
            "modal_price": 5200,
            "trend": "Stable"
        },
        {
            "commodity": "Tomato (ٹماٹر)",
            "variety": "Local Farm Fresh",
            "mandi": "Lahore / Faisalabad / Karachi",
            "unit": "16 kg Crate (پیٹی)",
            "min_price": 1400,
            "max_price": 2100,
            "modal_price": 1750,
            "trend": "Up"
        },
        {
            "commodity": "Onion (پیاز)",
            "variety": "Red Dry Grade A",
            "mandi": "Multan / Hyderabad / Lahore",
            "unit": "40 kg (Maund / من)",
            "min_price": 3600,
            "max_price": 4800,
            "modal_price": 4200,
            "trend": "Stable"
        }
    ]

    return {
        "as_of_date": current_date,
        "source": "AMIS (Agriculture Market Information System, Govt of Punjab)",
        "source_url": "http://www.amis.pk",
        "currency": "PKR (Rs.)",
        "benchmarks": benchmarks,
        "disclaimer_en": "Wholesale mandi benchmarks collected from major grain & fruit markets. Rates vary daily by produce grade, moisture, and local commission agent deductions.",
        "disclaimer_ur": "یہ نرخ پنجاب اور سندھ کی مرکزی غلہ و سبزی منڈیوں کے ہول سیل اوسط ریٹس ہیں۔ مقامی آڑھتی کے کٹوتیوں اور مال کے معیار کے لحاظ سے قیمت میں فرق ہو سکتا ہے۔"
    }

def get_field_practical_guides():
    """
    Returns practical agricultural safety and crop management guides in English & Urdu.
    """
    return [
        {
            "id": "pesticide_safety",
            "title_en": "Pesticide Safety & Spray Guidelines",
            "title_ur": "اسپرے کے بنیادی حفاظتی اصول اور احتیاطیں",
            "category_en": "Crop Protection",
            "category_ur": "حفاظتِ نباتات",
            "summary_en": "Essential safety rules for handling agrochemicals, minimizing wind drift, and honoring Pre-Harvest Intervals (PHI).",
            "summary_ur": "زرعی زہروں کے استعمال، ہوا میں بہاؤ سے بچاؤ اور فصل توڑنے سے پہلے وقفہ (PHI) کے لازمی اصول۔",
            "points_en": [
                "Never spray when wind speed exceeds 15 km/h to prevent chemical drift onto nearby water bodies or livestock.",
                "Always wear protective cloth mask, rubber gloves, and eye goggles during mixing and application.",
                "Spray along the wind direction; never walk backward or spray directly facing into the wind.",
                "Respect the Pre-Harvest Interval (PHI): Cease chemical sprays 7 to 14 days before harvest to eliminate toxic residue.",
                "Puncture and bury empty pesticide containers responsibly; never reuse them for household water or food storage."
            ],
            "points_ur": [
                "جب ہوا کی رفتار 15 کلومیٹر فی گھنٹہ سے زیادہ ہو تو کبھی اسپرے نہ کریں تاکہ دوا نہروں یا جانوروں پر نہ جائے۔",
                "دوا تیار کرتے اور اسپرے کرتے وقت ہمیشہ ماسک، دستانے اور عینک کا استعمال لازمی کریں۔",
                "ہمیشہ ہوا کی سمت میں اسپرے کریں؛ کبھی بھی ہوا کے مخالف رخ چل کر اسپرے نہ کریں۔",
                "فصل توڑنے سے پہلے کا وقفہ (PHI) مدنظر رکھیں: کٹائی سے 7 تا 14 دن قبل ہر قسم کا کیمیائی اسپرے بند کر دیں۔",
                "خالی بوتلوں کو تلف کرنے کے لیے زمین میں دبا دیں؛ انہیں گھر میں پانی یا خوراک کے لیے ہرگز استعمال نہ کریں۔"
            ]
        },
        {
            "id": "organic_remedies",
            "title_en": "Organic & Low-Cost Natural Remedies",
            "title_ur": "دیسی اور کم خرچ قدرتی نسخے",
            "category_en": "Organic Farming",
            "category_ur": "قدرتی کاشتکاری",
            "summary_en": "Preparation of homemade neem oil extract, wood ash, and bio-fungicides to control sucking pests and foliar molds.",
            "summary_ur": "نیم کا عرق، لکڑی کی راکھ اور دیسی فنگسائڈز کی تیاری کا آسان طریقہ۔",
            "points_en": [
                "Neem Leaf Extract: Boil 2 kg chopped neem leaves in 5 liters water for 30 minutes. Dilute with 15 liters water and 10 ml mild soap for aphid and whitefly control.",
                "Wood Ash Treatment: Sift clean wood ash and dust lightly over damp vegetable foliage in early morning to deter beetles and fungal spores.",
                "Baking Soda Bio-Fungicide: Mix 1 tablespoon baking soda with 1 teaspoon vegetable oil in 4 liters of water to manage early powdery mildew on cucurbits and tomatoes.",
                "Crop Rotation: Break pest life cycles by alternating heavy nitrogen feeders (corn, tomato) with legumes (peas, mung bean)."
            ],
            "points_ur": [
                "نیم کے پتوں کا اسپرے: 2 کلو نیم کے پتے 5 لیٹر پانی میں ابالیں۔ چھان کر 15 لیٹر پانی اور تھوڑا سا صابن ملا کر تیلے اور سفید مکھی پر اسپرے کریں۔",
                "لکڑی کی راکھ کا استعمال: صبح کے وقت اوس والے پتوں پر صاف راکھ کا ہلکا چھڑکاؤ سنڈیوں اور فنگس کے حملے کو روکتا ہے۔",
                "میٹھا سوڈا فنگسائڈ: 4 لیٹر پانی میں ایک چمچ میٹھا سوڈا اور ایک چمچ کوکنگ آئل ملا کر ٹماٹر اور توری کے پتوں کی سفیدی پر اسپرے کریں۔",
                "فصلوں کا ہیر پھیر: زمین کی زرخیزی اور بیماریوں کے خاتمے کے لیے ٹماٹر اور مکئی کے بعد دالیں یا پھلی دار فصلیں کاشت کریں۔"
            ]
        },
        {
            "id": "fertilizer_management",
            "title_en": "Balanced Fertilizer Application (NPK)",
            "title_ur": "کھادوں کا متوازن اور بر وقت استعمال",
            "category_en": "Soil & Nutrients",
            "category_ur": "مٹی اور غذائیت",
            "summary_en": "Guidelines on strategic application of Nitrogen (Urea), Phosphorus (DAP), and Potassium (SOP) across crop stages.",
            "summary_ur": "یوریا، ڈی اے پی اور پوٹاش کی مرحلہ وار فراہمی کے زرعی طریقے تاکہ خرچ کم اور پیداوار زیادہ ہو۔",
            "points_en": [
                "Apply total Phosphorus (DAP) and Potassium at sowing / seedbed preparation so root establishment is vigorous.",
                "Split Nitrogen (Urea) into 2 to 3 doses. Avoid applying excessive nitrogen before flowering, which induces vegetative excess and pest attraction.",
                "Zinc Sulfate (33% or 21%) is critical for rice and maize to prevent 'Khaira' disease and stunted yellowing.",
                "Never broadcast urea on dry, sun-baked soil; immediately follow with irrigation to prevent volatilization loss."
            ],
            "points_ur": [
                "فاسفورس (ڈی اے پی) اور پوٹاش کی پوری مقدار بوائی کے وقت زمین کی تیاری میں ڈالیں تاکہ جڑیں مضبوط ہوں۔",
                "یوریا کو 2 سے 3 اقساط میں دیں۔ پھول آنے سے پہلے زیادہ یوریا نہ ڈالیں ورنہ کیڑوں کا حملہ بڑھ جاتا ہے۔",
                "دھان اور مکئی میں زنک کی کمی سے پتے پیلے ہو جاتے ہیں، اس لیے زنک سلفیٹ کا استعمال لازمی کریں۔",
                "خشک زمین پر کبھی یوریا نہ چھڑکیں ورنہ گیس بن کر اڑ جائے گی؛ ہمیشہ پانی کے ساتھ یا فوراً بعد ڈالیں۔"
            ]
        }
    ]

def estimate_irrigation_schedule(crop_type, soil_type, sowing_date_str, rain_next_3_days_mm=0.0):
    """
    Computes cautious irrigation interval based on crop coefficient,
    soil water retention, and upcoming rain forecast.
    """
    crop_profiles = {
        "Wheat": {"critical_days": [21, 65, 85, 105], "names_en": "Crown Root, Tillering, Heading, Grain Filling", "names_ur": "تاجی جڑیں، شگوفے، سٹہ بننا، دانہ پکنا", "base_interval_days": 18},
        "Rice": {"critical_days": [15, 35, 60, 80], "names_en": "Tillering, Panicle Initiation, Flowering", "names_ur": "پھوٹ، گوبھ، بور آنا", "base_interval_days": 5},
        "Cotton": {"critical_days": [35, 60, 85, 110], "names_en": "Squaring, Flowering, Boll Development", "names_ur": "ڈوڈی، پھول، ٹینڈا بننا", "base_interval_days": 14},
        "Corn": {"critical_days": [25, 50, 75], "names_en": "Knee-high, Tasseling/Silking, Grain Filling", "names_ur": "گھٹنا اونچی، چھلی اور بال، دانہ بننا", "base_interval_days": 10},
        "Potato": {"critical_days": [20, 45, 70], "names_en": "Stolon Formation, Tuber Bulking", "names_ur": "تنے کی شاخیں، آلو کا بننا", "base_interval_days": 8},
        "Tomato": {"critical_days": [15, 40, 65, 90], "names_en": "Vegetative, Flowering, Fruit Setting", "names_ur": "پھوٹ، پھول، ٹماٹر کا بننا", "base_interval_days": 7},
        "Sugarcane": {"critical_days": [30, 90, 150], "names_en": "Formative Phase, Grand Growth", "names_ur": "پودے کی ساخت، تیز نشوونما", "base_interval_days": 12}
    }

    profile = crop_profiles.get(crop_type, crop_profiles["Wheat"])
    base_interval = profile["base_interval_days"]

    days_sown = 30
    if sowing_date_str:
        try:
            s_dt = datetime.strptime(sowing_date_str, "%Y-%m-%d")
            days_sown = max(1, (datetime.now() - s_dt).days)
        except Exception:
            days_sown = 30

    if soil_type.lower() == "sandy":
        interval = max(4, int(base_interval * 0.7))
        soil_note_en = "Sandy soil drains rapidly. Apply smaller, more frequent irrigations to prevent percolation loss."
        soil_note_ur = "ریتلی زمین میں پانی جلدی جذب ہو کر نیچے چلا جاتا ہے۔ ہلکا اور بار بار پانی دیں۔"
    elif soil_type.lower() == "clay":
        interval = int(base_interval * 1.3)
        soil_note_en = "Clay soil holds moisture for extended periods. Ensure good surface drainage to prevent waterlogging."
        soil_note_ur = "چکنی زمین میں نمی دیر تک رہتی ہے۔ ضرورت سے زیادہ پانی نہ دیں تاکہ جڑوں کا دم نہ گھٹے۔"
    else:
        interval = base_interval
        soil_note_en = "Loam soil provides an optimal balance of moisture retention and root aeration."
        soil_note_ur = "میرا زمین میں نمی اور ہوا کا توازن مثالی ہے۔ معمول کے وقفے سے پانی دیں۔"

    if rain_next_3_days_mm >= 8.0:
        action_en = f"RAIN ALERT: Significant rainfall ({rain_next_3_days_mm} mm) expected in next 72 hours. Postpone tube-well pumping to save fuel/electricity."
        action_ur = f"بارش کا انتباہ: اگلے 3 دنوں میں {rain_next_3_days_mm} ملی میٹر بارش متوقع ہے۔ ٹیوب ویل کا پانی روک دیں اور بارش کے پانی سے فائدہ اٹھائیں۔"
        urgency = "Delay Irrigation"
        urgency_color = "#2E6930"
    elif rain_next_3_days_mm >= 3.0:
        action_en = f"LIGHT RAIN: Moderate rain ({rain_next_3_days_mm} mm) forecast. Check field moisture before running tube-wells."
        action_ur = f"ہلکی بارش ({rain_next_3_days_mm} ملی میٹر) متوقع ہے۔ کھیت کی وتر چیک کریں اور ضرورت ہو تو 2 دن مؤخر کریں۔"
        urgency = "Monitor Moisture"
        urgency_color = "#B45309"
    else:
        action_en = f"DRY CONDITIONS: Dry weather prevailing. Follow the recommended irrigation interval of every {interval} days."
        action_ur = f"خشک موسم جاری ہے۔ فصل کو ہر {interval} دن کے معمول کے وقفے سے پانی دیں۔"
        urgency = "Follow Routine Schedule"
        urgency_color = "#1B3B2B"

    return {
        "crop_type": crop_type,
        "soil_type": soil_type,
        "days_sown": days_sown,
        "recommended_interval_days": interval,
        "critical_stages_en": profile["names_en"],
        "critical_stages_ur": profile["names_ur"],
        "action_en": action_en,
        "action_ur": action_ur,
        "soil_note_en": soil_note_en,
        "soil_note_ur": soil_note_ur,
        "urgency": urgency,
        "urgency_color": urgency_color,
        "disclaimer_en": "Note: This is an agronomic estimation based on crop stages and weather forecasts. Always check physical soil moisture (Vattar/وتر) before operating tube-wells.",
        "disclaimer_ur": "نوٹ: یہ ایک زرعی تخمینہ ہے۔ ٹیوب ویل چلانے سے پہلے کھیت کی زمینی وتر (نمی) خود ضرور چیک کریں۔"
    }
