// Function that detects user input on each input-form, and add the 
// correspondent tag, for being stored when click on "Submit"
let add_tag = function () {

    tags = [];
    // Retrieve from the html the tags that we are interested in
    tags.push(app.book_title);
    tags.push(app.book_topic);

    // tags.push(app.book_label);

    // To avoid store in the database empty tags
    // This function removes the tagas that accomplish the condition
    app.tags = tags.filter(function (el) {
        // Condition: empty
        return el != "";
    });

    console.log(app.tags);
}


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
        add_tag: add_tag
    }
});

