// Function that detects user input on each input-form, and add the 
// correspondent tag, for being stored when click on "Submit"


let add_tag = function () {

    tags = [];
    // Retrieve from the html the tags that we are interested in
    tags.push(app.book_title.toLowerCase());
    tags.push(app.book_author.toLowerCase());
    tags.push(app.book_course.toLowerCase());
    tags.push(app.book_topic.toLowerCase());
    tags.push(app.book_tag1.toLowerCase());
    tags.push(app.book_tag2.toLowerCase());
    tags.push(app.book_tag3.toLowerCase());


    // To avoid store in the database empty tags
    // This function removes the tagas that accomplish the condition
    app.tags = tags.filter(function (el) {
        // Condition: empty
        return el != "";
    });

    console.log(app.tags);
}

let save_new_book = function () {
    console.log("save book");

    $.post(save_new_book_url, {
        // Book atributes
        title: app.book_title,
        author: app.book_author,
        price: app.book_price,
        book_condition: app.book_condition,
        course: app.book_course,
        topic: app.book_topic,
        description: app.book_description,
        tags: app.tags
        // tags: []

        // topic: app.book_topic,
        // List of tags
        // Only for testing!
        // title: 'bookX',
        // topic: 'topic_test',
        // tags: testing_list

        // User
        //user: ...
    }, function (response) {

        // for implementing a sping load bar
        setTimeout(function () {
            // alert("Book added correctly!");
            // yourReview.hasBeenSaved = false;
        }, 1000);
    }
    )
}


let getLoggedInUser = function (callback) {
    $.getJSON(getLoggedInUserUrl, function (response) {
        app.loggedInUser = response.user;
        callback();
    });
};

let app = new Vue({
    el: "#vue_new_book",
    delimiters: ['${', '}'],
    unsafeDelimiters: ['!{', '}'],
    data: {
        book_title: '',
        book_author: '',
        book_price: '',
        book_condition: '',
        book_course: '',
        book_topic: '',
        book_description: '',
        book_label: '',
        book_tag1: '',
        book_tag2: '',
        book_tag3: '',
        tags: []
    },
    methods: {
        add_tag: add_tag,
        save_new_book: save_new_book,
        getLoggedInUser: getLoggedInUser
    }
});

