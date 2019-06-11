import os

def get_logged_in_user():
    user = None if auth.user is None else auth.user
    return response.json(dict(user=user))

def get_all_books():
    with_watchlist = (request.vars.with_watchlist == 'true')
    books = db(db.book).select()
    if (with_watchlist == True):
        to_return = []
        # Iterate back through the books to give their watchlist status for the current user
        for book in books:
            if (book != None):
                book['watchlist_status'] = is_book_on_watchlist(auth.user.email, book.id) 
            to_return.append(book)
        return response.json(dict(books=to_return))
    else:
        return response.json(dict(books=books))

def get_promoted_tags():
    '''Function that returns a dict with the json config object'''
    # ------------Path Setup------------------
    absFilePath = os.path.abspath(__file__)                # Absolute Path of the module
    # print(absFilePath)
    fileDir = os.path.dirname(os.path.abspath(__file__))   # Directory of the Module
    # print(fileDir)
    parentDir = os.path.dirname(fileDir)                   # Directory of the Module directory
    # print(parentDir)
    newPath = os.path.join(parentDir, 'config/config.txt')
    path = open(newPath)
    config = json.load(path)
    path.close()
    return response.json(dict(config=config))

# Internal function for abstraction
def is_book_on_watchlist(user_email, book_id):
    ''' Returns whether a book is on a users watchlist in the db'''
    query = db((db.watchlist.user_email == user_email) & (db.watchlist.book_id == book_id))
    current_book_watchlist = query.select().first()
    if (current_book_watchlist != None):
        return True
    else:
        return False

# Function to toggle to presence of a user_book in the db
def toggle_watchlist():
    book_id = request.vars.book_id
    # Get the current user's ID from the DB
    user_email = request.vars.user_email
    if (user_email == None):
        print("ERROR: No user email found!")
    # Get the current status of the book in the DB
    query = db((db.watchlist.user_email == user_email) & (db.watchlist.book_id == book_id))
    # If in the DB, we remove it
    if (is_book_on_watchlist(user_email, book_id)):
        query.delete()
    # If not in the DB, we add it
    else:
        db.watchlist.insert(user_email = user_email, book_id = book_id)
    return response.json(dict())


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

    # Now, we need to retrieve the list of tags from request.vars
    list_of_tags = request.vars.getlist('tags[]')

    # *********************BOOK INSERTION************************** #
    # First, insert the book retreiving the atributes from the request.vars    
    # id_book = db.book.update_or_insert (
    id_book = db.book.insert (
        # r = request.vars
        title = request.vars.title,
        author = request.vars.topic,
        price = request.vars.price,
        book_condition = request.vars.condition,
        description = request.vars.description,
        course = request.vars.course,
        


        #         book_title: app.book_title,
        # book_author: app.book_author,
        # book_price: app.book_price,
        # book_condition: app.book_condition,
        # book_course: app.book_course,
        # book_topic: app.book_topic,
        # book_description: app.book_description,
        # tags: app.tags

        tags = list_of_tags
    )    
    # id_book contains the id of the book that we have just inserted in the db
    book = db.book(db.book.id == id_book)
    print ("New book stored:", book)

    # *********************ASIGN BOOK TO USER INSERTION************************** #
    db.book_owner.insert (
        book_id = id_book,
        user_id = auth.user.id
    )

    # *********************TAGS INSERTION************************** #
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
    search_string = request.vars.search_string
    if (search_string == ''):
        result = db(db.book).select()
        return response.json(dict(books=result))

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
    # print("requests" , request.vars)
    last_name = request.vars.last_name
    first_name = request.vars.first_name
    
    # auth.user.first_name = first_name
    # Selecting the user to update
    query = db(db.auth_user.id == auth.user_id).select().first()
    query.update_record(first_name=first_name, last_name=last_name)
    # To change menu
    auth.user.first_name = first_name
    print ("auth:", auth.user)
    
    return response.json(dict())

def get_user_books():
    books = []
    rows = db(db.book_owner.user_id == auth.user.id).select()
    for row in rows:
        book_ret = db(db.book.id == row.book_id).select().first()
        books.append(book_ret)
    return response.json(dict(books = books))
