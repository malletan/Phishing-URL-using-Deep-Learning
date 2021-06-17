const api = "https://urlwatcher.mooo.com/";
const errors = document.querySelector(".errors");
const loading = document.querySelector(".loading");
const resultValue = document.querySelector(".result-value");
const infoResult = document.querySelector(".info-result")
const results = document.querySelector(".result-container");
results.style.display = "none";
loading.style.display = "none";
errors.textContent = "";
const form = document.querySelector(".form-data");
const url = document.querySelector(".url");

const BAD_LIMIT = 0.5
const MID_LIMIT = 0.7


const searchUrl = async url => {
    loading.style.display = "block";
    errors.textContent = "";
    try {
        const response = await axios.post(`${api}/`, {url: url});
        loading.style.display = "none";
        resultValue.textContent = response.data;
        if (response.data < BAD_LIMIT) {
            infoResult.textContent = "Actual page is not usual warning it is be dangerous";
            infoResult.style.color = "red";
        } else if (response.data < MID_LIMIT) {
            infoResult.textContent = "Actual page might be dangerous";
            infoResult.style.color = "orange";
        } else {
            infoResult.textContent = "Actual page is fine";
            infoResult.style.color = "green";
        }
        //infoResult.textContent = "123456";
        infoResult.style.display = "block";
        results.style.display = "block";
    } catch (error) {
        console.log(error)
        loading.style.display = "none";
        results.style.display = "none";
        infoResult.style.display = "none";
        errors.textContent = "Server is down.";
    }
};

const handleSubmit = async e => {
    e.preventDefault();
    searchUrl(url.value);
    console.log(url.value);
};

form.addEventListener("submit", e => handleSubmit(e));
