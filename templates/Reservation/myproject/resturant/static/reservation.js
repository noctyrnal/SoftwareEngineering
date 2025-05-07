document.addEventListener("DOMContentLoaded", function () {
    const dateInput = document.getElementById("reservation-date");
    const timeInput = document.getElementById("reservation-time");

    let reservedSlots = {};

    // Fetch reserved slots
    fetch("/reserved-slots/")
        .then(response => response.json())
        .then(data => {
            data.forEach(slot => {
                const key = slot.date;
                if (!reservedSlots[key]) {
                    reservedSlots[key] = [];
                }
                reservedSlots[key].push(slot.time);
            });
        });

    dateInput.addEventListener("change", function () {
        const selectedDate = this.value;
        const times = reservedSlots[selectedDate] || [];

        // Reset time input
        timeInput.value = "";

        // Disable time options dynamically if needed
        // (For a better UX, you could replace this with a dropdown instead of input)
        timeInput.addEventListener("input", function () {
            if (times.includes(this.value)) {
                alert("This time is already booked. Please choose another time.");
                this.value = "";
            }
        });
    });
});
