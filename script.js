(function() {
    "use strict";

    const page = location.pathname;

    const usernameField = document.getElementById("username");
    const passwordField = document.getElementById("password");
    const cancelButton = document.getElementById("cancel");
    const loginStatus = document.getElementById("login-status");
    const logoutButton = document.getElementById("logout");

    const responseArea = document.getElementById("response");

    var login = new XMLHttpRequest();
    var createUser = new XMLHttpRequest();
    var response = new Object();

    switch (page) {
        case "/login.html":
            var loginOkButton = document.getElementById("login_ok");
            loginOkButton.addEventListener("click", loginAttempt);
            break;
        case "/sign_up.html":
            var createUserOkButton = document.getElementById("create_user_ok");
            createUserOkButton.addEventListener("click", createUserAttempt);
            break;
        default:
            console.log("It's not working.");
    }

    if(document.cookie.split(";").filter(s => s.includes("username")) != "") {
        var cookieUsername = document.cookie.split(";").filter(s => s.includes("username"));
        cookieUsername = cookieUsername[0].split("=")[1];
    }

    if(document.cookie.split(";").filter(s => s.includes("login=success")) != "") {
        loginStatus.innerHTML = "You are logged in as user " + cookieUsername;
        logoutButton.innerHTML = "Log out.";
        logoutButton.addEventListener("click", logOut);
    };

    cancelButton.addEventListener("click", clickCancel);

    function loginAttempt() {
        responseArea.innerHTML = "";
        login.addEventListener("loadend", loginComplete);
        var data = new Object;
        var username = usernameField.value;
        var password = passwordField.value;
        usernameField.value = "";
        passwordField.value = "";
        data = {"username": username, "password": password};
        var dataString = JSON.stringify(data);
        document.cookie = "username=" + username + "; max-age=3600; path=/"
        login.open("POST", "/login.json");
        login.setRequestHeader("Content-Type", "application/json");
        login.send(dataString);
    };

    function createUserAttempt() {
        responseArea.innerHTML = "";
        createUser.addEventListener("loadend", createUserComplete);
        var data = new Object;
        var username = usernameField.value;
        var password = passwordField.value;
        if(username && password != "") {
            usernameField.value = "";
            passwordField.value = "";
            data = {"username": username, "password": password};
            document.cookie = "username=" + username + "; max-age=3600; path=/"
            console.log(document.cookie);
            var dataString = JSON.stringify(data);
            createUser.open("POST", "/create_user.json");
            createUser.setRequestHeader("Content-Type", "application/json");
            createUser.send(dataString);
            responseArea.innerHTML = "User " + username + " created.";
        } else {
            responseArea.innerHTML = "Username and password required.";
        };
    };

    function clickCancel() {
        usernameField.value = "";
        passwordField.value = "";
    };

    function loginComplete() {
        var loginAttemptStatus = login.status;
        switch(loginAttemptStatus) {
            case 200:
                response = login.responseText;
                document.cookie = "login=success; max-age=3600; path=/";
                loginStatus.innerHTML = "You are logged in as " + cookieUsername;
                logoutButton.innerHTML = "Log out.";
                logoutButton.addEventListener("click", logOut);
                break;
            case 403:
                responseArea.innerHTML = "Login failed.";
                var cookie = document.cookie.split(";");
                cookie = cookie.map(x => x + "; max-age=0");
                cookie.map(x => document.cookie = x);
                loginStatus.innerHTML = "";
                logoutButton.innerHTML = "";
                break;
            case 500:
                break;
            default:
                console.log("💩");
        };
    };
    
    function createUserComplete() {
        var createUserStatus = createUser.status;
        switch(createUserStatus) {
            case 200:
                response = JSON.parse(login.responseText);
                responseArea.innerHTML = (response);
                break;
            case 403:
                break;
            case 500:
                break;
            default:
                console.log("💩");
        };
    };

    function logOut() {
        var cookie = document.cookie.split(";");
        cookie = cookie.map(x => x + "; max-age=0");
        cookie.map(x => document.cookie = x);
        loginStatus.innerHTML = "";
        logoutButton.innerHTML = "";
    }

})();