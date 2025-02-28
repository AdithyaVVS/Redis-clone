const API_BASE_URL = "http://127.0.0.1:5000";

function getApiKey() {
    return document.getElementById("apiKey").value;
}

function setKey() {
    const key = document.getElementById("setKey").value;
    const value = document.getElementById("setValue").value;

    fetch(`${API_BASE_URL}/set`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-API-Key": getApiKey()
        },
        body: JSON.stringify({ key: key, value: value })
    })
    .then(response => response.json())
    .then(data => alert(data.message));
}

function getKey() {
    const key = document.getElementById("getKey").value;

    fetch(`${API_BASE_URL}/get?key=${key}`, {
        method: "GET",
        headers: { "X-API-Key": getApiKey() }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("getResult").innerText = data.value || data.error;
    });
}

function listKeys() {
    fetch(`${API_BASE_URL}/list_keys`, {
        method: "GET",
        headers: { "X-API-Key": getApiKey() }
    })
    .then(response => response.json())
    .then(data => {
        const searchKey = document.getElementById("searchKey").value.toLowerCase();
        const keysList = document.getElementById("keysList");
        keysList.innerHTML = "";
        data.keys.forEach(key => {
            if (key.toLowerCase().includes(searchKey)) {
                let li = document.createElement("li");
                li.innerText = key;
                keysList.appendChild(li);
            }
        });
    });
}

function deleteKey() {
    const key = document.getElementById("deleteKey").value;

    fetch(`${API_BASE_URL}/delete`, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            "X-API-Key": getApiKey()
        },
        body: JSON.stringify({ key: key })
    })
    .then(response => response.json())
    .then(data => alert(data.message));
}

function setTTL() {
    const key = document.getElementById("ttlKey").value;
    const ttl = document.getElementById("ttlValue").value;

    fetch(`${API_BASE_URL}/expire`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-API-Key": getApiKey()
        },
        body: JSON.stringify({ key: key, ttl: parseInt(ttl) })
    })
    .then(response => response.json())
    .then(data => alert(data.message));
}

function getTTL() {
    const key = document.getElementById("checkTTLKey").value;

    fetch(`${API_BASE_URL}/ttl?key=${key}`, {
        method: "GET",
        headers: { "X-API-Key": getApiKey() }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("ttlResult").innerText = `TTL: ${data.ttl || data.error}`;
    });
}

function enqueue() {
    const queue = document.getElementById("queueName").value;
    const value = document.getElementById("queueValue").value;

    fetch(`${API_BASE_URL}/enqueue`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-API-Key": getApiKey()
        },
        body: JSON.stringify({ queue: queue, value: value })
    })
    .then(response => response.json())
    .then(data => alert(data.message));
}

function dequeue() {
    const queue = document.getElementById("queueName").value;

    fetch(`${API_BASE_URL}/dequeue?queue=${queue}`, {
        method: "GET",
        headers: { "X-API-Key": getApiKey() }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("queueResult").innerText = `Dequeued: ${data.value || data.error}`;
    });
}
