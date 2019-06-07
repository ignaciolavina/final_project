

let fill_placeholders = function () {
    placeholder_first_name = app.user.first_name;
    placeholder_last_name = app.user.last_name;
    placeholder_email = app.user.email;
    placeholder_info = 'user info';

    document.getElementById("username").placeholder = app.user.first_name;

    console.log('filling placeholders');
    console.log('user_inside');
    console.log(app.user);
}

let onPageLoad = function () {
    getLoggedInUser(function () {
        console.log('dd');
    });
    // fill_placeholders();
};

let getLoggedInUser = function (callback) {
    $.getJSON(getLoggedInUserUrl, function (response) {
        app.user = response.user;
        console.log(app.user);
        callback();
    });
};

let update_profile = function () {
    // document.getElementById("username").placeholder = "Type name here..";
    app.updating_profile = true;
}

let save_profile = function () {
    fill_placeholders();
    app.updating_profile = false;
}

let app = new Vue({
    el: "#profile_page",
    delimiters: ['${', '}'],
    unsafeDelimiters: ['!{', '}'],
    data: {
        user: '',
        placeholder_first_name: '',
        placeholder_last_name: '',
        placeholder_email: '',
        placeholder_info: '',
        updating_profile: false
    },
    methods: {
        update_profile: update_profile,
        save_profile: save_profile,
        fill_placeholders: fill_placeholders
        // getLoggedInUser: getLoggedInUser
    }
});

onPageLoad();