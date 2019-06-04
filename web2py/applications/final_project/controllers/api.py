def get_logged_in_user():
    user = None if auth.user is None else auth.user.email
    return response.json(dict(user=user))

def get_all_books():
    books = db(db.book).select()
    return response.json(dict(books=books))



# Missing all validation
def save_new_book():
    db.book.update_or_insert (
        title = request.vars.title,
        # Add the rest of the values ti insert
        # WARNING! author pointing "topic", change when needed
        author = request.vars.topic
    )

    list_of_tags = request.vars.tags
    # For each tag, update or insert in the database
    # for tag in list_of_tags:
    #     # Check if tag is already in the db
    #     db.tags.update_or_insert((db.tags.name = request.vars.tag),
    #         name = request.vars.tag,
    #         # book = book reference
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