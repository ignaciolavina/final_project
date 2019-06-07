

let onPageLoad = function () {
    getLoggedInUser(function () {
        // getAllBooks();
    });

};

let getLoggedInUser = function (callback) {
    $.getJSON(getLoggedInUserUrl, function (response) {
        app.loggedInUser = response.user;
        console.log(app.loggedInUser);
        callback();
    });
};

let get_user = function () {

};

let app = new Vue({
    el: "#profile_page",
    delimiters: ['${', '}'],
    unsafeDelimiters: ['!{', '}'],
    data: {

    },
    methods: {
        // getLoggedInUser: getLoggedInUser
    }
});

onPageLoad();