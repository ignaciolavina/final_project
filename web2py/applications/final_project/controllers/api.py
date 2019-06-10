def get_logged_in_user():
    user = None if auth.user is None else auth.user
    return response.json(dict(user=user))

def get_all_books():
    books = db(db.book).select()
    return response.json(dict(books=books))




''' Save_new_book is a function that does two main things:
- Add a new book to the database (parameters sent by the client in request.vars)
- For each tag:
    - Add the tag to the database (if not exist)
    - Add to the list of books of that tag, the new book inserted
'''
# Missing all validation
def save_new_book():
    print("\nsave new book API")
    # print ("request.vars=>", request.vars)


    # *********************BOOK INSERTION************************** #
    # First, insert the book retreiving the atributes from the request.vars    
    # id_book = db.book.update_or_insert (
    id_book = db.book.insert (
        title = request.vars.title,
        # Add the rest of the values ti insert
        # WARNING! author pointing "topic", change when needed
        author = request.vars.topic
    )    
    # id_book contains the id of the book that we have just inserted in the db
    book = db.book(db.book.id == id_book)
    print ("New book stored:", book)


    # *********************TAGS INSERTION************************** #
    # Now, we need to retrieve the list of tags from request.vars
    list_of_tags = request.vars.getlist('tags[]')
    # print ("list of tags" , list_of_tags)

    # For each tag, update or insert in the database
    # pointing the book that we have inserted
    for tag in list_of_tags:
        # print (tag)
        # Check if tag is already in the db
        tag_id = db.tags.update_or_insert(
            db.tags.name == tag,
            name = tag
            # books.push(id_book) #doesn't work
            # books = id_book
            )
        # in case of update, tag_id will be None, so we need to ensure having value on tag_id
        # if tag_id is None:
        #     tag_id = db(db.tags.name == tag).select().first().id_book

        tag_object = db(db.tags.name == tag).select().first()
        # print("\ntag Object", tag_object)

        # first, we try to retrieve the current list of books for that tag (if exist, otherwhise we create an array)
        list_books_for_tag = tag_object.books 
        if list_books_for_tag is None:
            list_books_for_tag = []
        # Adding the new book (by id)
        # Now list_books_for_tag contains the books that already had + the new book
        list_books_for_tag.append(id_book)       

        # updating the entry (list of books) on the database
        db.tags.update_or_insert(db.tags.name == tag,
            books = list_books_for_tag
        )

    # When validation, send respose trhough this boolean var
    # stored_correctly = True
    return response.json(dict()) #stored=stored_correctly))


# Method that receives trhough the request vars an string that the user has input on the search var
# And retrieves only the products that match part of that string
def search():
    tags = db(db.tags).select()
    # Obtaining the string of the search var from the request vars
    search_string = request.vars.search_string or ''

    # result[] is the variable to send back (contains a list of books)
    result = []
   
    # Search in db where tag like '%string%'
    string_query = ('%' + search_string.lower() + '%')
    tags_that_match = db(db.tags.name.like(string_query)).select(groupby=db.tags.name)

    # each tag represent a tag that contains the search string
    id_of_books_visited = []
    for tag in tags_that_match:
        # for each tag, we visit all the books
        for book in tag.books:
            # if the book has not been visited yet
            if book not in id_of_books_visited:
                # print('not in')
                id_of_books_visited.append(book)
                # print('id founded', book)
                result.append(db(db.book.id == book).select().first())

    # for r in result:
    #     print('r', r)
    return response.json(dict(books=result))

def save_profile():
    print ("saving_profile")
    user = request.vars.user
    print("requests" , request.vars)
    # print (user.last_name)
    # auth.user.first_name = request.vars.user.first_name 
    # print ("auth user", auth.user.last_name)
    
    query = db(db.auth_user.id == auth.user_id).select().first()
    print("query: ", query)
    # db(db.auth_user.id == auth.user_id).update(last_name=request.vars.last_name, first_name= request.vars.first_name)
    db.update(db.auth_user.id == auth.user_id, last_name=request.vars.last_name, first_name= request.vars.first_name)

    # db.auth_user.update(db.auth_user.id == auth.user_id, last_name="my new")
    # query.update_record(last_name=request.vars.last_name)
    # , first_name=request.vars.first_name)
    print ("auth:", auth.user)
    
    return response.json(dict())


