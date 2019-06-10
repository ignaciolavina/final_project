

let fill_placeholders = function () {
    placeholder_first_name = app.user.first_name;
    placeholder_last_name = app.user.last_name;
    placeholder_email = app.user.email;
    placeholder_info = 'user info';

    // document.getElementById("username").placeholder = app.user.first_name;

    console.log('filling placeholders');
    console.log('user_inside');
    console.log(app.user);
};

let onPageLoad = function () {
    getLoggedInUser(function () {
    });
    // fill_placeholders();
};

let getLoggedInUser = function (callback) {
    $.getJSON(getLoggedInUserUrl, function (response) {
        app.user = response.user;
        console.log("app.user", app.user);
        vmodel_first_name = app.user.first_name;
        vmodel_last_name = app.user.last_name;
        console.log("vmodel")
        console.log(vmodel_last_name)
        callback();
    });
};

let update_profile = function () {
    console.log(app.user.name)
    app.updating_profile = true;

};


let save_profile = function () {
    app.updating_profile = false;
    app.user.first_name = app.vmodel_first_name;
    app.user.last_name = app.vmodel_last_name;
    console.log("wrsdvzxdx")
    console.log(app.vmodel_first_name)

    $.post(save_profile_url, {
        user: app.user,
        first_name: app.vmodel_first_name,
        last_name: app.vmodel_last_name
    }, function (response) {

        // for implementing a sping load bar
        setTimeout(function () {

            console.log("profile saved");
            // document.getElementById("main_user").innerHTML = app.vmodel_first_name;
            // $('user updated').hide();

            // alert("Book added correctly!");
            // yourReview.hasBeenSaved = false;
        }, 1000);
    })
};

let app = new Vue({
    el: "#profile_page",
    delimiters: ['${', '}'],
    unsafeDelimiters: ['!{', '}'],
    data: {
        user: '',
        vmodel_first_name: '',
        vmodel_last_name: '',
        // placeholder_email: '',
        vmodel_public_info: '',
        updating_profile: false,
        variable: 'varrr'
    },
    methods: {
        update_profile: update_profile,
        save_profile: save_profile,
        fill_placeholders: fill_placeholders
        // getLoggedInUser: getLoggedInUser
    }
});

onPageLoad();