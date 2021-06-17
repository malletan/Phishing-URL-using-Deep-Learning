var jsonData = 0
const BAD_LIMIT = 0.5
const MID_LIMIT = 0.7


function checkActualPage() {
    let headers = new Headers();
    headers.append('Content-Type', 'application/json');
    let page = '{"url":"' + window.location + '"}';
    (async () => {
        const resp = await fetch("https://urlwatcher.mooo.com/",
            {
                method: "POST",
                headers: headers,
                body: page
            });
        jsonData = await resp.json();
        if (jsonData < BAD_LIMIT) {
            alert("Actual page is not usual warning it is be dangerous")
        } else if (jsonData < MID_LIMIT) {
            alert("Actual page might be dangerous")
        } else {
            alert("Actual page is fine")
        }
    })();
}

checkActualPage()
