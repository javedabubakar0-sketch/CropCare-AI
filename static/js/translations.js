/**
 * CropCare AI - English and Urdu Translations Dictionary
 * Accurate agricultural vocabulary for Pakistani farmers and students.
 */

const translations = {
    en: {
        app_title: "CropCare AI",
        tagline: "Agricultural Decision Support & Plant Health",
        status_online: "AI Active (16 Classes)",
        status_offline: "AI Model Offline",
        lang_btn: "اردو میں دیکھیں",
        btn_viva_guide: "Viva Guide",

        // Navigation Tabs
        tab_dashboard: "Overview",
        tab_scanner: "Crop Diagnosis",
        tab_crops: "My Fields",
        tab_tasks: "Farm Calendar",
        tab_weather: "Weather & Irrigation",
        tab_guides: "Market & Knowledge",
        tab_records: "Farm Records",

        // Dashboard
        dash_weather_title: "Farm Conditions",
        spray_window_label: "Spray Safety Window",
        dash_crops_title: "Active Farm Crops",
        btn_add_field: "Add Field",
        empty_crops_text: "No farm fields registered yet. Click 'Add Field' to record your crop acreage and sowing dates.",
        btn_add_first_field: "Register First Field",

        dash_tasks_title: "Due Farm Tasks",
        btn_add_task: "Add Task",
        empty_tasks_text: "No pending farm operations due today.",

        // 3D Visualizations
        hero_3d_title: "Wheat (Triticum aestivum) — 3D Botanical Specimen",
        hero_3d_desc: "Natural foliar geometry, organic soil clod, and wind sway simulation.",
        hero_stage_tillering: "Tillering (Young)",
        hero_stage_heading: "Heading (Mature Ear)",
        hero_wind_label: "Wind Breeze:",
        hero_wind_gentle: "Gentle (8 km/h)",
        hero_wind_field: "Field (18 km/h)",
        hero_wind_calm: "Calm",
        hero_reset_view: "Reset View",
        field_3d_title: "Interactive 3D Crop Field Parcel",
        field_3d_desc: "Virtual miniature plot mapped to your registered SQLite farm records. Click any row to inspect plot details.",
        scanner_3d_title: "3D Foliage Specimen & Optical Scanner",
        scanner_3d_disclaimer: "Illustrative 3D Botanical Model — Diagnostic inference is calculated by the Scikit-Learn model directly from your uploaded leaf photo.",

        // Scanner
        scanner_title: "Plant Foliage Diagnostic Chamber",
        label_crop_hint: "Select Plant Type (Optional):",
        dropzone_title: "Select or Photograph Leaf",
        dropzone_desc: "Drag and drop leaf photo here, or browse files on your device.",
        btn_choose_image: "Choose Image",
        btn_run_model: "Run Local Model",
        btn_clear_photo: "Clear",
        sample_tray_title: "Or Test with Built-in Presentation Samples:",
        evaluating_text: "Analyzing Botanical Features Locally...",
        evaluating_sub: "Extracting 36 color moments, GLI vegetation index, and lesion textures",
        result_empty_title: "No Foliage Scanned Yet",
        result_empty_desc: "Select a leaf image or click one of the presentation sample leaves to generate an instant diagnosis.",
        conf_label: "Model Confidence",
        diag_symptoms_title: "Foliar Symptoms",
        diag_prevention_title: "Agronomic & Preventive Measures",
        diag_treatment_title: "Targeted Treatment / Fungicide",
        diag_weather_title: "Weather Susceptibility",
        btn_print_report: "Print Report",
        expert_disclaimer: "Disclaimer: CropCare AI runs a local machine-learning classifier for botanical decision support. Always cross-verify critical field infections with a local agricultural extension officer.",

        // Crops Management
        crops_page_title: "Field & Crop Management",
        btn_register_field: "Register New Field",
        th_crop: "Crop Name",
        th_field: "Field Name",
        th_area: "Area (Acres)",
        th_variety: "Variety",
        th_sowing: "Sowing Date",
        th_soil: "Soil Texture",
        th_actions: "Action",

        // Tasks Page
        tasks_page_title: "Crop Calendar & Farm Operations",

        // Weather Page
        weather_page_title: "Field Weather & Chemical Spray Window",
        w_temp_label: "Temperature",
        w_hum_label: "Relative Humidity",
        w_wind_label: "Wind Velocity",
        w_precip_label: "Precipitation",
        forecast_title: "5-Day Agricultural Forecast",

        // Irrigation Helper
        irrigation_title: "Cautious Irrigation Estimation Helper",
        irri_crop: "Select Crop:",
        irri_soil: "Soil Texture:",
        irri_sowing: "Sowing Date:",
        btn_calc_irrigation: "Calculate Irrigation Advisory",

        // Guides & Mandi
        mandi_title: "Wholesale Mandi Benchmarks",
        guides_title: "Field Practical Guides",

        // Records
        records_title: "Saved Diagnostic Records (Local SQLite)",
        btn_clear_history: "Clear All Records",
        th_date: "Date",
        th_diagnosis: "Diagnosis",
        th_conf: "Confidence",
        th_status: "Status",

        // Modals
        modal_add_crop_title: "Register Farm Field",
        lbl_crop_name: "Crop Type:",
        lbl_field_name: "Field Name / Identifier:",
        lbl_area: "Area (Acres):",
        lbl_variety: "Seed Variety:",
        lbl_sowing_date: "Sowing Date:",
        lbl_soil_type: "Soil Type:",
        lbl_notes: "Field Notes:",
        btn_cancel: "Cancel",
        btn_save_field: "Save Field",

        modal_add_task_title: "Add Farm Task",
        lbl_task_crop: "Target Crop / Field:",
        lbl_task_type: "Operation Type:",
        lbl_task_title: "Task Description:",
        lbl_task_due: "Scheduled Due Date:",
        btn_save_task: "Add Task",

        modal_scan_title: "Diagnostic Scan Record",
        btn_close: "Close",
        viva_title: "CropCare AI — University Presentation & Viva Guide"
    },

    ur: {
        app_title: "کراپ کیئر اے آئی",
        tagline: "فصلوں کی تشخیص اور زرعی مشاورتی نظام",
        status_online: "ماڈل فعال ہے (16 اقسام)",
        status_offline: "ماڈل آف لائن ہے",
        lang_btn: "View in English",
        btn_viva_guide: "پریزنٹیشن و وائیوا",

        // Navigation Tabs
        tab_dashboard: "جائزہ و خلاصہ",
        tab_scanner: "فصل کی تشخیص",
        tab_crops: "میرے کھیت",
        tab_tasks: "زرعی کیلنڈر",
        tab_weather: "موسم و آبپاشی",
        tab_guides: "مارکیٹ و رہنمائی",
        tab_records: "فارم ریکارڈز",

        // Dashboard
        dash_weather_title: "کھیت کے موسمی حالات",
        spray_window_label: "اسپرے کی محفوظ ونڈو",
        dash_crops_title: "زیرِ کاشت فصلیں",
        btn_add_field: "نیا کھیت درج کریں",
        empty_crops_text: "ابھی تک کوئی کھیت درج نہیں ہے۔ اپنی فصلوں، بوائی اور رقبے کا ریکارڈ رکھنے کے لیے 'نیا کھیت درج کریں' پر کلک کریں۔",
        btn_add_first_field: "پہلا کھیت درج کریں",

        dash_tasks_title: "آج کے زرعی کام",
        btn_add_task: "نیا کام شامل کریں",
        empty_tasks_text: "آج کے لیے کوئی کام باقی نہیں ہے۔",

        // 3D Visualizations
        hero_3d_title: "گندم (قومی اناج) — 3D نباتاتی نمونہ",
        hero_3d_desc: "پتوں کی قدرتی ساخت، زرخیز مٹی کا ڈھیلا اور ہوا کے جھونکوں کا زندہ مشاہدہ۔",
        hero_stage_tillering: "شاخیں نکلنا (چھوٹا پودا)",
        hero_stage_heading: "بالی کا مرحلہ (پختہ اناج)",
        hero_wind_label: "ہوا کی رفتار:",
        hero_wind_gentle: "ہلکی ہوا (8 کلومیٹر)",
        hero_wind_field: "کھیت کی تیز ہوا (18 کلومیٹر)",
        hero_wind_calm: "ساکن",
        hero_reset_view: "زاویہ اصل پر لائیں",
        field_3d_title: "متحرک 3D زرعی رقبہ اور کیاریاں",
        field_3d_desc: "آپ کے رجسٹرڈ کھیتوں کا متحرک 3D نقشہ۔ کسی بھی کیاری پر کلک کر کے تفصیلات دیکھیں۔",
        scanner_3d_title: "3D پتے کا نباتاتی نمونہ اور اسکیننگ",
        scanner_3d_disclaimer: "وضاحتی 3D نمونہ — بیماری کی تشخیص اور تخمینہ آپ کی اپ لوڈ کردہ اصل تصویر سے تیار کیا جاتا ہے۔",

        // Scanner
        scanner_title: "پتوں کے معائنے کا خاکہ",
        label_crop_hint: "پودے کی قسم منتخب کریں (اختیاری):",
        dropzone_title: "پتے کی تصویر منتخب کریں یا کھینچیں",
        dropzone_desc: "تصویر یہاں ڈریگ کریں یا اپنے موبائل/کمپیوٹر سے منتخب کریں۔",
        btn_choose_image: "تصویر منتخب کریں",
        btn_run_model: "تشخیص شروع کریں",
        btn_clear_photo: "صاف کریں",
        sample_tray_title: "یا پریزنٹیشن کے لیے نمونہ پتوں پر ٹیسٹ کریں:",
        evaluating_text: "پتے کی نباتاتی علامات کا معائنہ جاری ہے...",
        evaluating_sub: "کلوروفل، رنگت، اور دھبوں کا 36 خصوصیات پر تجزیہ",
        result_empty_title: "ابھی تک کوئی پتا اسکین نہیں کیا گیا",
        result_empty_desc: "تصویر اپ لوڈ کریں یا دیے گئے نمونہ پتوں پر کلک کر کے فوری تشخیصی رپورٹ دیکھیں۔",
        conf_label: "ماڈل کا اعتماد",
        diag_symptoms_title: "بیماری کی علامات",
        diag_prevention_title: "حفاظتی و تدارکی تدابیر",
        diag_treatment_title: "مجوزہ علاج و فنگس کش اسپرے",
        diag_weather_title: "موسمی حساسیت",
        btn_print_report: "رپورٹ پرنٹ کریں",
        expert_disclaimer: "انتباہ: کراپ کیئر اے آئی کسانوں کی مدد کے لیے ایک خودکار تجزیاتی نظام ہے۔ تصدیق کے لیے محکمہ زراعت کے فیلڈ اسسٹنٹ سے ضرور رہنمائی لیں۔",

        // Crops Management
        crops_page_title: "کھیت اور فصلوں کا انتظام",
        btn_register_field: "نیا کھیت درج کریں",
        th_crop: "فصل کا نام",
        th_field: "کھیت کا نام / نمبر",
        th_area: "رقبہ (ایکڑ)",
        th_variety: "بیج کی ورائٹی",
        th_sowing: "تاریخِ کاشت",
        th_soil: "مٹی کی ساخت",
        th_actions: "کارروائی",

        // Tasks Page
        tasks_page_title: "فصل کا کیلنڈر اور فیلڈ آپریشنز",

        // Weather Page
        weather_page_title: "موسم اور زرعی اسپرے کا موزوں وقت",
        w_temp_label: "درجہ حرارت",
        w_hum_label: "ہوا میں نمی",
        w_wind_label: "ہوا کی رفتار",
        w_precip_label: "بارش کا امکان",
        forecast_title: "اگلے 5 دن کی زرعی پیشگوئی",

        // Irrigation Helper
        irrigation_title: "آبپاشی کا محتاط مشیر",
        irri_crop: "فصل منتخب کریں:",
        irri_soil: "مٹی کی ساخت:",
        irri_sowing: "تاریخِ کاشت:",
        btn_calc_irrigation: "آبپاشی کا تخمینہ لگائیں",

        // Guides & Mandi
        mandi_title: "مرکزی منڈیوں کے ہول سیل ریٹس",
        guides_title: "کھیت کے عملی رہنماء اصول",

        // Records
        records_title: "محفوظ شدہ تشخیصی ریکارڈز (لوکل ڈیٹا بیس)",
        btn_clear_history: "تمام ریکارڈز صاف کریں",
        th_date: "تاریخ",
        th_diagnosis: "تشخیص",
        th_conf: "اعتماد",
        th_status: "کیفیت",

        // Modals
        modal_add_crop_title: "نئے کھیت کا اندراج",
        lbl_crop_name: "فصل کی قسم:",
        lbl_field_name: "کھیت کا نام یا پہچان:",
        lbl_area: "رقبہ (ایکڑ):",
        lbl_variety: "بیج کی قسم (ورائٹی):",
        lbl_sowing_date: "تاریخِ کاشت:",
        lbl_soil_type: "مٹی کی قسم:",
        lbl_notes: "اضافی نوٹس:",
        btn_cancel: "منسوخ کریں",
        btn_save_field: "کھیت محفوظ کریں",

        modal_add_task_title: "نیا زرعی کام شامل کریں",
        lbl_task_crop: "متعلقہ فصل یا کھیت:",
        lbl_task_type: "کام کی قسم:",
        lbl_task_title: "کام کی تفصیل:",
        lbl_task_due: "مقررہ تاریخ:",
        btn_save_task: "کام محفوظ کریں",

        modal_scan_title: "پتے کا تشخیصی ریکارڈ",
        btn_close: "بند کریں",
        viva_title: "کراپ کیئر اے آئی — یونیورسٹی پریزنٹیشن و وائیوا گائیڈ"
    }
};

let currentLang = localStorage.getItem("cropcare_lang") || "en";

function setLanguage(lang) {
    currentLang = lang;
    localStorage.setItem("cropcare_lang", lang);

    const html = document.documentElement;
    const isUrdu = lang === "ur";

    if (isUrdu) {
        html.setAttribute("dir", "rtl");
        html.setAttribute("lang", "ur");
        document.body.classList.add("lang-ur");
    } else {
        html.setAttribute("dir", "ltr");
        html.setAttribute("lang", "en");
        document.body.classList.remove("lang-ur");
    }

    // Update text elements with data-i18n attribute
    document.querySelectorAll("[data-i18n]").forEach(el => {
        const key = el.getAttribute("data-i18n");
        if (translations[lang] && translations[lang][key]) {
            el.textContent = translations[lang][key];
        }
    });

    // Update Language Toggle Button text
    const langBtnText = document.getElementById("lang-btn-text");
    if (langBtnText) {
        langBtnText.textContent = isUrdu ? "View in English" : "اردو میں دیکھیں";
    }

    // Refresh dynamic content in current language
    if (window.renderActiveWeather) {
        window.renderActiveWeather();
    }
    if (window.renderGuidesAndMandi) {
        window.renderGuidesAndMandi();
    }
}

function toggleLanguage() {
    setLanguage(currentLang === "en" ? "ur" : "en");
}
