//  This function allows to add some properties to each product that will be used for the properly display of the product
let processProducts = function () {
    let index = 0;
    app.products.map((product) => {
        Vue.set(product, 'index', index++);
        Vue.set(product, 'showReviews', false);
        Vue.set(product, 'yourReview', { body: '', rating: 0, numStars: 0 });
        Vue.set(product, 'otherReviews', []);
        Vue.set(product, 'isHidden', false);
    });
};

// This function is called at the beggining, to retrieve all the prodcuts in the database
// For that it makes a query to the server, (trhough api, get_all_products)
let getAllProducts = function () {
    $.getJSON(getAllProductsUrl, function (response) {
        app.products = response.products;
        processProducts();
    });
};

let getLoggedInUser = function (callback) {
    $.getJSON(getLoggedInUserUrl, function (response) {
        app.loggedInUser = response.user;
        callback();
    });
};

let onPageLoad = function () {
    getLoggedInUser(function () {
        getAllProducts();
    });
};

let getYourReview = function (productIndex) {
    // exit the function if the user is not logged in
    if (app.loggedInUser == undefined) {
        return;
    }

    let product = app.products[productIndex];

    $.getJSON(getYourReviewUrl, { product_id: product.id, email: app.loggedInUser }, function (response) {
        if (response.review != null) {
            product.yourReview = response.review;
            product.yourReview.rating = response.review.rating;
            product.yourReview.numStars = response.review.rating;
        }
        Vue.set(product.yourReview, 'hasBeenSaved', false);
    });
};

let getOtherReviews = function (productIndex) {
    let product = app.products[productIndex];
    $.getJSON(getOtherReviewsUrl, { product_id: product.id }, function (response) {
        product.otherReviews = response.other_reviews;
    });
};

let toggleReviewsSection = function (productIndex) {
    let product = app.products[productIndex];

    products = app.products;
    products.forEach(p => {
        p.showReviews = false;
    });

    product.showReviews = !product.showReviews;
};

let saveReview = function (productIndex) {
    // exit the function if the user is not logged in
    if (app.loggedInUser == undefined) {
        return;
    }

    let product = app.products[productIndex];
    let yourReview = product.yourReview;
    yourReview.hasBeenSaved = false;

    $.post(saveReviewUrl, {
        product_id: product.id,
        email: app.loggedInUser,
        body: yourReview.body
    }, function (response) {
        yourReview.hasBeenSaved = true;
        setTimeout(function () {
            yourReview.hasBeenSaved = false;
        }, 1000);
    });
};

let hoverStar = function (productIndex, starNum) {
    let product = app.products[productIndex];
    product.yourReview.numStars = starNum;
};

let leaveStarRow = function (productIndex) {
    let product = app.products[productIndex];
    product.yourReview.numStars = product.yourReview.rating;
};


let clickStar = function (productIndex, starNum) {
    let product = app.products[productIndex];
    product.yourReview.rating = starNum;
    $.post(updateStarUrl, {
        product_id: product.id,
        email: app.loggedInUser,
        rating: starNum
    }, function () {
        let sum = 0
        let length = product.otherReviews.length + 1;
        for (let i = 0; i < product.otherReviews.length; i++) {
            if (product.otherReviews[i].rating == 0) {
                length--;
            } else {
                sum += product.otherReviews[i].rating;
            }
        }
        if (product.yourReview.rating == 0) {
            length--;
        } else {
            sum += product.yourReview.rating;
        }

        product.avg_rating = sum / length;
    });
};


let closeReview = function (productIndex) {
    let product = app.products[productIndex];
    product.showReviews = false;
};

let do_search = function () {
    $.getJSON(search_url,
        { search_string: app.search_string },
        function (data) {
            app.strings = data.strings;
            // self.vue.products = data.products;
            app.products = data.strings;
        });
};

let app = new Vue({
    el: "#app_two",
    delimiters: ['${', '}'],
    unsafeDelimiters: ['!{', '}'],
    data: {
        products: [],
        starIndices: [1, 2, 3, 4, 5],
        loggedInUser: undefined,
        search_string: '',
        strings: []
    },
    methods: {
        getYourReview: getYourReview,
        toggleReviewsSection: toggleReviewsSection,
        saveReview: saveReview,
        hoverStar: hoverStar,
        leaveStarRow: leaveStarRow,
        clickStar: clickStar,
        getAllProducts: getAllProducts,
        processProducts: processProducts,
        closeReview: closeReview
    }
});

onPageLoad();