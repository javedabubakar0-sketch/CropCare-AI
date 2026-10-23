/**
 * CropCare AI - Professional Agricultural Frontend Controller
 * Complete interactive logic for:
 * - Tab navigation and quick actions
 * - Real local ML leaf disease scanning & presentation sample leaves
 * - Field & Crop registration (SQLite)
 * - Farm Calendar & Task Checklist (SQLite)
 * - Practical Irrigation Estimation Helper
 * - Mandi Wholesale Benchmark Rates & Field Guides
 * - Scan history archive & PDF/print export
 */

let selectedScanFile = null;
let lastScanResult = null;
let currentTaskFilter = "all";

document.addEventListener("DOMContentLoaded", () => {
    initLanguageSetup();
    initNavigationTabs();
    initScanner();
    initCrops();
    initTasks();
    initIrrigation();
    initGuidesAndMandi();
    initRecords();
    initModals();

    // Set default sowing date to today
    const sowingInp = document.getElementById("inp-sowing-date");
    if (sowingInp) sowingInp.value = new Date().toISOString().split("T")[0];

    const irriSowingInp = document.getElementById("irri-sowing-date");
    if (irriSowingInp) irriSowingInp.value = new Date(Date.now() - 30 * 86400000).toISOString().split("T")[0];

    const taskDueInp = document.getElementById("inp-task-due");
    if (taskDueInp) taskDueInp.value = new Date(Date.now() + 7 * 86400000).toISOString().split("T")[0];
});

// -------------------------------------------------------------
// 1. Language Setup
// -------------------------------------------------------------
function initLanguageSetup() {
    const saved = localStorage.getItem("cropcare_lang") || "en";
    setLanguage(saved);

    const toggleBtn = document.getElementById("btn-toggle-lang");
    if (toggleBtn) {
        toggleBtn.addEventListener("click", () => {
            toggleLanguage();
        });
    }
}

// -------------------------------------------------------------
// 2. Navigation Tabs & Quick Actions
// -------------------------------------------------------------
function initNavigationTabs() {
    const tabButtons = document.querySelectorAll(".nav-tab-btn");
    tabButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const targetId = btn.getAttribute("data-tab");
            switchTab(targetId);
        });
    });

    // Quick action jumps from dashboard
    document.querySelectorAll("[data-jump-tab]").forEach(el => {
        el.addEventListener("click", () => {
            const target = el.getAttribute("data-jump-tab");
            switchTab(target);
        });
    });

    // Check URL parameters or hash on load
    const urlParams = new URLSearchParams(window.location.search);
    const initialTab = urlParams.get("tab") || (window.location.hash ? window.location.hash.replace("#", "") : null);
    if (initialTab && document.getElementById(initialTab)) {
        switchTab(initialTab);
    }
    // Mobile Sidebar Drawer Toggle
    const hamburgerBtn = document.getElementById("btn-hamburger");
    const sidebar = document.getElementById("app-sidebar");
    const backdrop = document.getElementById("sidebar-backdrop");
    const sidebarClose = document.getElementById("sidebar-close-btn");

    if (hamburgerBtn && sidebar) {
        hamburgerBtn.addEventListener("click", () => {
            sidebar.classList.add("open");
            if (backdrop) backdrop.classList.add("open");
        });
    }

    if (sidebarClose && sidebar) {
        sidebarClose.addEventListener("click", () => {
            sidebar.classList.remove("open");
            if (backdrop) backdrop.classList.remove("open");
        });
    }

    if (backdrop && sidebar) {
        backdrop.addEventListener("click", () => {
            sidebar.classList.remove("open");
            backdrop.classList.remove("open");
        });
    }

    // Sidebar Viva Button
    const sidebarVivaBtn = document.getElementById("btn-sidebar-viva");
    if (sidebarVivaBtn) {
        sidebarVivaBtn.addEventListener("click", () => {
            openModal("modal-viva-guide");
        });
    }
}

function switchTab(tabId) {
    document.querySelectorAll(".nav-tab-btn").forEach(b => {
        b.classList.toggle("active", b.getAttribute("data-tab") === tabId);
    });

    document.querySelectorAll(".tab-panel").forEach(p => {
        p.classList.toggle("active", p.id === tabId);
    });

    // Close mobile drawer if open
    const sidebar = document.getElementById("app-sidebar");
    const backdrop = document.getElementById("sidebar-backdrop");
    if (sidebar) sidebar.classList.remove("open");
    if (backdrop) backdrop.classList.remove("open");

    // Update topbar title
    const activeBtn = document.querySelector(`.nav-tab-btn[data-tab="${tabId}"]`);
    const pageTitle = document.getElementById("topbar-page-title");
    if (activeBtn && pageTitle) {
        const span = activeBtn.querySelector("span[data-i18n]") || activeBtn.querySelector("span");
        if (span) pageTitle.textContent = span.textContent;
    }

    // Trigger tab-specific refreshes
    if (tabId === "tab-crops") loadCrops();
    if (tabId === "tab-tasks") loadTasks();
    if (tabId === "tab-records") loadRecords();
    if (tabId === "tab-guides") loadGuidesAndMandi();

    window.scrollTo({ top: 0, behavior: "smooth" });
}

// -------------------------------------------------------------
// 3. Leaf Disease Scanner (Central Feature)
// -------------------------------------------------------------
function initScanner() {
    const dropZone = document.getElementById("drop-zone");
    const fileInput = document.getElementById("file-input");
    const browseBtn = document.getElementById("btn-browse-file");
    const runBtn = document.getElementById("btn-run-scan");
    const resetBtn = document.getElementById("btn-reset-scan");
    const printBtn = document.getElementById("btn-print-report");

    if (!dropZone || !fileInput) return;

    browseBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        fileInput.click();
    });

    dropZone.addEventListener("click", (e) => {
        if (!selectedScanFile) fileInput.click();
    });

    fileInput.addEventListener("change", (e) => {
        if (e.target.files && e.target.files[0]) {
            handleSelectedFile(e.target.files[0]);
        }
    });

    // Drag and Drop
    ["dragenter", "dragover"].forEach(name => {
        dropZone.addEventListener(name, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.add("dragover");
        });
    });

    ["dragleave", "drop"].forEach(name => {
        dropZone.addEventListener(name, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.remove("dragover");
        });
    });

    dropZone.addEventListener("drop", (e) => {
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleSelectedFile(e.dataTransfer.files[0]);
        }
    });

    runBtn.addEventListener("click", () => {
        if (selectedScanFile) {
            uploadAndScanLeaf(selectedScanFile);
        }
    });

    resetBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        resetScanner();
    });

    if (printBtn) {
        printBtn.addEventListener("click", () => {
            window.print();
        });
    }

    // Presentation Sample Leaf Buttons
    document.querySelectorAll(".btn-sample-chip").forEach(btn => {
        btn.addEventListener("click", () => {
            const sampleName = btn.getAttribute("data-sample");
            scanSampleLeaf(sampleName);
        });
    });
}

function handleSelectedFile(file) {
    if (!file.type.startsWith("image/")) {
        alert("Please select a valid image file (JPG, PNG, or WEBP).");
        return;
    }

    selectedScanFile = file;
    const reader = new FileReader();
    reader.onload = (e) => {
        const previewImg = document.getElementById("preview-image");
        const filename = document.getElementById("preview-filename");
        const filesize = document.getElementById("preview-filesize");
        const uploadPrompt = document.getElementById("upload-prompt");
        const previewBox = document.getElementById("preview-box");

        previewImg.src = e.target.result;
        filename.textContent = file.name;
        filesize.textContent = `${Math.round(file.size / 1024)} KB`;

        uploadPrompt.style.display = "none";
        previewBox.classList.add("active");
    };
    reader.readAsDataURL(file);
}

function resetScanner() {
    selectedScanFile = null;
    const fileInput = document.getElementById("file-input");
    if (fileInput) fileInput.value = "";

    const uploadPrompt = document.getElementById("upload-prompt");
    const previewBox = document.getElementById("preview-box");
    if (uploadPrompt) uploadPrompt.style.display = "block";
    if (previewBox) previewBox.classList.remove("active");
}

async function uploadAndScanLeaf(file) {
    showScanLoading(true);
    if (window.CropCare3D && typeof window.CropCare3D.triggerScannerStart === "function") {
        window.CropCare3D.triggerScannerStart();
    }

    const formData = new FormData();
    formData.append("leaf_image", file);

    const cropHint = document.getElementById("scan-crop-select").value;
    if (cropHint && cropHint !== "auto") {
        formData.append("crop_hint", cropHint);
    }

    try {
        const res = await fetch("/api/scan", {
            method: "POST",
            body: formData
        });
        const result = await res.json();
        showScanLoading(false);

        if (!res.ok || !result.success) {
            handleScanError(result);
            return;
        }

        renderDiagnosticResult(result);
        loadRecords();
        loadStats();
    } catch (err) {
        showScanLoading(false);
        alert("Error connecting to CropCare AI local model server: " + err.message);
    }
}

async function scanSampleLeaf(sampleName) {
    showScanLoading(true);
    if (window.CropCare3D && typeof window.CropCare3D.triggerScannerStart === "function") {
        window.CropCare3D.triggerScannerStart();
    }

    try {
        const res = await fetch("/api/scan-sample", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ sample_name: sampleName })
        });
        const result = await res.json();
        showScanLoading(false);

        if (!res.ok || !result.success) {
            handleScanError(result);
            return;
        }

        // Show preview of the sample
        const previewImg = document.getElementById("preview-image");
        const filename = document.getElementById("preview-filename");
        const uploadPrompt = document.getElementById("upload-prompt");
        const previewBox = document.getElementById("preview-box");

        if (previewImg) previewImg.src = result.image_url;
        if (filename) filename.textContent = sampleName;
        if (uploadPrompt) uploadPrompt.style.display = "none";
        if (previewBox) previewBox.classList.add("active");

        renderDiagnosticResult(result);
        loadRecords();
        loadStats();
    } catch (err) {
        showScanLoading(false);
        alert("Failed to analyze presentation sample leaf: " + err.message);
    }
}

function showScanLoading(isLoading) {
    const spinner = document.getElementById("scan-loading-indicator");
    const dropzone = document.getElementById("drop-zone");
    if (spinner) spinner.style.display = isLoading ? "flex" : "none";
    if (dropzone) dropzone.style.opacity = isLoading ? "0.4" : "1";
}

function handleScanError(result) {
    const msg = result.message || result.error || "Unable to classify this leaf.";
    const solution = result.solution || "Ensure the photo is clear, focused on the leaf surface, and well-lit.";
    alert(`⚠️ Botanical Diagnosis Issue:\n\n${msg}\n\nAction: ${solution}`);
}

function renderDiagnosticResult(data) {
    lastScanResult = data;
    if (window.CropCare3D && typeof window.CropCare3D.triggerScannerComplete === "function") {
        window.CropCare3D.triggerScannerComplete(data);
    }
    const isUr = (typeof currentLang !== "undefined" && currentLang === "ur");

    const placeholder = document.getElementById("result-placeholder");
    const content = document.getElementById("result-active-content");
    if (placeholder) placeholder.style.display = "none";
    if (content) content.style.display = "block";

    // Crop & Disease Labels
    const cropEl = document.getElementById("res-crop");
    if (cropEl) cropEl.textContent = isUr ? (data.crop_ur || data.crop) : data.crop;

    const nameEl = document.getElementById("res-disease-name");
    if (nameEl) nameEl.textContent = isUr ? (data.disease_name_ur || data.disease_name) : data.disease_name;

    const sciEl = document.getElementById("res-scientific");
    if (sciEl) sciEl.textContent = data.scientific_name ? `(${data.scientific_name})` : "";

    // Status Badge
    const statusBadge = document.getElementById("res-status-badge");
    if (statusBadge) {
        const isHealthy = data.status === "Healthy";
        statusBadge.textContent = isUr ? (data.status_ur || data.status) : data.status;
        statusBadge.style.backgroundColor = isHealthy ? "var(--alert-green-bg)" : "var(--alert-red-bg)";
        statusBadge.style.color = isHealthy ? "var(--alert-green)" : "var(--alert-red)";
        statusBadge.style.borderColor = isHealthy ? "var(--alert-green-border)" : "var(--alert-red-border)";
    }

    // Confidence
    const confPct = Math.round(data.confidence || 0);
    const confText = document.getElementById("res-confidence-pct");
    const confBar = document.getElementById("res-confidence-bar");
    if (confText) confText.textContent = `${confPct}%`;
    if (confBar) {
        confBar.style.width = `${confPct}%`;
        confBar.style.backgroundColor = confPct > 70 ? "var(--primary-600)" : confPct > 45 ? "var(--alert-amber)" : "var(--alert-red)";
    }

    // Symptoms
    const symEl = document.getElementById("res-symptoms");
    if (symEl) symEl.textContent = isUr ? (data.symptoms_ur || data.symptoms) : data.symptoms;

    // Prevention List
    const prevList = document.getElementById("res-prevention-list");
    if (prevList) {
        const items = isUr ? (data.prevention_ur || data.prevention || []) : (data.prevention || []);
        prevList.innerHTML = Array.isArray(items) ? items.map(p => `<li>${p}</li>`).join("") : `<li>${items}</li>`;
    }

    // Treatment
    const treatEl = document.getElementById("res-treatment");
    if (treatEl) treatEl.textContent = isUr ? (data.treatment_ur || data.treatment) : data.treatment;

    // Weather Susceptibility
    const weatherNote = document.getElementById("res-weather-note");
    if (weatherNote) {
        weatherNote.textContent = isUr ? (data.weather_advisory_ur || data.weather_advisory) : data.weather_advisory;
    }
}

// -------------------------------------------------------------
// 4. Field & Crop Management (SQLite)
// -------------------------------------------------------------
function initCrops() {
    const addCropForm = document.getElementById("form-add-crop");
    if (addCropForm) {
        addCropForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            const payload = {
                crop_name: document.getElementById("inp-crop-name").value,
                field_name: document.getElementById("inp-field-name").value,
                area_acres: parseFloat(document.getElementById("inp-area-acres").value) || 1.0,
                variety: document.getElementById("inp-crop-variety").value,
                sowing_date: document.getElementById("inp-sowing-date").value,
                soil_type: document.getElementById("inp-soil-type").value,
                notes: document.getElementById("inp-crop-notes").value
            };

            try {
                const res = await fetch("/api/crops", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                if (data.success) {
                    closeModal("modal-add-crop");
                    addCropForm.reset();
                    loadCrops();
                    loadTasks();
                    loadStats();
                } else {
                    alert(data.message || "Failed to save crop.");
                }
            } catch (err) {
                alert("Error saving field: " + err.message);
            }
        });
    }

    const openBtns = ["btn-open-add-crop", "btn-table-add-crop", "btn-empty-add-crop"];
    openBtns.forEach(id => {
        const b = document.getElementById(id);
        if (b) b.addEventListener("click", () => openModal("modal-add-crop"));
    });
}

async function loadCrops() {
    try {
        const res = await fetch("/api/crops");
        const data = await res.json();
        if (!data.success) return;

        const crops = data.crops || [];
        window.currentCrops = crops;
        if (window.CropCare3D && typeof window.CropCare3D.updateFieldCrops === "function") {
            window.CropCare3D.updateFieldCrops(crops);
        }

        // Update nav badge
        const badge = document.getElementById("nav-crops-count");
        if (badge) badge.textContent = crops.length;

        // Render in Crops Page Table
        const tbody = document.getElementById("crops-table-body");
        if (tbody) {
            if (crops.length === 0) {
                tbody.innerHTML = `<tr><td colspan="8" style="text-align:center; padding: 24px; color: var(--text-muted);">No fields registered. Click 'Register New Field' to begin.</td></tr>`;
            } else {
                tbody.innerHTML = crops.map((c, idx) => `
                    <tr>
                        <td>${idx + 1}</td>
                        <td><strong>${c.crop_name}</strong></td>
                        <td>${c.field_name}</td>
                        <td><span class="status-pill status-pill-neutral">${c.area_acres} Acres</span></td>
                        <td>${c.variety || '—'}</td>
                        <td>${c.sowing_date}</td>
                        <td><span class="status-pill status-pill-healthy">${c.soil_type}</span></td>
                        <td>
                            <button class="btn-icon-danger" onclick="deleteCrop(${c.id})" title="Delete Field">
                                <svg class="ag-icon ag-icon-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                    <polyline points="3 6 5 6 21 6"/>
                                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                                </svg>
                            </button>
                        </td>
                    </tr>
                `).join("");
            }
        }

        // Render on Dashboard
        const dashContainer = document.getElementById("dash-crops-container");
        if (dashContainer) {
            if (crops.length === 0) {
                dashContainer.innerHTML = `
                    <div style="padding: 24px 16px; text-align: center; color: var(--text-muted);">
                        <p style="font-size: 0.84rem; margin-bottom: 12px;">No farm fields registered yet. Record your acreage to track sowing milestones.</p>
                        <button class="btn-primary btn-sm" onclick="openModal('modal-add-crop')" type="button">+ Register First Field</button>
                    </div>
                `;
            } else {
                dashContainer.innerHTML = `
                    <table class="crop-summary-table">
                        <tbody>
                            ${crops.map(c => `
                                <tr>
                                    <td class="crop-primary-cell">
                                        <span class="crop-name-strong">${c.crop_name}</span>
                                        <span class="crop-field-sub">${c.field_name} &bull; ${c.variety || 'Standard Variety'}</span>
                                    </td>
                                    <td><span class="status-pill status-pill-neutral">${c.area_acres} Acres</span></td>
                                    <td style="font-size: 0.76rem; color: var(--text-muted);">Sown: ${c.sowing_date}</td>
                                    <td><span class="status-pill status-pill-healthy">${c.soil_type} Soil</span></td>
                                </tr>
                            `).join("")}
                        </tbody>
                    </table>
                `;
            }
        }
    } catch (err) {
        console.error("Failed to load crops:", err);
    }
}

async function deleteCrop(cropId) {
    if (!confirm("Are you sure you want to delete this field and its associated tasks?")) return;
    try {
        const res = await fetch(`/api/crops/${cropId}`, { method: "DELETE" });
        const data = await res.json();
        if (data.success) {
            loadCrops();
            loadTasks();
            loadStats();
        }
    } catch (err) {
        alert("Failed to delete crop: " + err.message);
    }
}
window.deleteCrop = deleteCrop;

// -------------------------------------------------------------
// 5. Farm Calendar & Task Checklist (SQLite)
// -------------------------------------------------------------
function initTasks() {
    const addTaskForm = document.getElementById("form-add-task");
    if (addTaskForm) {
        addTaskForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            const payload = {
                crop_name: document.getElementById("inp-task-crop").value,
                task_type: document.getElementById("inp-task-type").value,
                title: document.getElementById("inp-task-title").value,
                due_date: document.getElementById("inp-task-due").value
            };

            try {
                const res = await fetch("/api/tasks", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                if (data.success) {
                    closeModal("modal-add-task");
                    addTaskForm.reset();
                    loadTasks();
                    loadStats();
                } else {
                    alert(data.message || "Failed to create task.");
                }
            } catch (err) {
                alert("Error adding task: " + err.message);
            }
        });
    }

    const openBtns = ["btn-open-add-task", "btn-table-add-task"];
    openBtns.forEach(id => {
        const b = document.getElementById(id);
        if (b) b.addEventListener("click", () => openModal("modal-add-task"));
    });

    // Task Filter Chips
    document.querySelectorAll("[data-filter-status]").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelectorAll("[data-filter-status]").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            currentTaskFilter = btn.getAttribute("data-filter-status");
            loadTasks();
        });
    });
}

async function loadTasks() {
    try {
        let url = "/api/tasks";
        if (currentTaskFilter !== "all") {
            url += `?status=${currentTaskFilter}`;
        }

        const res = await fetch(url);
        const data = await res.json();
        if (!data.success) return;

        const tasks = data.tasks || [];
        const pendingCount = tasks.filter(t => t.status === "pending").length;

        // Nav badge
        const badge = document.getElementById("nav-tasks-count");
        if (badge) badge.textContent = pendingCount;

        // Render in Farm Calendar Tab
        const fullList = document.getElementById("full-tasks-list");
        if (fullList) {
            if (tasks.length === 0) {
                fullList.innerHTML = `<div style="padding: 24px; text-align: center; color: var(--text-muted); font-size: 0.84rem;">No farm tasks found for this filter.</div>`;
            } else {
                fullList.innerHTML = tasks.map(t => `
                    <div class="task-item ${t.status === 'completed' ? 'completed' : ''}" data-task-id="${t.id}">
                        <div class="task-left">
                            <input type="checkbox" class="task-checkbox" ${t.status === 'completed' ? 'checked' : ''} onchange="toggleTask(${t.id})">
                            <div>
                                <div class="task-title">${t.title}</div>
                                <div class="task-meta">Due: ${t.due_date} &bull; ${t.crop_name}</div>
                            </div>
                        </div>
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span class="task-badge">${t.task_type}</span>
                            <button class="btn-icon-danger" onclick="deleteTask(${t.id})" title="Delete Task">
                                <svg class="ag-icon ag-icon-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                    <polyline points="3 6 5 6 21 6"/>
                                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                                </svg>
                            </button>
                        </div>
                    </div>
                `).join("");
            }
        }

        // Render pending on Dashboard (up to 5)
        const dashContainer = document.getElementById("dash-tasks-container");
        if (dashContainer) {
            const pendingTasks = tasks.filter(t => t.status === "pending").slice(0, 5);
            if (pendingTasks.length === 0) {
                dashContainer.innerHTML = `
                    <div style="padding: 24px 16px; text-align: center; color: var(--text-muted); font-size: 0.82rem;">
                        No pending farm operations due today.
                    </div>
                `;
            } else {
                dashContainer.innerHTML = `
                    <div class="task-list">
                        ${pendingTasks.map(t => `
                            <div class="task-item" data-task-id="${t.id}">
                                <div class="task-left">
                                    <input type="checkbox" class="task-checkbox" onchange="toggleTask(${t.id})">
                                    <div>
                                        <div class="task-title">${t.title}</div>
                                        <div class="task-meta">Due: ${t.due_date} &bull; ${t.crop_name}</div>
                                    </div>
                                </div>
                                <span class="task-badge">${t.task_type}</span>
                            </div>
                        `).join("")}
                    </div>
                `;
            }
        }
    } catch (err) {
        console.error("Failed to load tasks:", err);
    }
}

async function toggleTask(taskId) {
    try {
        const res = await fetch(`/api/tasks/${taskId}/toggle`, { method: "POST" });
        const data = await res.json();
        if (data.success) {
            loadTasks();
            loadStats();
        }
    } catch (err) {
        alert("Failed to toggle task: " + err.message);
    }
}
window.toggleTask = toggleTask;

async function deleteTask(taskId) {
    try {
        const res = await fetch(`/api/tasks/${taskId}`, { method: "DELETE" });
        const data = await res.json();
        if (data.success) {
            loadTasks();
            loadStats();
        }
    } catch (err) {
        alert("Failed to delete task: " + err.message);
    }
}
window.deleteTask = deleteTask;

// -------------------------------------------------------------
// 6. Irrigation Helper
// -------------------------------------------------------------
function initIrrigation() {
    const irriForm = document.getElementById("form-irrigation");
    if (!irriForm) return;

    irriForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const districtSelect = document.getElementById("district-select");
        const lat = districtSelect ? districtSelect.selectedOptions[0].dataset.lat : "31.5204";
        const lon = districtSelect ? districtSelect.selectedOptions[0].dataset.lon : "74.3587";

        const payload = {
            crop_type: document.getElementById("irri-crop-type").value,
            soil_type: document.getElementById("irri-soil-type").value,
            sowing_date: document.getElementById("irri-sowing-date").value,
            lat: lat,
            lon: lon
        };

        try {
            const res = await fetch("/api/irrigation-advisory", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            if (data.success) {
                renderIrrigationAdvisory(data);
            }
        } catch (err) {
            alert("Failed to calculate irrigation: " + err.message);
        }
    });
}

function renderIrrigationAdvisory(data) {
    const isUr = (typeof currentLang !== "undefined" && currentLang === "ur");
    const output = document.getElementById("irrigation-output");
    if (!output) return;

    output.style.display = "block";

    const urgency = document.getElementById("irri-urgency-badge");
    if (urgency) {
        urgency.textContent = data.urgency;
        urgency.style.color = data.urgency_color;
    }

    const intervalTag = document.getElementById("irri-interval-tag");
    if (intervalTag) {
        intervalTag.textContent = isUr
            ? `وقفہ: ہر ${data.recommended_interval_days} دن بعد`
            : `Interval: Every ${data.recommended_interval_days} Days`;
    }

    const actionText = document.getElementById("irri-action-text");
    if (actionText) actionText.textContent = isUr ? data.action_ur : data.action_en;

    const soilText = document.getElementById("irri-soil-text");
    if (soilText) soilText.textContent = isUr ? data.soil_note_ur : data.soil_note_en;

    const stagesText = document.getElementById("irri-stages-text");
    if (stagesText) stagesText.textContent = isUr ? data.critical_stages_ur : data.critical_stages_en;

    const discText = document.getElementById("irri-disclaimer-text");
    if (discText) discText.textContent = isUr ? data.disclaimer_ur : data.disclaimer_en;
}

// -------------------------------------------------------------
// 7. Guides & Mandi Wholesale Rates
// -------------------------------------------------------------
function initGuidesAndMandi() {
    loadGuidesAndMandi();
}

async function loadGuidesAndMandi() {
    const isUr = (typeof currentLang !== "undefined" && currentLang === "ur");

    // Mandi Rates
    try {
        const mRes = await fetch("/api/mandi-rates");
        const mData = await mRes.json();
        if (mData.success && mData.benchmarks) {
            const tbody = document.getElementById("mandi-table-body");
            if (tbody) {
                tbody.innerHTML = mData.benchmarks.map(b => `
                    <tr>
                        <td><strong>${b.commodity}</strong><br><small style="color:var(--text-muted);">${b.variety}</small></td>
                        <td>${b.mandi}</td>
                        <td>${b.unit}</td>
                        <td style="font-weight:700; color:var(--primary-900);">Rs. ${b.modal_price.toLocaleString()}</td>
                    </tr>
                `).join("");
            }
            const disc = document.getElementById("mandi-disclaimer");
            if (disc) disc.textContent = isUr ? mData.disclaimer_ur : mData.disclaimer_en;
        }
    } catch (err) {
        console.warn("Mandi rates fetch error:", err);
    }

    // Guides
    try {
        const gRes = await fetch("/api/knowledge-center");
        const gData = await gRes.json();
        if (gData.success && gData.guides) {
            const container = document.getElementById("guides-accordion-container");
            if (container) {
                container.innerHTML = gData.guides.map(g => {
                    const title = isUr ? g.title_ur : g.title_en;
                    const cat = isUr ? g.category_ur : g.category_en;
                    const points = isUr ? g.points_ur : g.points_en;

                    return `
                        <div class="accordion-item">
                            <div class="accordion-header" onclick="this.parentElement.classList.toggle('open')">
                                <div>
                                    <span style="font-size: 0.75rem; color: var(--primary-700); text-transform: uppercase;">[${cat}]</span>
                                    <div>${title}</div>
                                </div>
                                <span>▼</span>
                            </div>
                            <div class="accordion-body">
                                <ul style="padding-left: 20px; line-height: 1.7;">
                                    ${points.map(pt => `<li>${pt}</li>`).join("")}
                                </ul>
                            </div>
                        </div>
                    `;
                }).join("");
            }
        }
    } catch (err) {
        console.warn("Guides fetch error:", err);
    }
}
window.renderGuidesAndMandi = loadGuidesAndMandi;

// -------------------------------------------------------------
// 8. Farm Records (Scan History Archive)
// -------------------------------------------------------------
function initRecords() {
    loadRecords();

    const clearBtn = document.getElementById("btn-clear-history");
    if (clearBtn) {
        clearBtn.addEventListener("click", async () => {
            if (!confirm("Are you sure you want to clear all leaf scan records?")) return;
            try {
                const res = await fetch("/api/history/clear", { method: "POST" });
                const data = await res.json();
                if (data.success) {
                    loadRecords();
                    loadStats();
                }
            } catch (err) {
                alert("Failed to clear history: " + err.message);
            }
        });
    }
}

async function loadRecords() {
    try {
        const res = await fetch("/api/history");
        const data = await res.json();
        if (!data.success) return;

        const scans = data.scans || [];
        const isUr = (typeof currentLang !== "undefined" && currentLang === "ur");
        const tbody = document.getElementById("history-table-body");

        if (tbody) {
            if (scans.length === 0) {
                tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding: 24px; color: var(--text-muted);">No scan records found. Diagnose a leaf to view saved history.</td></tr>`;
            } else {
                tbody.innerHTML = scans.map((s, idx) => {
                    const dateFormatted = s.timestamp ? s.timestamp.substring(0, 16).replace("T", " ") : "Recent";
                    const isHealthy = s.status === "Healthy";
                    const diagName = isUr ? (s.disease_name_ur || s.disease_name) : s.disease_name;
                    const cropName = isUr ? (s.crop_ur || s.crop) : s.crop;

                    return `
                        <tr>
                            <td>${idx + 1}</td>
                            <td style="font-size:0.8rem; white-space:nowrap;">${dateFormatted}</td>
                            <td><strong>${cropName}</strong></td>
                            <td>${diagName}</td>
                            <td>${Math.round(s.confidence)}%</td>
                            <td>
                                <span class="status-pill ${isHealthy ? 'status-pill-healthy' : 'status-pill-danger'}">
                                    ${isUr ? (s.status_ur || s.status) : s.status}
                                </span>
                            </td>
                            <td>
                                <button class="btn-secondary btn-sm" onclick="viewScanRecord(${s.id})">Inspect</button>
                                <button class="btn-icon-danger" onclick="deleteScanRecord(${s.id})" title="Delete Record">
                                    <svg class="ag-icon ag-icon-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                        <polyline points="3 6 5 6 21 6"/>
                                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                                    </svg>
                                </button>
                            </td>
                        </tr>
                    `;
                }).join("");
            }
        }

        // Render Recent Scans on Dashboard
        const dashRecent = document.getElementById("dash-recent-scans-container");
        if (dashRecent) {
            const recent = scans.slice(0, 4);
            if (recent.length === 0) {
                dashRecent.innerHTML = `<div style="padding: 20px; text-align: center; color: var(--text-muted); font-size: 0.8rem;">No recent scans recorded. Scan a leaf photo to build your field history.</div>`;
            } else {
                dashRecent.innerHTML = recent.map(s => {
                    const isHealthy = s.status === "Healthy";
                    const diagName = isUr ? (s.disease_name_ur || s.disease_name) : s.disease_name;
                    const cropName = isUr ? (s.crop_ur || s.crop) : s.crop;
                    const timeStr = s.timestamp ? s.timestamp.substring(0, 10) : "Recent";
                    const imgSrc = s.filepath ? `/${s.filepath}` : '/static/sample_leaves/healthy_tomato.jpg';
                    return `
                        <div class="recent-scan-row">
                            <div class="recent-scan-left">
                                <img src="${imgSrc}" class="recent-scan-thumb" alt="${diagName}" onerror="this.style.display='none'">
                                <div>
                                    <div style="font-weight: 600; color: var(--text-main); font-size: 0.82rem;">${diagName}</div>
                                    <div style="font-size: 0.74rem; color: var(--text-muted);">${cropName} &bull; ${timeStr}</div>
                                </div>
                            </div>
                            <span class="status-pill ${isHealthy ? 'status-pill-healthy' : 'status-pill-danger'}">${Math.round(s.confidence)}%</span>
                        </div>
                    `;
                }).join("");
            }
        }
    } catch (err) {
        console.error("Failed to load records:", err);
    }
}

async function viewScanRecord(scanId) {
    try {
        const res = await fetch(`/api/history/${scanId}`);
        const data = await res.json();
        if (data.success && data.scan) {
            const s = data.scan;
            const isUr = (typeof currentLang !== "undefined" && currentLang === "ur");
            const modalBody = document.getElementById("scan-modal-body");

            modalBody.innerHTML = `
                <div style="text-align: center; margin-bottom: 16px;">
                    <img src="${s.filepath}" alt="${s.disease_name}" style="max-height: 220px; border-radius: var(--radius-sm); border: 1px solid var(--border-color);">
                </div>
                <h3 style="color: var(--primary-900);">${isUr ? (s.disease_name_ur || s.disease_name) : s.disease_name}</h3>
                <p style="font-size: 0.85rem; color: var(--primary-700); font-weight: 600; margin-bottom: 8px;">${isUr ? (s.crop_ur || s.crop) : s.crop} &bull; ${Math.round(s.confidence)}% Confidence</p>
                <div style="font-size: 0.88rem; line-height: 1.6; margin-bottom: 12px;">
                    <strong>Symptoms:</strong> ${isUr ? (s.symptoms_ur || s.symptoms) : s.symptoms}
                </div>
                <div style="font-size: 0.88rem; line-height: 1.6; margin-bottom: 12px;">
                    <strong>Treatment:</strong> ${isUr ? (s.treatment_ur || s.treatment_en) : s.treatment_en}
                </div>
                <div style="font-size: 0.82rem; color: var(--text-muted);">
                    Timestamp: ${s.timestamp}
                </div>
            `;
            openModal("scan-modal");
        }
    } catch (err) {
        alert("Failed to fetch scan detail: " + err.message);
    }
}
window.viewScanRecord = viewScanRecord;

async function deleteScanRecord(scanId) {
    if (!confirm("Delete this scan record?")) return;
    try {
        const res = await fetch(`/api/history/${scanId}`, { method: "DELETE" });
        const data = await res.json();
        if (data.success) {
            loadRecords();
            loadStats();
        }
    } catch (err) {
        alert("Failed to delete scan: " + err.message);
    }
}
window.deleteScanRecord = deleteScanRecord;

// -------------------------------------------------------------
// 9. Stats Synchronization
// -------------------------------------------------------------
async function loadStats() {
    try {
        const res = await fetch("/api/stats");
        const data = await res.json();
        if (!data.success) return;
        // Keep stats in memory or dispatch update
    } catch (err) {
        console.warn("Failed to update stats:", err);
    }
}

// -------------------------------------------------------------
// 10. Modals Management
// -------------------------------------------------------------
function initModals() {
    // Close modal on X or cancel buttons
    document.getElementById("btn-close-crop-modal")?.addEventListener("click", () => closeModal("modal-add-crop"));
    document.getElementById("btn-cancel-crop-modal")?.addEventListener("click", () => closeModal("modal-add-crop"));

    document.getElementById("btn-close-task-modal")?.addEventListener("click", () => closeModal("modal-add-task"));
    document.getElementById("btn-cancel-task-modal")?.addEventListener("click", () => closeModal("modal-add-task"));

    document.getElementById("btn-close-scan-modal")?.addEventListener("click", () => closeModal("scan-modal"));
    document.getElementById("btn-modal-dismiss")?.addEventListener("click", () => closeModal("scan-modal"));

    // Viva Guide Modal
    document.getElementById("btn-open-viva-modal")?.addEventListener("click", () => openModal("modal-viva-guide"));
    document.getElementById("btn-close-viva-modal")?.addEventListener("click", () => closeModal("modal-viva-guide"));
    document.getElementById("btn-dismiss-viva-modal")?.addEventListener("click", () => closeModal("modal-viva-guide"));

    // Close on overlay backdrop click
    document.querySelectorAll(".modal-overlay").forEach(overlay => {
        overlay.addEventListener("click", (e) => {
            if (e.target === overlay) {
                overlay.classList.remove("active");
            }
        });
    });
}

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.add("active");
}
window.openModal = openModal;

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.remove("active");
}
window.closeModal = closeModal;
