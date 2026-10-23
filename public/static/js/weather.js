/**
 * CropCare AI - Practical Agricultural Weather & Spray Window Integration
 * Integrates real-time Open-Meteo meteorological data with chemical spray safety thresholds.
 */

const WEATHER_CODE_DESCRIPTIONS = {
    0: { en: "Clear Sky", ur: "صاف آسمان", icon: "☀️" },
    1: { en: "Mainly Clear", ur: "زیادہ تر صاف", icon: "🌤️" },
    2: { en: "Partly Cloudy", ur: "جزوی ابر آلود", icon: "⛅" },
    3: { en: "Overcast", ur: "گہرے بادل", icon: "☁️" },
    45: { en: "Foggy / Mist", ur: "دھند", icon: "🌫️" },
    48: { en: "Dense Frost / Fog", ur: "شدید کہرا", icon: "🌫️" },
    51: { en: "Light Drizzle", ur: "ہلکی بوندا باندی", icon: "🌦️" },
    53: { en: "Moderate Drizzle", ur: "درمیانی پھوار", icon: "🌦️" },
    55: { en: "Dense Drizzle", ur: "تیز بوندا باندی", icon: "🌧️" },
    61: { en: "Slight Rain", ur: "ہلکی بارش", icon: "🌧️" },
    63: { en: "Moderate Rain", ur: "درمیانی بارش", icon: "🌧️" },
    65: { en: "Heavy Rain", ur: "تیز بارش", icon: "⛈️" },
    80: { en: "Rain Showers", ur: "بارش کی بوچھاڑ", icon: "🌧️" },
    82: { en: "Heavy Showers", ur: "تیز ژالہ باری / بوچھاڑ", icon: "⛈️" },
    95: { en: "Thunderstorm", ur: "طوفان و گرج چمک", icon: "⛈️" }
};

class WeatherManager {
    constructor() {
        this.cityName = "Lahore (Punjab)";
        this.lat = "31.5204";
        this.lon = "74.3587";
        this.cachedData = null;
    }

    async init() {
        const districtSelect = document.getElementById("district-select");
        if (districtSelect) {
            districtSelect.addEventListener("change", (e) => {
                const opt = e.target.selectedOptions[0];
                this.cityName = opt.text;
                this.lat = opt.getAttribute("data-lat") || "31.5204";
                this.lon = opt.getAttribute("data-lon") || "74.3587";
                this.fetchWeather();
            });
        }

        await this.fetchWeather();
    }

    async fetchWeather() {
        try {
            const url = `/api/weather?lat=${this.lat}&lon=${this.lon}&city=${encodeURIComponent(this.cityName)}`;
            const res = await fetch(url);
            const data = await res.json();

            if (!data.success) {
                console.warn("Weather API returned error:", data.error);
                return;
            }

            this.cachedData = data;
            this.render();
        } catch (err) {
            console.error("Failed to fetch weather data:", err);
        }
    }

    render() {
        if (!this.cachedData) return;
        const d = this.cachedData;
        const isUr = (typeof currentLang !== "undefined" && currentLang === "ur");
        const current = d.current || {};
        const daily = d.daily || {};

        const temp = Math.round(current.temperature_2m ?? 24);
        const humidity = Math.round(current.relative_humidity_2m ?? 50);
        const wind = Math.round(current.wind_speed_10m ?? 8);
        const precip = current.precipitation ?? 0;
        const apparent = Math.round(current.apparent_temperature ?? temp);
        const code = current.weather_code ?? 0;
        const condition = WEATHER_CODE_DESCRIPTIONS[code] || WEATHER_CODE_DESCRIPTIONS[0];

        // 1. Update Dashboard Summary Bar
        const dashTemp = document.getElementById("dash-temp");
        if (dashTemp) dashTemp.textContent = `${temp}°C`;

        const dashCond = document.getElementById("dash-weather-condition");
        if (dashCond) dashCond.textContent = isUr ? condition.ur : condition.en;

        const dashLoc = document.getElementById("dash-location-text");
        if (dashLoc) dashLoc.textContent = `${this.cityName} • Real-time Open-Meteo`;

        const dashWind = document.getElementById("dash-wind");
        if (dashWind) dashWind.textContent = `${wind} km/h`;

        const heroWindDisplay = document.getElementById("hero-wind-display");
        if (heroWindDisplay) heroWindDisplay.textContent = `${wind} km/h`;
        if (window.CropCare3D && typeof window.CropCare3D.setHeroWind === "function") {
            if (wind < 5) window.CropCare3D.setHeroWind("calm");
            else if (wind > 15) window.CropCare3D.setHeroWind("field");
            else window.CropCare3D.setHeroWind("gentle");
        }

        const dashHum = document.getElementById("dash-humidity");
        if (dashHum) dashHum.textContent = `${humidity}%`;

        const dashHumRisk = document.getElementById("dash-humidity-risk");
        if (dashHumRisk) {
            dashHumRisk.textContent = isUr ? (d.risk_level_ur || d.risk_level) : d.risk_level;
        }

        const dashSprayBadge = document.getElementById("dash-spray-badge");
        if (dashSprayBadge) {
            dashSprayBadge.textContent = isUr ? (d.spray_status_ur || d.spray_status) : d.spray_status;
            dashSprayBadge.style.backgroundColor = (wind > 20 || precip > 0.5) ? "var(--alert-red)" : (temp > 36) ? "var(--alert-amber)" : "var(--primary-700)";
        }

        const dashSprayAdv = document.getElementById("dash-spray-advisory");
        if (dashSprayAdv) {
            dashSprayAdv.textContent = isUr ? d.spray_advisory_ur : d.spray_advisory;
        }

        // Render Alerts on Dashboard if present
        const alertBox = document.getElementById("dash-alert-container");
        if (alertBox) {
            if (d.alerts && d.alerts.length > 0) {
                alertBox.innerHTML = d.alerts.map(a => `
                    <div class="ag-alert-box alert-warning">
                        <span style="font-size: 1.2rem;">⚠️</span>
                        <div><strong>${isUr ? "موسمی انتباہ:" : "Weather Alert:"}</strong> ${isUr ? a.text_ur : a.text}</div>
                    </div>
                `).join("");
            } else {
                alertBox.innerHTML = "";
            }
        }

        // 2. Update Weather Tab Full Details
        const wTemp = document.getElementById("w-full-temp");
        if (wTemp) wTemp.textContent = `${temp}°C`;

        const wFeels = document.getElementById("w-full-feels");
        if (wFeels) wFeels.textContent = isUr ? `محسوس: ${apparent}°C` : `Feels like ${apparent}°C`;

        const wHum = document.getElementById("w-full-hum");
        if (wHum) wHum.textContent = `${humidity}%`;

        const wWind = document.getElementById("w-full-wind");
        if (wWind) wWind.textContent = `${wind} km/h`;

        const wPrecip = document.getElementById("w-full-precip");
        if (wPrecip) wPrecip.textContent = `${precip} mm`;

        // Spray Card
        const sprayStatus = document.getElementById("spray-eval-status");
        if (sprayStatus) sprayStatus.textContent = isUr ? d.spray_status_ur : d.spray_status;

        const sprayDesc = document.getElementById("spray-eval-desc");
        if (sprayDesc) sprayDesc.textContent = isUr ? d.spray_advisory_ur : d.spray_advisory;

        const sprayCard = document.getElementById("spray-evaluation-card");
        if (sprayCard && d.spray_color) {
            sprayCard.className = `ag-alert-box ${wind > 20 || precip > 0.5 ? "alert-danger" : temp > 36 ? "alert-warning" : "alert-success"}`;
        }

        // Fungal Disease Risk Card
        const riskStatus = document.getElementById("disease-risk-status");
        if (riskStatus) riskStatus.textContent = isUr ? d.risk_level_ur : d.risk_level;

        const riskDesc = document.getElementById("disease-risk-desc");
        if (riskDesc) riskDesc.textContent = isUr ? d.disease_advisory_ur : d.disease_advisory;

        const riskCard = document.getElementById("disease-risk-card");
        if (riskCard) {
            riskCard.className = `ag-alert-box ${d.risk_level.includes("High") ? "alert-danger" : d.risk_level.includes("Moderate") ? "alert-warning" : "alert-info"}`;
        }

        // 3. Render 5-Day Forecast Grid
        const forecastContainer = document.getElementById("forecast-cards-container");
        if (forecastContainer && daily.time) {
            const days = daily.time.slice(0, 5);
            const maxTemps = daily.temperature_2m_max || [];
            const minTemps = daily.temperature_2m_min || [];
            const rainSums = daily.precipitation_sum || [];
            const codes = daily.weather_code || [];

            forecastContainer.innerHTML = days.map((dateStr, i) => {
                const dateObj = new Date(dateStr);
                const dayName = isUr
                    ? dateObj.toLocaleDateString("ur-PK", { weekday: "short" })
                    : dateObj.toLocaleDateString("en-US", { weekday: "short" });
                const formattedDate = dateObj.toLocaleDateString("en-US", { month: "short", day: "numeric" });
                const cCode = codes[i] ?? 0;
                const cDesc = WEATHER_CODE_DESCRIPTIONS[cCode] || WEATHER_CODE_DESCRIPTIONS[0];
                const maxT = Math.round(maxTemps[i] ?? 25);
                const minT = Math.round(minTemps[i] ?? 15);
                const rain = (rainSums[i] ?? 0).toFixed(1);

                return `
                    <div class="forecast-day-card">
                        <div class="forecast-day-date">${dayName}, ${formattedDate}</div>
                        <div class="forecast-day-icon">${cDesc.icon}</div>
                        <div class="forecast-day-temp">${maxT}° / ${minT}°C</div>
                        <div class="forecast-day-rain">💧 ${rain} mm</div>
                    </div>
                `;
            }).join("");
        }
    }
}

const weatherManager = new WeatherManager();
window.weatherManager = weatherManager;
window.renderActiveWeather = () => weatherManager.render();

document.addEventListener("DOMContentLoaded", () => {
    weatherManager.init();
});
