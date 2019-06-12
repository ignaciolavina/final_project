
// First function called at page load
let onPageLoad = function () {
    getLoggedInUser(function () {
        getAllBooks(function () {
            getPromotedBooks({});
        });
    });
};

// Function to retrieve all the books to display in the dashboard
let getAllBooks = function (callback) {
    $.getJSON(getAllBooksUrl, {
        // Whether we want a watchlist icon appended to these or not
        with_watchlist: (app.loggedInUser != undefined)
    },
        function (response) {
            app.books = response.books;
            processBooks();
            callback();
        });
};

// Processes the books and adds an index to each one
let processBooks = function () {
    let index = 0;
    app.books.map((book) => {
        Vue.set(book, 'index', index++);
        Vue.set(book, 'is_watchlisted', book.watchlist_status)
    });
};

// Function gets the currently logged in user and stores it in a reactive variable called loggedInUser
let getLoggedInUser = function (callback) {
    $.getJSON(getLoggedInUserUrl, function (response) {
        app.loggedInUser = response.user;
        callback();
    });
};

// Function to get the promoted books and display them
let getPromotedBooks = function () {
    
}

let do_search = function () {
    $.getJSON(search_url,
        { search_string: app.search_string },
        function (data) {
            app.strings = data.strings;
            // self.vue.products = data.products;
            app.books = data.books;

        });
};

let hover_card = function () {
    console.log("hover")
};

let toggle_watchlist = function (bookIndex) {
    let book = app.books[bookIndex];
    let new_status = !book.is_watchlisted;
    book.is_watchlisted = new_status;
    $.post(toggle_watchlist_url, {
        // Book ID
        book_id: book.id,
        // User ID
        user_email: app.loggedInUser.email
    }, function (response) {

        // for implementing a sping load bar
        setTimeout(function () {
            alert("Book added to watchlist correctly!");
        }, 1000);
    }
    )
};

let app = new Vue({
    el: "#app",
    delimiters: ['${', '}'],
    unsafeDelimiters: ['!{', '}'],
    data: {
        books: [],
        promoted_books: [],
        search_string: '',
        loggedInUser: undefined
    },
    methods: {
        toggle_watchlist: toggle_watchlist,
        hover_card: hover_card
    }
});

onPageLoad();