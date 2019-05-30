let processBooks = function () {
    let index = 0;
    app.books.map((b) => {
        Vue.set(b, 'index', index++);
    });
};

let processCartEntries = function () {
    let index = 0;
    app.cart.entries.map((e) => {
        Vue.set(e, 'index', index++);
    });
};

// ------------- store functions -------------------

let getBooks = function () {
    $.getJSON(getBooksUrl, function (response) {
        app.books = response.books;
        processBooks();
    });
};

let getCartEntries = function () {
    if (app.user) {
        $.getJSON(getCartEntriesUrl, function (response) {
            app.cart.entries = response.entries;
            processCartEntries();
        });
    }
};

let getLoggedInUser = function (callback) {
    $.getJSON(getLoggedInUserUrl, function (response) {
        app.user = response.user;
        callback();
    });
};

let onPageLoad = function () {
    getLoggedInUser(function () {
        getBooks();
        getCartEntries();
    });
};

let addToCart = function (bookIndex) {
    let book = app.books[bookIndex];
    $.post(updateCartEntryUrl, {
        user_id: app.user.id,
        book_id: book.id,
        quantity: 1
    }, function (response) {
        book.is_in_cart = true;
        if (!app.cart.entries.includes(response.entry)) {
            app.cart.entries.unshift(response.entry);
            processCartEntries();
        }
    });
};


// ------------- shopping cart functions -------------------------

let updateEntryInDatabase = function (entry) {
    $.post(updateCartEntryUrl, {
        user_id: entry.user_id,
        book_id: entry.book.id,
        quantity: entry.quantity
    });
};

let increaseQuantity = function (cartEntryIndex) {
    let entry = app.cart.entries[cartEntryIndex];
    if (entry.book.stock > entry.quantity) {
        entry.quantity++;
        updateEntryInDatabase(entry);
    }
};

let decreaseQuantity = function (cartEntryIndex) {
    let entry = app.cart.entries[cartEntryIndex];
    if (entry.book.stock > 0 && entry.quantity > 0) {
        entry.quantity--;
        updateEntryInDatabase(entry);
    }
};

let app = new Vue({
    el: "#app",
    delimiters: ['${', '}'],
    unsafeDelimiters: ['!{', '}'],
    data: {
        route: 'store',
        user: undefined,
        books: [],
        cart: {
            entries: [],
            orderTotal: 0
        }
    },
    methods: {
        addToCart: addToCart,
        increaseQuantity: increaseQuantity,
        decreaseQuantity: decreaseQuantity
    }
});

onPageLoad();