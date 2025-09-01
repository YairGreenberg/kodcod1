const baseURL = "http://127.0.0.1:5000";

const testButton = document.getElementById("all_text")
testButton.addEventListener("click", function (e) {
    getAllData();
});
const searchByDates = document.getElementById("search_dates")
searchByDates.addEventListener("click", function (e) {
    getByRangeOfDates();
});

const searchByWord = document.getElementById("search_text")
searchByWord.addEventListener("click", function (e) {
    getWordInput();
});

function getAllData() {
    fetch(baseURL + '/')
        .then(function (response) {
            return response.json()

        })
        .then(function (data) {
            const dataContainer = document.getElementById("dataContainer")
            for (const obj of data) {            // עובר על כל מילון במערך
                for (const [key, value] of Object.entries(obj)) { // עובר על מפתח:ערך במילון
                    dataContainer.innerHTML += `
                <div>
                    <p>${key}: ${value}</p>
                </div>
            `;
                }
            }

        })
}

function getByRangeOfDates() {
    const datePicker = document.getElementById("datePicker");

    datePicker.innerHTML = `
        <label>
            Start date:
            <input type="date" id="startDate" />
        </label>
        <label>
            End date:
            <input type="date" id="endDate" />
        </label>
        <button id="sendDateToServer" style="display:none;" onclick="sendDateToServer()">click to get</button>`;

    const startInput = document.getElementById("startDate");
    const endInput = document.getElementById("endDate");
    const btn = document.getElementById("sendDateToServer");

    function updateButtonVisibility() {
        if (startInput.value !== "" && endInput.value !== "") {
            btn.style.display = "inline-block";
        } else {
            btn.style.display = "none";
        }
    }

    startInput.addEventListener("change", updateButtonVisibility);
    endInput.addEventListener("change", updateButtonVisibility);
}

async function sendDateToServer() {
    const start = document.getElementById("startDate").value;
    const end = document.getElementById("endDate").value;
    // console.log(start)
    // console.log(end)
const formattedStart = convertToIsraeliFormat(start);
const formattedEnd = convertToIsraeliFormat(end);

console.log("Original dates:", start, end);
console.log("Formatted dates:", formattedStart, formattedEnd);

try {
    const response = await fetch(baseURL + '/filter/date', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            start_date: formattedStart,  // DD-MM-YYYY format
            end_date: formattedEnd      // DD-MM-YYYY format
        })
    });

    const data = await response.json();
    // אפשרי לעשות רק במידה ויש תוצאות
    const filterByDateResults = document.getElementById("filterByDateResults")
    filterByDateResults.innerHTML = ""; // נקה תוצאות קודמות
    
    for (const obj of data) {            // עובר על כל מילון במערך
        for (const [key, value] of Object.entries(obj)) { // עובר על מפתח:ערך במילון
            filterByDateResults.innerHTML += `
            <div>
                <p>${key}: ${value}</p>
            </div> `;
        }
    }

} catch (error) {
    console.error('Error calling server:', error);
    alert('Error searching. Please try again.');
}
}

function convertToIsraeliFormat(dateString) {
    const parts = dateString.split('-'); // [YYYY, MM, DD]
    return `${parts[2]}-${parts[1]}-${parts[0]}`; // DD-MM-YYYY
}

function getWordInput() {
    const inputContainer = document.getElementById("inputContainer");

    const input = document.createElement("input");
    input.type = "text";
    input.id = "wordInput";
    input.placeholder = "Type a word";

    const submitBtn = document.createElement("button");
    submitBtn.textContent = "Submit";
    submitBtn.addEventListener("click", async function () {
        const value = input.value.trim();
        if (value == "") {
            alert("Please type a word first!");
        } else {
            try {
                const response = await fetch(baseURL + '/filter/string', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        word: value
                    })
                });

                const data = await response.json();
                // אפשרי לעשותרק במידה ויש תוצאות
                const filterByTextResults = document.getElementById("filterByTextResults")
                for (const obj of data) {            // עובר על כל מילון במערך
                    for (const [key, value] of Object.entries(obj)) { // עובר על מפתח:ערך במילון
                        filterByTextResults.innerHTML += `
                <div>
                    <p>${key}: ${value}</p>
                    </div> `;
                    }
                }

            } catch (error) {
                console.error('Error calling server:', error);
                alert('Error searching. Please try again.');
            }
        }
    });

    inputContainer.appendChild(input);
    inputContainer.appendChild(submitBtn);
}








