

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
    get_watchlisted_books();
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

let toggle_watchlist = function (bookIndex, bookArray) {
    let book = bookArray[bookIndex];
    let new_status = !book.is_watchlisted;
    book.is_watchlisted = new_status;
    $.post(toggle_watchlist_url, {
        // Book ID
        book_id: book.id,
        // User ID
        user_email: app.user.email
    }, function (response) {
        if (bookArray == app.watchlisted_books && (!book.is_watchlisted)) {
            app.watchlisted_books.splice(bookIndex, 1);
        }
        // for implementing a sping load bar
        setTimeout(function () {
            alert("Watchlist status toggled!");
        }, 1000);
    }
    )
};

// Processes the books and adds an index to each one
let processWatchlistedBooks = function () {
    let index = 0;
    app.watchlisted_books.map((book) => {
        Vue.set(book, 'index', index++);
        Vue.set(book, 'is_watchlisted', book.watchlist_status)
    });
};

// Processes the books and adds an index to each one
let processUserBooks = function () {
    let index = 0;
    app.user_books.map((book) => {
        Vue.set(book, 'index', index++);
        Vue.set(book, 'is_watchlisted', book.watchlist_status)
    });
};

let get_user_books = function () {
    $.getJSON(get_user_books_url, {
        with_watchlist: true
    },
        function (response) {
        app.user_books = response.books;
        processUserBooks();
    });
};

let get_watchlisted_books = function () {
    $.getJSON(getAllBooksUrl, {
        with_watchlist: true
    },
        function (response) {
            let books = response.books;
            books.forEach(element => {
                if (element.watchlist_status == true) {
                    app.watchlisted_books.push(element);
                }
            });
            processWatchlistedBooks();
        });
};

// Confirmation function on delete
let delete_confirmation = function (book) {
    if (confirm("Are you sure you want to delete the book?")) {
        delete_book(book);
    }
};

let hover_card = function () {
    console.log("hover")
};

let delete_book = function (book) {
    console.log("delete book function: ");
    console.log(book)

    // window.confirm("Are you sure you want to delete the book?");


    $.post(delete_user_book_url, {
        book_id: book.id

    }, function (response) {
        window.location.href = '/profile';
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

let edit_book = function (book) {
    window.location.href = '/edit_book/' + book.id;
}

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
        user_books: [],
        watchlisted_books: []
    },
    methods: {
        update_profile: update_profile,
        save_profile: save_profile,
        fill_placeholders: fill_placeholders,
        get_user_books: get_user_books,
        getLoggedInUser: getLoggedInUser,
        delete_book: delete_book,
        delete_confirmation: delete_confirmation,
        edit_book: edit_book,
        hover_card: hover_card,
        toggle_watchlist: toggle_watchlist
    }
});

onPageLoad();