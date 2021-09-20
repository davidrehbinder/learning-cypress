(function() {
    "use strict";
    
    const usernameField = document.getElementById("username");
    const passwordField = document.getElementById("password");
    const responseArea = document.getElementById("response");
    const cancelButton = document.getElementById("cancel");
    const page = location.pathname;

    var login = new XMLHttpRequest();
    var createUser = new XMLHttpRequest();
    var response = new Object();

    switch (page) {
        case '/login.html':
            var loginOkButton = document.getElementById("login_ok");
            loginOkButton.addEventListener("click", loginAttempt);
            break;
        case '/sign_up.html':
            var createUserOkButton = document.getElementById("create_user_ok");
            createUserOkButton.addEventListener("click", createUser);
            break;
        default:
            console.log("It's not working.");
    }

    cancelButton.addEventListener("click", clickCancel);

    function loginAttempt() {
        console.log('login!')
        loginOkButton.innerHTML = 'Ok';
        login.addEventListener("loadend", loginComplete);
        var data = new Object;
        var username = usernameField.value;
        var password = passwordField.value;
        data = {"username": username, "password": password};
        var dataString = JSON.stringify(data);
        login.open("POST", "/login.json");
        login.setRequestHeader("Content-Type", "application/json");
        login.send(dataString);
    };

    function createUser() {
        createUserOkButton.innerHTML = 'Ok';
        createUser.addEventListener("loadend", createUserComplete);
        var data = new Object;
        var username = usernameField.value;
        var password = passwordField.value;
        data = {"username": username, "password": password};
        var dataString = JSON.stringify(data);
        createUser.open("POST", "/create_user.json");
        createUser.setRequestHeader("Content-Type", "application/json");
        createUser.send(dataString);
    };

    function clickCancel() {
        cancelButton.innerHTML = 'Cancel';
        usernameField.value = '';
        passwordField.value = '';
    };

    function loginComplete() {
        status = login.status;
        switch(status) {
            case '200':
                response = JSON.parse(login.responseText);
                responseArea.innerHTML = (response);
                break;
            case '403':
                break;
            case '500':
                break;
            default:
                console.log('💩');
        };
    };
    
    function createUserComplete() {
        status = login.status;
        switch(status) {
            case '200':
                response = JSON.parse(login.responseText);
                responseArea.innerHTML = (response);
                break;
            case '403':
                break;
            case '500':
                break;
            default:
                console.log('💩');
        };
    };
    
    })();