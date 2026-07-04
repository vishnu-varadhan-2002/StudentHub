// ================= Panel navigation =================
const navItems = document.querySelectorAll(".nav-item");
const panels = document.querySelectorAll(".panel");
const pageTitle = document.getElementById("page-title");

function showPanel(name) {
    navItems.forEach(n => n.classList.toggle("active", n.dataset.panel === name));
    panels.forEach(p => p.classList.toggle("active", p.id === "panel-" + name));
    const active = [...navItems].find(n => n.dataset.panel === name);
    if (active && pageTitle) pageTitle.textContent = active.textContent.trim();
    window.scrollTo({ top: 0, behavior: "smooth" });
}

navItems.forEach(item => {
    item.addEventListener("click", () => showPanel(item.dataset.panel));
});

// Open a panel if the URL has a #panel-xxx hash (used after fee payment / upload)
if (location.hash.startsWith("#panel-")) {
    showPanel(location.hash.replace("#panel-", ""));
}

// ================= Tabs (results / announcements / updates) =================
document.querySelectorAll(".tabs").forEach(group => {
    const buttons = group.querySelectorAll(".tab");
    const container = group.parentElement;
    buttons.forEach(btn => {
        btn.addEventListener("click", () => {
            buttons.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            container.querySelectorAll(".tab-body").forEach(body => {
                body.classList.toggle("active", body.dataset.body === btn.dataset.tab);
            });
        });
    });
});

// ================= Guided tour (Hubby the mascot) =================
const steps = [
    { panel: "dashboard",     title: "Hi, I'm Hubby! 🤖",     text: "Welcome to StudentHub — your all-in-one campus app. Let me give you a quick tour!" },
    { panel: "dashboard",     title: "Your Dashboard 🏠",      text: "Here you see your attendance, CGPA, pending fees and upcoming events at a glance." },
    { panel: "attendance",    title: "Attendance 🗓️",          text: "Track your subject-wise attendance. Anything below 75% is flagged in red." },
    { panel: "results",       title: "Results 📊",             text: "Check your exam scores and practical lab marks with grades." },
    { panel: "bio",           title: "Bio Data 🧑",            text: "All your personal and academic details live here." },
    { panel: "projects",      title: "Projects 📤",            text: "Upload your project files and view everything you've submitted." },
    { panel: "announcements", title: "Announcements 📢",       text: "Never miss general and exam-related notices from your college." },
    { panel: "updates",       title: "Campus Updates 📰",      text: "Stay updated on campus news, events, culturals and sports!" },
    { panel: "fees",          title: "Fees & Receipts 💳",     text: "Pay tuition, bus, canteen and other fees — and download receipts instantly." },
    { panel: "dashboard",     title: "You're all set! 🎉",     text: "That's StudentHub! Explore freely — I'm always here if you need me." },
];

let stepIndex = 0;
const guideLayer = document.getElementById("guideLayer");
const guideTitle = document.getElementById("guideTitle");
const guideText = document.getElementById("guideText");
const guideNext = document.getElementById("guideNext");
const guideDots = document.getElementById("guideDots");

function renderStep() {
    const s = steps[stepIndex];
    showPanel(s.panel);
    guideTitle.textContent = s.title;
    guideText.textContent = s.text;
    guideNext.textContent = stepIndex === steps.length - 1 ? "Finish 🎉" : "Next →";
    guideDots.innerHTML = steps.map((_, i) =>
        `<span class="${i === stepIndex ? 'on' : ''}"></span>`).join("");
}

function startTour() {
    stepIndex = 0;
    guideLayer.classList.add("show");
    renderStep();
}

function nextStep() {
    if (stepIndex < steps.length - 1) {
        stepIndex++;
        renderStep();
    } else {
        endTour();
    }
}

function endTour() {
    guideLayer.classList.remove("show");
    localStorage.setItem("hub_tour_done", "1");
    showPanel("dashboard");
}

// Auto-start the tour the first time a student logs in
window.addEventListener("load", () => {
    if (!localStorage.getItem("hub_tour_done")) {
        setTimeout(startTour, 600);
    }
});
