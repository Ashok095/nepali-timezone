/**
 * Nepali DateTime widget functionality
 */

// Nepali calendar data
const nepaliMonths = [
    "Baisakh", "Jestha", "Asar", "Shrawan",
    "Bhadra", "Aswin", "Kartik", "Mangsir",
    "Poush", "Magh", "Falgun", "Chaitra"
];

// Initialize Nepali DateTime widgets
function initNepaliDateTimeWidgets() {
    const inputs = document.querySelectorAll(".nepali-datetime-input");
    inputs.forEach(input => {
        setupNepaliDatePicker(input);
    });
}

// Setup individual date picker
function setupNepaliDatePicker(input) {
    if (typeof $ !== 'undefined' && $.fn.nepaliDatePicker) {
        $(input).nepaliDatePicker({
            dateFormat: "%Y-%m-%d",
            closeOnDateSelect: true
        });
    } else {
        console.warn("Nepali DatePicker library not loaded");
        // Fallback to standard date input
        input.type = "datetime-local";
    }
}

// Initialize on DOM ready
document.addEventListener("DOMContentLoaded", function() {
    initNepaliDateTimeWidgets();
});