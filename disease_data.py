"""
CropCare AI - Disease Knowledge Base (English & Urdu)
Contains botanical details, symptoms, prevention, organic remedies,
and weather susceptibility for each crop disease class.
"""

DISEASE_DATABASE = {
    "Tomato___healthy": {
        "crop": "Tomato",
        "crop_ur": "ٹماٹر",
        "disease_name": "Healthy Leaf",
        "disease_name_ur": "صحت مند پتا",
        "scientific_name": "Solanum lycopersicum",
        "status": "Healthy",
        "status_ur": "صحت مند",
        "severity": "None",
        "severity_ur": "کوئی بیماری نہیں",
        "symptoms": "Uniform deep green foliage, crisp leaf margins, normal vein patterns, and no visible lesions or discoloration.",
        "symptoms_ur": "پتے کا رنگ یکساں گہرا سبز ہے، کنارے صاف ہیں اور کسی قسم کے دھبے یا زردی موجود نہیں ہے۔",
        "prevention": [
            "Maintain consistent drip irrigation at the base to avoid wetting leaves.",
            "Ensure 45-60 cm spacing between plants for optimal airflow and sunlight.",
            "Apply balanced N-P-K fertilizer and inspect weekly for early pest signs.",
            "Mulch soil around plants to prevent soil-borne fungal spores from splashing onto lower leaves."
        ],
        "prevention_ur": [
            "پودوں کی جڑوں میں قطرہ قطرہ پانی دیں تاکہ پتے خشک رہیں اور فنگس سے محفوظ رہیں۔",
            "ہوا اور دھوپ کی مناسب فراہمی کے لیے پودوں کے درمیان 45 سے 60 سینٹی میٹر کا فاصلہ رکھیں۔",
            "متوازن کھاد کا استعمال کریں اور کیڑوں کے حملے سے بچاؤ کے لیے ہفتہ وار معائنہ کریں۔",
            "مٹی پر ملچنگ کریں تاکہ بارش یا پانی سے مٹی کے جراثیم نچلے پتوں پر نہ لگیں۔"
        ],
        "treatment": "No chemical treatment needed. Continue good agricultural practices.",
        "treatment_ur": "کسی اسپرے کی ضرورت نہیں ہے۔ پودے کی عمومی دیکھ بھال جاری رکھیں۔",
        "weather_advisory": "Ideal growing temperature is 20°C - 28°C with moderate humidity (50-70%).",
        "weather_advisory_ur": "پودے کی بہترین نشوونما کے لیے 20 سے 28 ڈگری سینٹی گریڈ درجہ حرارت اور 50 سے 70 فیصد نمی موزوں ہے۔"
    },
    "Tomato___Early_blight": {
        "crop": "Tomato",
        "crop_ur": "ٹماٹر",
        "disease_name": "Early Blight",
        "disease_name_ur": "اگیتا جھلساؤ (ارلی بلائیٹ)",
        "scientific_name": "Alternaria solani",
        "status": "Diseased",
        "status_ur": "متاثرہ",
        "severity": "Moderate",
        "severity_ur": "درمیانہ",
        "symptoms": "Concentric dark brown rings resembling a 'bullseye' target on older leaves, surrounded by yellow chlorotic halos. Leaves eventually dry up and fall off.",
        "symptoms_ur": "نچلے اور پرانے پتوں پر گہرے بھورے دائرے دار دھبے (ہدف نما نشانات) بنتے ہیں جن کے گرد زرد ہالہ ہوتا ہے۔ متاثرہ پتے سوکھ کر گر جاتے ہیں۔",
        "prevention": [
            "Rotate crops annually; avoid planting nightshades (tomato, potato, eggplant) consecutively in the same soil.",
            "Prune bottom 12 inches of foliage to stop soil splashing.",
            "Sterilize pruning shears with 70% alcohol between cuts."
        ],
        "prevention_ur": [
            "ہر سال فصلیں بدل کر کاشت کریں؛ آلو، ٹماٹر اور بینگن کو مسلسل ایک ہی زمین پر نہ اگائیں۔",
            "زمین سے لگنے والے نچلے 12 انچ کے پتوں کو احتیاط سے کاٹ دیں تاکہ مٹی نہ اڑے۔",
            "پودوں کی کٹائی کے اوزاروں کو اسپرٹ یا جراثیم کش محلول سے صاف رکھیں۔"
        ],
        "treatment": "Spray organic neem oil solution or copper-based fungicide (Mancozeb or Chlorothalonil) every 7-10 days upon initial spotting.",
        "treatment_ur": "ابتدائی علامات پر نیم کے تیل کا محلول یا تانبے پر مبنی فنگس کش اسپرے (مینکوزیب / کلوروتھالونیل) 7 سے 10 دن کے وقفے سے کریں۔",
        "weather_advisory": "Spreads rapidly during warm (24°C - 29°C), humid weather following rain or heavy dew.",
        "weather_advisory_ur": "بارش کے بعد گرم اور مرطوب موسم (24 تا 29 ڈگری سینٹی گریڈ) میں یہ بیماری تیزی سے پھیلتی ہے۔"
    },
    "Tomato___Late_blight": {
        "crop": "Tomato",
        "crop_ur": "ٹماٹر",
        "disease_name": "Late Blight",
        "disease_name_ur": "پچھیتا جھلساؤ (لیٹ بلائیٹ)",
        "scientific_name": "Phytophthora infestans",
        "status": "Diseased",
        "status_ur": "شدید متاثرہ",
        "severity": "High",
        "severity_ur": "شدید خطرہ",
        "symptoms": "Large, irregular water-soaked pale green to dark brown oily lesions that expand rapidly. White cottony fungal growth develops on undersides of leaves during high humidity.",
        "symptoms_ur": "پتوں پر بڑے فاسد، پانی بھرے گہرے بھورے دھبے بنتے ہیں جو بہت تیزی سے پھیلتے ہیں۔ زیادہ نمی میں پتے کے پچھلے حصے پر سفید روئی نما پھپھوندی ظاہر ہوتی ہے۔",
        "prevention": [
            "Plant certified disease-resistant tomato varieties (e.g., Mountain Magic, Defiant).",
            "Immediately destroy and bag infected plants; never add them to compost heaps.",
            "Water early in the morning so sun dries the leaves quickly."
        ],
        "prevention_ur": [
            "بیماری کے خلاف قوتِ مدافعت رکھنے والی تصدیق شدہ اقسام کے بیج استعمال کریں۔",
            "شدید متاثرہ پودوں کو اکھاڑ کر زمین میں دبا دیں یا جلا دیں، کمپوسٹ میں نہ ڈالیں۔",
            "صبح سویرے پانی دیں تاکہ دن کی دھوپ میں پتے جلد خشک ہو جائیں۔"
        ],
        "treatment": "Emergency application of systemic fungicides containing Metalaxyl, Cymoxanil, or Copper Hydroxide is urgently required.",
        "treatment_ur": "فوری طور پر میٹالیکسائل یا کاپر ہائیڈرو آکسائیڈ پر مشتمل سسٹمک فنگسائڈ کا اسپرے لازمی کریں۔",
        "weather_advisory": "Extremely dangerous in cool, wet conditions (15°C - 22°C with humidity > 90%).",
        "weather_advisory_ur": "ٹھنڈے اور نمی والے موسم (15 سے 22 ڈگری سینٹی گریڈ اور 90 فیصد سے زیادہ نمی) میں یہ تباہ کن ثابت ہوتی ہے۔"
    },
    "Tomato___Leaf_Mold": {
        "crop": "Tomato",
        "crop_ur": "ٹماٹر",
        "disease_name": "Leaf Mold",
        "disease_name_ur": "پتوں کی پھپھوندی (لیف مولڈ)",
        "scientific_name": "Passalora fulva",
        "status": "Diseased",
        "status_ur": "متاثرہ",
        "severity": "Moderate",
        "severity_ur": "درمیانہ",
        "symptoms": "Pale green or yellowish spots on upper leaf surface. The underside displays a velvety olive-green to grayish-brown mold cover.",
        "symptoms_ur": "پتے کی اوپری سطح پر زردی مائل پیلے دھبے جبکہ نچلی سطح پر زیتونی سبز یا بھورے رنگ کی مخملی پھپھوندی جم جاتی ہے۔",
        "prevention": [
            "Increase greenhouse or field ventilation to keep relative humidity below 80%.",
            "Use drip irrigation exclusively and widen planting distance.",
            "Remove infected lower leaves to restrict spore transmission."
        ],
        "prevention_ur": [
            "گرین ہاؤس یا کھیت میں ہوا کی روانی کو بہتر بنائیں تاکہ ہوا میں نمی 80 فیصد سے کم رہے۔",
            "صرف ڈرپ اریگیشن کا استعمال کریں اور پودوں کے درمیان مناسب کشادگی رکھیں۔",
            "متاثرہ نچلے پتوں کو فوراً توڑ کر تلف کر دیں۔"
        ],
        "treatment": "Apply bio-fungicides like Bacillus amyloliquefaciens or sulfur-based organic sprays.",
        "treatment_ur": "بائیو فنگسائڈ یا سلفر پر مبنی اسپرے کا استعمال کریں۔",
        "weather_advisory": "Thrives in sheltered, stagnant air with high relative humidity (>85%) and 20°C - 25°C.",
        "weather_advisory_ur": "بند ہوا، گھٹن اور 85 فیصد سے زائد نمی کے حالات میں یہ بیماری تیزی سے بڑھتی ہے۔"
    },
    "Tomato___Bacterial_spot": {
        "crop": "Tomato",
        "crop_ur": "ٹماٹر",
        "disease_name": "Bacterial Spot",
        "disease_name_ur": "بیکٹیریل دھبے (بیکٹیریل اسپاٹ)",
        "scientific_name": "Xanthomonas campestris",
        "status": "Diseased",
        "status_ur": "متاثرہ",
        "severity": "Moderate",
        "severity_ur": "درمیانہ",
        "symptoms": "Small (1-3 mm), dark, greasy or translucent circular spots with yellow halos. Spots may coalesce, causing leaf scorch and defoliation.",
        "symptoms_ur": "پتوں پر چھوٹے چھوٹے (1 سے 3 ملی میٹر) گہرے چکنے گول دھبے جن کے گرد پیلی پٹی ہوتی ہے۔ شدید حملے میں پتا جھلس جاتا ہے۔",
        "prevention": [
            "Use hot water-treated pathogen-free seeds.",
            "Avoid overhead sprinkler irrigation that splashes bacteria.",
            "Never work among wet plants to avoid mechanical spreading."
        ],
        "prevention_ur": [
            "گرم پانی سے صاف اور تصدیق شدہ جراثیم سے پاک بیج کاشت کریں۔",
            "اوپر سے فوارہ نما پانی دینے سے پرہیز کریں جس سے بیکٹیریا اڑ کر پھیلتا ہے۔",
            "گیلے پودوں کے درمیان کام کرنے سے گریز کریں تاکہ ہاتھ یا کپڑوں سے جراثیم نہ پھیلیں۔"
        ],
        "treatment": "Spray fixed copper bactericide mixed with Mancozeb to enhance bacterial control.",
        "treatment_ur": "کاپر بیکٹیری سائیڈ کو مینکوزیب کے ساتھ ملا کر اسپرے کریں۔",
        "weather_advisory": "Favored by warm temperatures (24°C - 30°C) combined with high rainfall or heavy dew.",
        "weather_advisory_ur": "تیز بارش یا بھاری شبنم کے ساتھ گرم موسم (24 تا 30 ڈگری سینٹی گریڈ) میں بیکٹیریا تیزی سے پھیلتا ہے۔"
    },
    "Potato___healthy": {
        "crop": "Potato",
        "crop_ur": "آلو",
        "disease_name": "Healthy Foliage",
        "disease_name_ur": "صحت مند پودا",
        "scientific_name": "Solanum tuberosum",
        "status": "Healthy",
        "status_ur": "صحت مند",
        "severity": "None",
        "severity_ur": "کوئی بیماری نہیں",
        "symptoms": "Vibrant emerald green leaves, sturdy stems, upright growth, and absence of blight lesions or curling.",
        "symptoms_ur": "پتوں کا رنگ شاداب سبز ہے، تنے مضبوط اور سیدھے ہیں اور کسی قسم کا کوئی جھلساؤ یا مڑاؤ نہیں ہے۔",
        "prevention": [
            "Hill potatoes periodically to protect developing tubers from light and disease.",
            "Maintain soil pH between 5.5 and 6.5 for optimal tuber development.",
            "Monitor regularly for aphids and Colorado potato beetles."
        ],
        "prevention_ur": [
            "آلوؤں پر مٹی چڑھاتے رہیں تاکہ تیار ہونے والے آلو دھوپ اور بیماریوں سے بچے رہیں۔",
            "زمین کی پی ایچ (pH) 5.5 سے 6.5 کے درمیان رکھیں۔",
            "تیلے (ایفڈز) اور پتنگوں کے حملے پر نظر رکھیں۔"
        ],
        "treatment": "Continue preventive monitoring and proper water management.",
        "treatment_ur": "کسی اسپرے کی ضرورت نہیں، مناسب آبپاشی جاری رکھیں۔",
        "weather_advisory": "Best tuber bulking occurs between 16°C and 22°C.",
        "weather_advisory_ur": "آلو کے موٹے ہونے کے لیے 16 سے 22 ڈگری سینٹی گریڈ کا درجہ حرارت بہترین ہے۔"
    },
    "Potato___Early_blight": {
        "crop": "Potato",
        "crop_ur": "آلو",
        "disease_name": "Early Blight",
        "disease_name_ur": "آلو کا اگیتا جھلساؤ",
        "scientific_name": "Alternaria solani",
        "status": "Diseased",
        "status_ur": "متاثرہ",
        "severity": "Moderate",
        "severity_ur": "درمیانہ",
        "symptoms": "Dark brown, dry, leathery target spots with concentric rings bounded by leaf veins. Can lead to early defoliation and tuber size reduction.",
        "symptoms_ur": "پتوں پر گہرے بھورے، خشک اور چمڑے جیسے دائرہ نما دھبے بنتے ہیں جو رگوں کے اندر محدود رہتے ہیں۔ اس سے فصل وقت سے پہلے سوکھ سکتی ہے۔",
        "prevention": [
            "Plant certified high-vitality seed potatoes.",
            "Avoid nitrogen stress; balanced nitrogen reduces plant vulnerability.",
            "Destroy crop residues after harvest through deep tillage."
        ],
        "prevention_ur": [
            "تصدیق شدہ اور بیماری سے پاک بیج کے آلو استعمال کریں۔",
            "نائٹروجن کی کمی نہ ہونے دیں؛ متوازن کھاد پودے کی مدافعت بڑھاتی ہے۔",
            "فصل کی کٹائی کے بعد پودوں کی باقیات کو گہرا ہل چلا کر زمین میں دبا دیں۔"
        ],
        "treatment": "Apply protective contact fungicides (Azoxystrobin or Chlorothalonil) before row closure.",
        "treatment_ur": "ایزوکساسٹروبن یا کلوروتھالونیل فنگسائڈ کا حفاظتی اسپرے کریں۔",
        "weather_advisory": "Alternating wet and dry periods accelerate spore release.",
        "weather_advisory_ur": "خشک اور گیلے موسم کا متبادل آنا اس کے بیج (اسپورز) کو تیزی سے پھیلاتا ہے۔"
    },
    "Potato___Late_blight": {
        "crop": "Potato",
        "crop_ur": "آلو",
        "disease_name": "Late Blight",
        "disease_name_ur": "آلو کا پچھیتا جھلساؤ",
        "scientific_name": "Phytophthora infestans",
        "status": "Diseased",
        "status_ur": "شدید متاثرہ",
        "severity": "High",
        "severity_ur": "شدید خطرہ",
        "symptoms": "Large, dark water-soaked lesions appearing at leaf tips and edges that rapidly turn black and necrotic. White mildew appears in damp conditions, carrying an offensive odor.",
        "symptoms_ur": "پتوں کے کناروں پر کالے اور پانی سے بھیگے بڑے دھبے نمودار ہوتے ہیں جو پوری فصل کو چند دنوں میں جلا دیتے ہیں۔ گیلے موسم میں سفید پھپھوندی بنتی ہے اور ناگوار بو آتی ہے۔",
        "prevention": [
            "Eliminate cull piles (discarded infected potato piles) in the vicinity.",
            "Apply preventive protective spray during high humidity forecasts.",
            "Avoid harvesting tubers in wet soil to prevent tuber rot."
        ],
        "prevention_ur": [
            "کھیت کے اردگرد پھینکے گئے خراب آلوؤں کے ڈھیروں کو تلف کریں۔",
            "زیادہ بارش اور نمی کی پیشگوئی پر پہلے سے حفاظتی اسپرے کریں۔",
            "گیلی مٹی میں آلوؤں کی کھدائی نہ کریں تاکہ گودے کے گلنے کا خطرہ نہ ہو۔"
        ],
        "treatment": "Spray systemic fungicides immediately: Dimethomorph, Cymoxanil, or Propamocarb.",
        "treatment_ur": "فوری طور پر ڈائمتھومورف، سائیموکسانیل یا پروپاموکارب پر مشتمل فنگس کش دوا کا اسپرے کریں۔",
        "weather_advisory": "Alert! Temperature 10°C - 20°C with persistent wetness (>90% humidity) creates epidemic conditions.",
        "weather_advisory_ur": "خبردار! 10 سے 20 ڈگری درجہ حرارت اور مسلسل نمی (90 فیصد سے زیادہ) میں یہ وبا کی صورت اختیار کر لیتی ہے۔"
    },
    "Corn___healthy": {
        "crop": "Corn (Maize)",
        "crop_ur": "مکئی",
        "disease_name": "Healthy Corn Foliage",
        "disease_name_ur": "صحت مند مکئی",
        "scientific_name": "Zea mays",
        "status": "Healthy",
        "status_ur": "صحت مند",
        "severity": "None",
        "severity_ur": "کوئی بیماری نہیں",
        "symptoms": "Broad, arched emerald green leaves with prominent white midrib, free from spots, stripes, or powdery pustules.",
        "symptoms_ur": "چوڑے، گہرے سبز چمکدار پتے جن کے درمیان سفید رگ واضح ہے، کسی قسم کے زنگ، دھبے یا لکیروں سے پاک ہیں۔",
        "prevention": [
            "Ensure proper seedbed drainage to avoid waterlogging.",
            "Follow soil-test recommended nitrogen, phosphorus, and potassium applications.",
            "Maintain optimal row spacing (60-75 cm)."
        ],
        "prevention_ur": [
            "پانی کے نکاس کا بہترین انتظام رکھیں تاکہ پانی کھڑا نہ ہو۔",
            "مٹی کے ٹیسٹ کے مطابق نائٹروجن اور پوٹاش کی مناسب مقدار دیں۔",
            "قطاروں کے درمیان 60 سے 75 سینٹی میٹر کا فاصلہ رکھیں۔"
        ],
        "treatment": "No chemical intervention needed. Ensure regular field scouting.",
        "treatment_ur": "کسی اسپرے کی ضرورت نہیں۔ پودوں کی معمول کی دیکھ بھال کریں۔",
        "weather_advisory": "Flourishes in sunny weather between 22°C and 32°C.",
        "weather_advisory_ur": "22 سے 32 ڈگری سینٹی گریڈ دھوپ والے گرم موسم میں مکئی خوب پھلتی پھولتی ہے۔"
    },
    "Corn___Common_rust": {
        "crop": "Corn (Maize)",
        "crop_ur": "مکئی",
        "disease_name": "Common Rust",
        "disease_name_ur": "مکئی کا زنگ (رسٹ)",
        "scientific_name": "Puccinia sorghi",
        "status": "Diseased",
        "status_ur": "متاثرہ",
        "severity": "Moderate",
        "severity_ur": "درمیانہ",
        "symptoms": "Golden-brown to cinnamon-brown powdery pustules on both upper and lower leaf surfaces. Pustules rupture the epidermis, releasing powdery spores.",
        "symptoms_ur": "پتے کے اوپر اور نیچے دونوں طرف دارچینی یا اینٹ جیسے بھورے رنگ کے ابھرے ہوئے دانے (چھالے) بنتے ہیں جن میں پاؤڈر جیسا زنگ بھرا ہوتا ہے۔",
        "prevention": [
            "Plant resistant corn hybrid seed varieties.",
            "Plant early in the season to evade peak spore flight.",
            "Manage weeds in and around field edges."
        ],
        "prevention_ur": [
            "زنگ کے خلاف مزاحمت رکھنے والے ہائبرڈ بیج کاشت کریں۔",
            "موسم کے شروع میں جلدی بوائی کریں تاکہ زنگ کے جراثیم کے زور پکڑنے سے پہلے فصل تیار ہو جائے۔",
            "کھیت کے کناروں پر جڑی بوٹیاں تلف کریں۔"
        ],
        "treatment": "Apply triazole or strobilurin fungicides (Pyraclostrobin or Tebuconazole) if pustules reach upper leaves before tasseling.",
        "treatment_ur": "اگر پودے پر بور آنے سے پہلے اوپر والے پتوں تک زنگ پہنچے تو ٹیبوکونازول کا اسپرے کریں۔",
        "weather_advisory": "Favored by moderate temperatures (16°C - 24°C) with high relative humidity (>95%).",
        "weather_advisory_ur": "16 سے 24 ڈگری سینٹی گریڈ معتدل درجہ حرارت اور رات کو بھاری شبنم میں یہ بیماری بڑھتی ہے۔"
    },
    "Corn___Northern_Leaf_Blight": {
        "crop": "Corn (Maize)",
        "crop_ur": "مکئی",
        "disease_name": "Northern Leaf Blight",
        "disease_name_ur": "ناردرن لیف بلائیٹ",
        "scientific_name": "Exserohilum turcicum",
        "status": "Diseased",
        "status_ur": "متاثرہ",
        "severity": "High",
        "severity_ur": "شدید خطرہ",
        "symptoms": "Long, elliptical, cigar-shaped grayish-green to tan lesions (2.5 - 15 cm long). Lesions run parallel to leaf margins and can coalesce, causing canopy death.",
        "symptoms_ur": "پتوں پر سگار کی شکل کے لمبے (2.5 سے 15 سینٹی میٹر) بھورے سرمئی دھبے نمودار ہوتے ہیں جو رگوں کے متوازی پھیل کر پورے پتے کو سکھا دیتے ہیں۔",
        "prevention": [
            "Select resistant hybrids with Ht gene resistance.",
            "Practice 2-year crop rotation with non-host crops like soybean or wheat.",
            "Tillage to bury corn stubble from prior seasons."
        ],
        "prevention_ur": [
            "مدافعتی صلاحیت والے ہائبرڈ بیجوں کا انتخاب کریں۔",
            "مکئی کے بعد سویابین یا گندم کاشت کر کے فصلوں کے ردوبدل کا اصول اپنائیں۔",
            "پچھلی فصل کے مڈھوں کو مٹی میں دبا کر ضائع کریں۔"
        ],
        "treatment": "Foliar application of fungicides containing Azoxystrobin + Difenoconazole at first sign of lesions.",
        "treatment_ur": "علامات ظاہر ہوتے ہی ایزوکساسٹروبن اور ڈائیفینوکونازول پر مشتمل اسپرے کریں۔",
        "weather_advisory": "Moderate temperatures (18°C - 27°C) with extended leaf wetness (6-18 hours).",
        "weather_advisory_ur": "18 سے 27 ڈگری درجہ حرارت اور بارش یا شبنم سے پتوں کا مسلسل گیلا رہنا بیماری کو بڑھاتا ہے۔"
    },
    "Apple___healthy": {
        "crop": "Apple",
        "crop_ur": "سیب",
        "disease_name": "Healthy Apple Leaf",
        "disease_name_ur": "صحت مند سیب کا پتا",
        "scientific_name": "Malus domestica",
        "status": "Healthy",
        "status_ur": "صحت مند",
        "severity": "None",
        "severity_ur": "کوئی بیماری نہیں",
        "symptoms": "Serrated, lush green foliage with smooth surface, free from blisters, spots, or powdery coatings.",
        "symptoms_ur": "کنارے دار، گہرے سبز صحت مند پتے جن پر کسی قسم کا کوئی دھبہ یا چھالا موجود نہیں ہے۔",
        "prevention": [
            "Prune canopy during winter dormancy to maximize sunlight penetration.",
            "Apply lime sulfur dormant spray before bud break.",
            "Rake and shred fallen autumn leaves to disrupt overwintering fungal spores."
        ],
        "prevention_ur": [
            "سردیوں میں درختوں کی شاخ تراشی کریں تاکہ اندر تک دھوپ اور ہوا پہنچ سکے۔",
            "شاخوں کے پھوٹنے سے پہلے چونا اور گندھک (لائم سلفر) کا اسپرے کریں۔",
            "خزاں میں گرے ہوئے پتوں کو جمع کر کے ٹھکانے لگائیں تاکہ جراثیم سردی میں زندہ نہ رہیں۔"
        ],
        "treatment": "Maintain regular orchard scouting and nutritional balance.",
        "treatment_ur": "باغ کا باقاعدگی سے معائنہ کریں اور متوازن کھادیں دیں۔",
        "weather_advisory": "Thrives in temperate orchard climates with good solar radiation.",
        "weather_advisory_ur": "معتدل آب و ہوا اور اچھی دھوپ میں سیب کا باغ بہترین رہتا ہے۔"
    },
    "Apple___Apple_scab": {
        "crop": "Apple",
        "crop_ur": "سیب",
        "disease_name": "Apple Scab",
        "disease_name_ur": "سیب کی خارش (اسکیب)",
        "scientific_name": "Venturia inaequalis",
        "status": "Diseased",
        "status_ur": "متاثرہ",
        "severity": "Moderate",
        "severity_ur": "درمیانہ",
        "symptoms": "Olive-green, velvety spots with feathery margins on leaves that later become dark brown and corky. Causes distorted leaf curling and premature leaf drop.",
        "symptoms_ur": "پتوں پر زیتونی سبز مخملی دھبے بنتے ہیں جو بعد میں گہرے بھورے اور سخت ہو جاتے ہیں۔ اس سے پتے مڑ کر وقت سے پہلے جھڑ جاتے ہیں۔",
        "prevention": [
            "Plant scab-resistant cultivars (e.g., Enterprise, Liberty, Honeycrisp).",
            "Apply 5% urea spray on fallen leaves in autumn to accelerate leaf decomposition.",
            "Maintain open tree canopy with annual dormant pruning."
        ],
        "prevention_ur": [
            "اسکیب کے خلاف مزاحمت رکھنے والی سیب کی اقسام لگائیں۔",
            "خزاں میں زمین پر گرے پتوں پر یوریا کا ہلکا اسپرے کریں تاکہ پتے جلد گل جائیں۔",
            "سالانہ شاخ تراشی سے درختوں کو کھلا اور ہوادار رکھیں۔"
        ],
        "treatment": "Spray Captan, Mancozeb, or Myclobutanil beginning at green tip stage through petal fall.",
        "treatment_ur": "کپتان (Captan) یا مائیکلوبوٹانیل فنگس کش دوا کا اسپرے پھول کھلنے اور پنکھڑیاں گرنے کے دوران کریں۔",
        "weather_advisory": "Primary infection occurs during cool spring rains (12°C - 20°C with 9+ hours of wetness).",
        "weather_advisory_ur": "بہار کے موسم میں بارش اور 12 سے 20 ڈگری سینٹی گریڈ کے دوران اس بیماری کا حملہ شروع ہوتا ہے۔"
    },
    "Apple___Cedar_apple_rust": {
        "crop": "Apple",
        "crop_ur": "سیب",
        "disease_name": "Cedar Apple Rust",
        "disease_name_ur": "سیب کا نارنجی زنگ",
        "scientific_name": "Gymnosporangium juniperi-virginianae",
        "status": "Diseased",
        "status_ur": "متاثرہ",
        "severity": "Moderate",
        "severity_ur": "درمیانہ",
        "symptoms": "Bright yellow-orange or reddish spots on leaf tops that slowly produce tiny black specks. Later, tube-like fungal cups form on leaf undersides.",
        "symptoms_ur": "پتے کے اوپر چمکدار پیلے نارنجی دھبے بنتے ہیں جن کے درمیان سیاہ نقطے ہوتے ہیں۔ بعد میں پتے کے نیچے چھوٹی نلکی نما تھیلیاں بن جاتی ہیں۔",
        "prevention": [
            "Remove eastern red cedar or juniper trees within 1 to 2 miles of apple orchards.",
            "Inspect nearby juniper bushes for brownish-orange gelatinous rust galls in spring.",
            "Select resistant cultivars (e.g., Redfree, Priscilla)."
        ],
        "prevention_ur": [
            "سیب کے باغ کے آس پاس موجود صنوبر (جونیپر) کے جنگلی پودوں کو ہٹائیں۔",
            "بہار میں اردگرد کی جھاڑیوں پر نارنجی جیل نما گانٹھوں کا معائنہ کریں۔",
            "قوتِ مدافعت رکھنے والی سیب کی اقسام کاشت کریں۔"
        ],
        "treatment": "Apply Immunox (Myclobutanil) or sulfur sprays from pink bud through bloom.",
        "treatment_ur": "مائیکلوبوٹانیل یا سلفر فنگسائڈ کا اسپرے کلیوں کے کھلنے پر کریں۔",
        "weather_advisory": "Spreads in wet spring weather when warm rains trigger gelatinous spore release from galls.",
        "weather_advisory_ur": "بہار کی بارشوں اور گرم مرطوب موسم میں اس کے جراثیم ہوا کے ذریعے میلوں دور تک پھیلتے ہیں۔"
    },
    "Grape___healthy": {
        "crop": "Grape",
        "crop_ur": "انگور",
        "disease_name": "Healthy Grape Foliage",
        "disease_name_ur": "صحت مند انگور کی بیل",
        "scientific_name": "Vitis vinifera",
        "status": "Healthy",
        "status_ur": "صحت مند",
        "severity": "None",
        "severity_ur": "کوئی بیماری نہیں",
        "symptoms": "Broad lobed leaves with vibrant green coloration, firm texture, and clear venation without necrotic margins.",
        "symptoms_ur": "انگور کے خوبصورت کٹاؤ والے پتے گہرے سبز ہیں، رگیں صاف ہیں اور کوئی دھبہ یا سوکھا پن نہیں ہے۔",
        "prevention": [
            "Trellis vines properly to keep foliage elevated off the moist ground.",
            "Perform shoot positioning and leaf pulling around fruit clusters for sun exposure.",
            "Maintain soil drainage to prevent root rot."
        ],
        "prevention_ur": [
            "بیل کو لکڑی یا تاروں کے فریم پر چڑھائیں تاکہ پتے گیلی زمین سے اوپر رہیں۔",
            "انگور کے گچھوں کے اردگرد سے ضرورت سے زیادہ پتے ہٹائیں تاکہ دھوپ پہنچے۔",
            "پانی کے اچھے نکاس کا بندوبست کریں۔"
        ],
        "treatment": "Standard vineyard maintenance; no fungicide application needed.",
        "treatment_ur": "معمول کی نگہداشت رکھیں، کسی کیمیکل کی ضرورت نہیں۔",
        "weather_advisory": "Prefers warm days (24°C - 32°C) with dry canopies.",
        "weather_advisory_ur": "گرم دن (24 سے 32 ڈگری) اور خشک پتے انگور کی بیل کے لیے بہترین ہیں۔"
    },
    "Grape___Black_rot": {
        "crop": "Grape",
        "crop_ur": "انگور",
        "disease_name": "Black Rot",
        "disease_name_ur": "انگور کا سیاہ سڑاؤ (بلیک روٹ)",
        "scientific_name": "Guignardia bidwellii",
        "status": "Diseased",
        "status_ur": "متاثرہ",
        "severity": "High",
        "severity_ur": "شدید خطرہ",
        "symptoms": "Small, reddish-brown circular spots on leaves that enlarge with dark brown borders. Tiny black pycnidia (pimples) speckle the center. Can shrivel berries into black mummies.",
        "symptoms_ur": "پتوں پر چھوٹے سرخی مائل بھورے گول دھبے جن کے گرد سیاہ کنارہ ہوتا ہے اور درمیان میں سیاہ دانے دار نشانات ہوتے ہیں۔ یہ پھل کو سکھا کر کالا کر دیتا ہے۔",
        "prevention": [
            "Prune and destroy mummified dried fruit clusters and infected canes during winter.",
            "Canopy management: ensure good sun penetration and air drying.",
            "Keep grass and weeds mown low beneath vine trellises."
        ],
        "prevention_ur": [
            "سردیوں میں بیل پر لگے سوکھے اور سیاہ ہوئے دانوں کے گچھے کاٹ کر جلا دیں۔",
            "بیل کی شاخیں اس طرح پھیلائیں کہ دھوپ ہر پتے تک پہنچے۔",
            "بیل کے نیچے گھاس اور جڑی بوٹیوں کو کٹا ہوا رکھیں۔"
        ],
        "treatment": "Apply protective fungicides (Mancozeb, Captan, or Tebuconazole) from early shoot growth through 4 weeks post-bloom.",
        "treatment_ur": "شاخوں کے نکلنے سے لے کر پھول جھڑنے کے 4 ہفتے بعد تک مینکوزیب یا ٹیبوکونازول کا اسپرے کریں۔",
        "weather_advisory": "Requires 6-24 hours of continuous leaf wetness between 21°C and 27°C.",
        "weather_advisory_ur": "21 سے 27 ڈگری سینٹی گریڈ میں اگر پتے 6 سے 24 گھنٹے گیلے رہیں تو یہ بیماری حملہ کرتی ہے۔"
    }
}

# Helper to retrieve class info safely
def get_disease_info(class_key):
    return DISEASE_DATABASE.get(class_key, {
        "crop": "Plant",
        "crop_ur": "پودا",
        "disease_name": class_key.replace("___", " - ").replace("_", " "),
        "disease_name_ur": "پودے کی بیماری",
        "scientific_name": "Unknown",
        "status": "Unknown",
        "status_ur": "نامعلوم",
        "severity": "Moderate",
        "severity_ur": "درمیانہ",
        "symptoms": "Visible discoloration or lesion detected on leaf surface.",
        "symptoms_ur": "پتے پر داغ یا بیماری کے اثرات پائے گئے ہیں۔",
        "prevention": ["Isolate plant", "Consult local agricultural extension"],
        "prevention_ur": ["پودے کو الگ کریں", "ماہرین زراعت سے مشورہ کریں"],
        "treatment": "Apply broad-spectrum organic bio-fungicide.",
        "treatment_ur": "عام مقاصد کے لیے بائیو فنگسائڈ کا اسپرے کریں۔",
        "weather_advisory": "Monitor ambient humidity and leaf wetness.",
        "weather_advisory_ur": "ہوا کی نمی اور پتوں کی خشکی کا خیال رکھیں۔"
    })
