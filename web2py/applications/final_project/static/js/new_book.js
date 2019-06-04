

let add_tag = function () {

    app.tags = [];
    app.tags.push(app.book_title);
    app.tags.push(app.book_topic);
    app.tags.push(app.book_label);

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

