const baseURL = "http://127.0.0.1:5000";

const allDivs = [
    "dataContainer",
    "filterByDateResults",
    "filterByTextResults",
    "datePicker",
    "inputContainer"
];

function hideAllDivs() {
    allDivs.forEach(id => {
        const div = document.getElementById(id);
        if (div) {
            div.style.display = "none";
            div.innerHTML = "";
        }
    });
}

function showDiv(divIds) {
    hideAllDivs();
    if (!Array.isArray(divIds)) {
        divIds = [divIds];
    }
    divIds.forEach(id => {
        const div = document.getElementById(id);
        if (div) {
            div.style.display = "block";
        }
    });
}

document.getElementById("all_text").addEventListener("click", () => {
    showDiv("dataContainer");
    getAllData();
});

document.getElementById("search_dates").addEventListener("click", () => {
    showDiv("datePicker");
    getByRangeOfDates();
});

document.getElementById("search_text").addEventListener("click", () => {
    showDiv("inputContainer");
    getWordInput();
});


function getAllData() {
    const container = document.getElementById("dataContainer");
    fetch(baseURL + '/')
        .then(res => res.json())
        .then(data => {
            container.innerHTML = '';

            data.forEach(obj => {
                const card = document.createElement("div");
                card.className = "data-card p-4 shadow-lg";

                const contentHTML = `
                            <p class="text-lg"><strong>Date:</strong> ${obj.date}</p>
                            <p class="text-lg"><strong>Time:</strong> ${obj.time}</p>
                            <p class="text-lg"><strong>Text:</strong> ${obj.text}</p>
                        `;

                card.innerHTML = contentHTML;
                container.innerHTML += `<div class="seperate-div"></div>`
                container.appendChild(card);
            });
        })
        .catch(err => alert("Error fetching data: " + err));
}

function getByRangeOfDates() {
    const datePicker = document.getElementById("datePicker");
    datePicker.innerHTML = `
        <div class="input-wrapper">
            <label>Start Date:</label>
            <input type="text" id="startDate" placeholder="dd-mm-yyyy" />
            <span class="calendar-icon">&#128197;</span>
        </div>
        <div class="input-wrapper">
            <label>End Date:</label>
            <input type="text" id="endDate" placeholder="dd-mm-yyyy" />
            <span class="calendar-icon">&#128197;</span>
        </div>
        <button id="sendDateToServer" style="display:none;" class="btn">Click to get</button>
    `;

    const startInput = document.getElementById("startDate");
    const endInput = document.getElementById("endDate");
    const btn = document.getElementById("sendDateToServer");

    function updateButtonVisibility() {
        btn.style.display = (startInput.value && endInput.value) ? "inline-block" : "none";
    }

    flatpickr("#startDate", {
        dateFormat: "d-m-Y",
        onChange: updateButtonVisibility,
        maxDate: "today"
    });
    flatpickr("#endDate", {
        dateFormat: "d-m-Y",
        onChange: updateButtonVisibility,
        maxDate: "today",
    });

    btn.addEventListener("click", sendDateToServer);
}

async function sendDateToServer() {
    const start = document.getElementById("startDate").value;
    const end = document.getElementById("endDate").value;
    showDiv("filterByDateResults")

    if (!start || !end) return;

    const startObj = parseDateToObject(start);
    const endObj = parseDateToObject(end);

    try {
        const response = await fetch(baseURL + '/filter/date', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                from_year: startObj.year, from_month: startObj.month, from_day: startObj.day,
                to_year: endObj.year, to_month: endObj.month, to_day: endObj.day
            })
        });
        const data = await response.json();
        const container = document.getElementById("filterByDateResults");
        container.innerHTML = "";

        if (data.length === 0) {
            container.innerHTML = `<p>No results found for the selected date range.</p>`;
        } else {
            data.forEach(obj => {
                const card = document.createElement("div");
                card.className = "data-card p-4 shadow-lg";

                const contentHTML = `
                            <p class="text-lg"><strong>Date:</strong> ${obj.date}</p>
                            <p class="text-lg"><strong>Time:</strong> ${obj.time}</p>
                            <p class="text-lg"><strong>Text:</strong> ${obj.text}</p>
                        `;

                card.innerHTML = contentHTML;
                container.innerHTML += `<div class="seperate-div"></div>`
                container.appendChild(card);
            });
        }
    } catch (err) {
        alert("Error fetching date data: " + err);
    }
}

function parseDateToObject(dateStr) {
    const [day, month, year] = dateStr.split("-");
    return { day: day.padStart(2, "0"), month: month.padStart(2, "0"), year };
}

function getWordInput() {
    const inputContainer = document.getElementById("inputContainer");
    inputContainer.innerHTML = "";

    const input = document.createElement("input");
    input.type = "text";
    input.id = "wordInput";
    input.placeholder = "Type a word";

    const submitBtn = document.createElement("button");
    submitBtn.textContent = "Submit";
    submitBtn.classList.add("btn");
    submitBtn.addEventListener("click", async () => {
        showDiv("filterByTextResults");
        const word = input.value.trim();
        if (!word) {
            document.getElementById("filterByTextResults").innerHTML = `<p>Please type a word first!</p>`;
            return;
        }

        try {
            const response = await fetch(baseURL + '/filter/string', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ word })
            });
            const data = await response.json();
            const container = document.getElementById("filterByTextResults");
            container.innerHTML = "";

            if (data.length === 0) {
                container.innerHTML = `<p>No results found for the word "${word}".</p>`;
            } else {
                data.forEach(obj => {
                    const card = document.createElement("div");
                    card.className = "data-card p-4 shadow-lg";

                    const contentHTML = `
                            <p class="text-lg"><strong>Date:</strong> ${obj.date}</p>
                            <p class="text-lg"><strong>Time:</strong> ${obj.time}</p>
                            <p class="text-lg"><strong>Text:</strong> ${obj.text}</p>
                        `;

                    card.innerHTML = contentHTML;
                    container.innerHTML += `<div class="seperate-div"></div>`
                    container.appendChild(card);
                });
            }
        } catch (err) {
            alert("Error fetching text data: " + err);
        }
    });

    inputContainer.appendChild(input);
    inputContainer.appendChild(submitBtn);
}

document.addEventListener("DOMContentLoaded", hideAllDivs);






let selectedComputer = "";

const computerList = document.getElementById("computer-list");
const buttons = document.querySelectorAll('.controls .btn');

function toggleButtons() {
    const isComputerSelected = computerList.value !== "";

    buttons.forEach(button => {
        button.disabled = !isComputerSelected;
    });
}

computerList.addEventListener("change", () => {
    selectedComputer = computerList.value;
    hideAllDivs();
    const dataContainer = document.getElementById("dataContainer");
    dataContainer.style.display = "block";
    dataContainer.innerHTML = `<p>Data will be loaded based on the selected computer: <strong>${selectedComputer}</strong>. Please click a button to view.</p>`;
    toggleButtons()
});