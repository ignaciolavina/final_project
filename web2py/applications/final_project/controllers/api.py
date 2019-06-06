def get_logged_in_user():
    user = None if auth.user is None else auth.user.email
    return response.json(dict(user=user))

def get_all_books():
    with_watchlist = (request.vars.with_watchlist == 'true')
    print(type(with_watchlist))
    books = db(db.book).select()
    if (with_watchlist == True):
        to_return = []
        # Iterate back through the books to give their watchlist status for the current user
        for book in books:
            book['watchlist_status'] = False 
            to_return.append(book)
        return response.json(dict(books=to_return))
    else:
        return response.json(dict(books=books))

# Function to toggle to presence of a user_book in the db
def toggle_watchlist():
    book_id = request.vars.book_id
    # Get the current user's ID from the DB
    user_email = request.vars.user_email
    if (user_email == None):
        print("ERROR: No user email found!")
    # Get the current status of the book in the DB
    query = db((db.watchlist.user_email == user_email) & (db.watchlist.book_id == book_id))
    current_book_watchlist = query.select().first()
    # If in the DB, we remove it
    if (current_book_watchlist != None):
        query.delete()
    # If not in the DB, we add it
    else:
        db.watchlist.insert(user_email = user_email, book_id = book_id)
    return response.json(dict())

# Missing all validation
def save_new_book():
    print("save new book API")
    print (request.vars)
    id_book = db.book.update_or_insert (
        title = request.vars.title,
        # Add the rest of the values ti insert
        # WARNING! author pointing "topic", change when needed
        author = request.vars.topic
    )
    print ("id:", id_book)
    book = db.book(db.book.id == id_book)

    list_of_tags = request.vars.getlist('tags[]')

    print ("list of tags" , list_of_tags)
    # For each tag, update or insert in the database
    for tag in list_of_tags:
        print (tag)
    #     # Check if tag is already in the db
    #     # lis_books_for_tag = (db.tags.name == tag).select().book
    #     db.tags.update_or_insert((db.tags.name == tag),
    #         name = tag,            
    #         # book = book reference
    #         # book.push(book_id)
    #     )
    
    # When validation, send respose trhough this boolean var
    # stored_correctly = True
    return response.json(dict()) #stored=stored_correctly))




# HOMEWORK 4 CODE (As guide)
# @auth.requires_login()
# def get_your_review():
#     review = db((db.review.book_id == request.vars.book_id) & (db.review.email == request.vars.email)).select().first()
#     return response.json(dict(review=review))

# @auth.requires_login()
# def save_review():
#     print(request.vars.book_id)
#     print(request.vars.email)
#     db.review.update_or_insert(
#         ((db.review.book_id == request.vars.book_id) & (db.review.email == request.vars.email)),
#         body=request.vars.body,
#         book_id=request.vars.book_id
#     )
#     return "ok"

# def get_other_reviews():
#     if auth.user is None:
#         other_reviews = db(db.review.book_id == request.vars.book_id).select()
#     else:
#         other_reviews = db( (db.review.book_id == request.vars.book_id) & (db.review.email != auth.user.email) ).select()
    
#     return response.json(dict(other_reviews=other_reviews))