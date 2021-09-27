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
    var logout = new XMLHttpRequest();
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
    };

    if (document.cookie.split(";").filter(s => s.includes("username=" + cookieUsername())) != "") {
        loginStatus.innerHTML = "You are logged in as user " + cookieUsername();
        logoutButton.innerHTML = "Log out.";
        logoutButton.addEventListener("click", logOut);
    };

    if (cancelButton != null) {
        cancelButton.addEventListener("click", clickCancel);
    }

    function clickCancel() {
        usernameField.value = "";
        passwordField.value = "";
    };

    function loginAttempt() {
        responseArea.innerHTML = "";
        login.addEventListener("loadend", loginComplete);
        var data = new Object;
        var username = usernameField.value;
        var password = passwordField.value;
        if (username && password != "") {
            usernameField.value = "";
            passwordField.value = "";
            data = {"username": username, "password": password};
            var dataString = JSON.stringify(data);
            login.open("POST", "/login.json");
            login.setRequestHeader("Content-Type", "application/json");
            login.send(dataString);
        } else {
            responseArea.innerHTML = "Username and password required.";
            usernameField.value = "";
            passwordField.value = "";
        };
    };

    function loginComplete() {
        var loginAttemptStatus = JSON.parse(login.responseText);
        switch(loginAttemptStatus["login"]) {
            case "success":
                response = login.responseText;
                loginStatus.innerHTML = "You are logged in as " + cookieUsername();
                logoutButton.innerHTML = "Log out.";
                logoutButton.addEventListener("click", logOut);
                break;
            case "failure":
                responseArea.innerHTML = "Login failed.";
                loginStatus.innerHTML = "";
                logoutButton.innerHTML = "";
                break;
            case "error":
                break;
            default:
                console.log("💩");
        };
    };

    function createUserAttempt() {
        responseArea.innerHTML = "";
        createUser.addEventListener("loadend", createUserComplete);
        var data = new Object;
        var username = usernameField.value;
        var password = passwordField.value;

        if (username && password != "") {
            usernameField.value = "";
            passwordField.value = "";
            data = {"username": username, "password": password};
            var dataString = JSON.stringify(data);
            createUser.open("POST", "/create_user.json");
            createUser.setRequestHeader("Content-Type", "application/json");
            createUser.send(dataString);
        } else {
            responseArea.innerHTML = "Username and password required.";
            usernameField.value = "";
            passwordField.value = "";
        };
    };
    
    function createUserComplete() {
        var createUserStatus = JSON.parse(createUser.responseText);
        console.log(createUserStatus);
        switch (createUserStatus["user_creation"]) {
            case "success":
                responseArea.innerHTML = "User " + createUserStatus["username"] + " created.";
                break;
            case "user_exists":
                responseArea.innerHTML = "User " + createUserStatus["username"] + " already exists.";
                break;
            case "too_short":
                responseArea.innerHTML = "Password is too short (needs to be 4 characters or more).";
                break;
            case "error":
                responseArea.innerHTML = "An error occurred.";
                break;
            default:
                console.log("💩");
        };
        usernameField.value = "";
        passwordField.value = "";
};

    function logOut() {
        logout.open("POST", "/logout.json");
        logout.setRequestHeader("Content-Type", "application/json");
        logout.send();
        loginStatus.innerHTML = "";
        logoutButton.innerHTML = "";
    }

    function cookieUsername() {
        if (document.cookie.split(";").filter(s => s.includes("username")) != "") {
            let username = document.cookie.split(";").filter(s => s.includes("username"));
            return username[0].split("=")[1];
        };
    };

})();