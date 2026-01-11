function isTokenExpired(token) {
    const payload = JSON.parse(atob(token.split('.')[1]));
    return payload.exp * 1000 < Date.now();
}

async function refreshAccessToken() {
    const refresh = localStorage.getItem("refresh");

    if (!refresh) {
        logout();
        return null;
    }

    const res = await fetch("http://127.0.0.1:8000/api/token/refresh/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh })
    });

    if (!res.ok) {
        logout();
        return null;
    }

    const data = await res.json();
    localStorage.setItem("access", data.access);
    return data.access;
}

function logout() {
    localStorage.clear();
    window.location.href = "{% url 'login' %}";
}

async function authFetch(url, options = {}) {
    let token = localStorage.getItem("access");

    if (!token || isTokenExpired(token)) {
        token = await refreshAccessToken();
        if (!token) return;
    }

    options.headers = {
        ...(options.headers || {}),
        "Authorization": "Bearer " + token,
    };

    let response = await fetch(url, options);

    if (response.status === 401) {
        token = await refreshAccessToken();
        if (!token) return;

        options.headers.Authorization = "Bearer " + token;
        response = await fetch(url, options);
    }

    return response;
}
