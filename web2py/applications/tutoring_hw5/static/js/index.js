let processBooks = function() {
    let index = 0;
    app.books.map((book) => {
        Vue.set(book, 'index', index++);
        Vue.set(book, 'showReviews', false);
        Vue.set(book, 'otherReviews', []);
        Vue.set(book, 'yourReview', { rating: 0, numStars: 0 });
    });
};

let getAllBooks = function() {
    $.getJSON(getAllBooksUrl, function(response) {
        app.books = response.books;
        processBooks();
        console.log(app.books)
    });
};

let getLoggedInUser = function(callback) {
    $.getJSON(getLoggedInUserUrl, function(response) {
        app.loggedInUser = response.user;
        callback();
    });
};

let onPageLoad = function() {
    getLoggedInUser(function() {
        getAllBooks();
    });
};

let getYourReview = function(bookIndex) {
    // exit the function if the user is not logged in
    if (app.loggedInUser == undefined) {
        return;
    }

    let book = app.books[bookIndex];

    $.getJSON(getYourReviewUrl, { book_id: book.id, email: app.loggedInUser }, function(response) {
        if (response.review != null) {
            book.yourReview.rating = response.review.rating;
            book.yourReview.numStars = response.review.rating;
        }
    });
};

let getOtherReviews = function(bookIndex) {
    let book = app.books[bookIndex];
    $.getJSON(getOtherReviewsUrl, { book_id: book.id }, function(response) {
        book.otherReviews = response.other_reviews;
    });
};

let toggleReviewsSection = function(bookIndex) {
    let book = app.books[bookIndex];
    book.showReviews = !book.showReviews;
};

let hoverStar = function(bookIndex, starNum) {
    let book = app.books[bookIndex];
    book.yourReview.numStars = starNum;
};

let leaveStarRow = function(bookIndex) {
    let book = app.books[bookIndex];
    book.yourReview.numStars = book.yourReview.rating;
};

let clickStar = function(bookIndex, starNum) {
    let book = app.books[bookIndex];
    book.yourReview.rating = starNum;
    $.post(updateStarUrl, {
        book_id: book.id,
        email: app.loggedInUser,
        rating: starNum
    }, function() {
        let sum = 0
        let length = book.otherReviews.length + 1;
        for (let i = 0; i < book.otherReviews.length; i++) {
            if (book.otherReviews[i].rating == 0) {
                length--;
            } else {
                sum += book.otherReviews[i].rating;
            }
        }
        if (book.yourReview.rating == 0) {
            length --;
        } else {
            sum += book.yourReview.rating;
        }

        book.avg_rating = sum / length;
    });
};

let app = new Vue({
    el: "#app",
    delimiters: ['${', '}'],
    unsafeDelimiters: ['!{', '}'],
    data: {
        books: [],
        starIndices: [1, 2, 3, 4, 5],
        loggedInUser: undefined,
    },
    methods: {
        getYourReview: getYourReview,
        toggleReviewsSection: toggleReviewsSection,
        hoverStar: hoverStar,
        leaveStarRow: leaveStarRow,
        clickStar: clickStar
    }
});

onPageLoad();