
// First function called at page load
let onPageLoad = function () {
    getLoggedInUser(function () {
        getAllBooks();
    });
};

// Function to retrieve all the books to display in the dashboard
let getAllBooks = function () {
    $.getJSON(getAllBooksUrl, function (response) {
        app.books = response.books;
        // processBooks();
    });
};

// NOt used YET
let processBooks = function () {
    let index = 0;
    app.books.map((book) => {
        Vue.set(book, 'index', index++);
    });
};


let getLoggedInUser = function (callback) {
    $.getJSON(getLoggedInUserUrl, function (response) {
        app.loggedInUser = response.user;
        callback();
    });
};

let app = new Vue({
    el: "#app",
    delimiters: ['${', '}'],
    unsafeDelimiters: ['!{', '}'],
    data: {
        books: [],
        loggedInUser: undefined
    },
    methods: {

    }
});

onPageLoad();