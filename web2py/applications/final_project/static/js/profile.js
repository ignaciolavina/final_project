

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
    get_user_books();
    // fill_placeholders();
};

let getLoggedInUser = function (callback) {
    $.getJSON(get_logged_in_user_url, function (response) {
        app.user = response.user;
        console.log("app.user", app.user);
        app.vmodel_first_name = app.user.first_name;
        app.vmodel_last_name = app.user.last_name;
        callback();
    });
};

let update_profile = function () {
    console.log(app.user.name)
    app.updating_profile = true;

};

let get_user_books = function () {
    $.getJSON(get_user_books_url, function (response) {
        console.log("response get_user_books");
        console.log(response);
        app.user_books = response.books;

    });
};

let delete_book = function (book) {
    console.log("delete book function: ");
    console.log(book)


    $.post(delete_user_book_url, {
        book_id: book.id

    }, function (response) {
    })
};

let save_profile = function () {
    if (app.vmodel_first_name == "" || app.vmodel_last_name == "") {
        alert("user data can not be empty");
    } else {
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

            }, 1000);
        })
    }
};

let app = new Vue({
    el: "#profile_page",
    delimiters: ['${', '}'],
    unsafeDelimiters: ['!{', '}'],
    data: {
        user: '',
        vmodel_first_name: '',
        vmodel_last_name: '',
        vmodel_public_info: '',
        updating_profile: false,
        user_books: []
    },
    methods: {
        update_profile: update_profile,
        save_profile: save_profile,
        fill_placeholders: fill_placeholders,
        get_user_books: get_user_books,
        getLoggedInUser: getLoggedInUser,
        delete_book: delete_book
    }
});

onPageLoad();