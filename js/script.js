(function() {
    "use strict";

    const page = location.pathname;

    const usernameField = document.getElementById("username");
    const passwordField = document.getElementById("password");
    const headlineField = document.getElementById("headline");
    const cancelButton = document.getElementById("cancel");
    const contentField = document.getElementById("content");
    const header = document.getElementById("header");
    const loginStatus = document.getElementById("login-status");
    const responseArea = document.getElementById("response");
    const logoutButtonArea = document.getElementById("logout");
    var logoutButton = document.getElementById("logoutButton");

    const domObserver = new MutationObserver(() => {
        if (logoutButton == null) {
            logoutButton = document.getElementById("logoutButton");
        }
    });

    var login = new XMLHttpRequest();
    var createUser = new XMLHttpRequest();
    var makePost = new XMLHttpRequest();
    var logout = new XMLHttpRequest();
    var getPosts = new XMLHttpRequest();
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
        case "/loggedin.html":
            var postOkButton = document.getElementById("post_ok");
            postOkButton.addEventListener("click", postAttempt);
            break;
        default:
    };

    if (document.cookie.split(";").filter(s => s.includes("username=" + cookieUsername())) != "") {
        loginStatus.innerHTML = "You are logged in as user " + cookieUsername();
        makeLogoutButton();
        if (page == "/index.html") {
            header.innerHTML = "<a href=\"/loggedin.html\">Create a post</a> |"
            header.innerHTML = header.innerHTML +"<a href=\"/posts.html\">View posts</a>"
        };
        if (page == "/posts.html") {
            getPostsAttempt();
        };
    };

    if (cancelButton != null) {
        cancelButton.addEventListener("click", clickCancel);
    }

    function clickCancel() {
        switch (page) {
            case "/login.html":
            case "/sign_up.html":
                usernameField.value = "";
                passwordField.value = "";
                break;
            case "/loggedin.html":
                headlineField.value = "";
                contentField.value = "";
                break;
            default:
        };
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
                makeLogoutButton();
                break;
            case "failure":
                responseArea.innerHTML = "Login failed.";
                loginStatus.innerHTML = "";
                logoutButtonArea.innerHTML = "";
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

    function postAttempt() {
        responseArea.innerHTML = "";
        let username = cookieUsername();
        if (typeof(username) == undefined) {
            return;
        };
        makePost.addEventListener("loadend", postComplete);
        var data = new Object;
        var headline = headlineField.value;
        var content = contentField.value;
        if (headline && content != "") {
            headlineField.value = "";
            contentField.value = "";
            data = {"username": username, "headline": headline, "content": content};
            var dataString = JSON.stringify(data);
            makePost.open("POST", "/post.json");
            makePost.setRequestHeader("Content-Type", "application/json");
            makePost.send(dataString);
        } else {
            responseArea.innerHTML = "Both headline and content required.";
            headlineField.value = "";
            contentField.value = "";
        };
    };

    function postComplete() {
        var postAttemptStatus = JSON.parse(makePost.responseText);
        switch(postAttemptStatus["post_creation"]) {
            case "success":
                let post_id = postAttemptStatus["post_id"];
                responseArea.innerHTML = "Post created successfully, id " + post_id;
                break;
            case "failure":
                responseArea.innerHTML = "Post creation failed.";
                break;
            case "error":
                responseArea.innerHTML = "An error occurred.";
                break;
            default:
                console.log("💩");
        };
    };

    function getPostsAttempt() {
        getPosts.addEventListener("loadend", getPostsComplete)
        getPosts.open("GET", "/post.json");
        getPosts.setRequestHeader("Content-Type", "application/json");
        getPosts.send()
    };

    function getPostsComplete() {
        let postList = document.getElementById("post-list");
        postList.innerHTML = ""
        var getPostsStatus = JSON.parse(getPosts.responseText);
        switch(getPostsStatus['status']) {
            case "no_posts":
                postList.innerHTML = "There are no posts to show.";
                break;
            case "error":
                postList.innerHTML = "Something went wrong.";
                break;
            case "success":
                let postCount = getPostsStatus['posts'].length;
                let allPosts = getPostsStatus['posts']
                for (let post = 0; post < postCount; post++) {
                    let currentPost = allPosts[post];
                    postList.innerHTML = postList.innerHTML + "<p id=\"post" + currentPost['id'] + "\">";
                    postList.innerHTML = postList.innerHTML + "<div class=\"headline\">" + currentPost['headline'] + "</div>";
                    postList.innerHTML = postList.innerHTML + "<div class=\"author\">Author: " + currentPost['username'] + "</div>";
                    postList.innerHTML = postList.innerHTML + "<div class=\"content\">" + currentPost['content'] + "</div>";
                    postList.innerHTML = postList.innerHTML + "</p>";
                };
                break;
            default:
                break;
        };
    };

    function makeLogoutButton() {
        const logoutButton = document.createElement("button");
        logoutButton.id = "logoutButton";
        logoutButton.name = "logoutButton";
        logoutButton.innerHTML = "Log out";
        logoutButtonArea.appendChild(logoutButton);
        logoutButton.addEventListener("click", logOut);
    };

    function logOut() {
        logout.open("POST", "/logout.json");
        logout.setRequestHeader("Content-Type", "application/json");
        logout.send();
        loginStatus.innerHTML = "";
        logoutButtonArea.innerHTML = "";
        if (page == "/index.html") {
            header.innerHTML = "";
        };
    };

    domObserver.observe(document.body, { childList: true, subtree: true});

    function cookieUsername() {
        if (document.cookie.split(";").filter(s => s.includes("username")) != "") {
            let username = document.cookie.split(";").filter(s => s.includes("username"));
            return username[0].split("=")[1];
        };
    };

})();