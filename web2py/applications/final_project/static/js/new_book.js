// Function that detects user input on each input-form, and add the 
// correspondent tag, for being stored when click on "Submit"
let add_tag = function () {

    tags = [];
    // Retrieve from the html the tags that we are interested in
    tags.push(app.book_title);
    tags.push(app.book_topic);

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
    dict = {
        tagy: app.tags
    }
    $.post(save_new_book_url, {
        // Book atributes
        title: app.book_title,
        topic: app.book_topic,
        // List of tags
        tags: app.tags,
        tagy: dict
        // User
        //user: ...
    }, function (response) {

        // for implementing a sping load bar
        setTimeout(function () {
            alert("Book added correctly!");
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
        book_topic: '',
        book_label: '',
        tags: []
    },
    methods: {
        add_tag: add_tag,
        save_new_book: save_new_book,
        getLoggedInUser: getLoggedInUser
    }
});

