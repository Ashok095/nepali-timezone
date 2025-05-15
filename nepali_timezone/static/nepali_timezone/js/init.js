document.addEventListener("DOMContentLoaded", function() {
    // Initialize nepali-date-picker on all inputs with class .nepali-datetime-input
    const inputs = document.querySelectorAll(".nepali-datetime-input");
    inputs.forEach(input => {
        // Check if jQuery and nepali-date-picker are available
        if (typeof $ !== 'undefined' && $.fn.nepaliDatePicker) {
            // Configure nepali-date-picker
            $(input).nepaliDatePicker({
                dateFormat: "%Y-%m-%d",
                closeOnDateSelect: true,
                // Additional options can be added here
            });

            // Handle time input separately (nepali-date-picker is date-only)
            input.addEventListener("change", function() {
                // Ensure time is appended if not provided
                if (this.value && !this.value.includes(" ")) {
                    this.value += " 00:00:00";
                }
            });
        } else {
            // Fallback to standard date input if libraries aren't available
            console.warn("jQuery or nepali-date-picker not available");
            input.type = "datetime-local";
        }
    });
});