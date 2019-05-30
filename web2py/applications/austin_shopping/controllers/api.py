def get_logged_in_user():
    return response.json(dict(user=auth.user))

def get_books():
    books = db(db.book).select()

    if auth.user is not None:
        for b in books:
            cart_entry = db( (db.cart_entry.book_id == b.id) & (db.cart_entry.user_id == auth.user.id) ).select().first()
            b.is_in_cart = cart_entry is not None

    return response.json(dict(books=books))

@auth.requires_login()
def get_cart_entries():
    entries = db(db.cart_entry.user_id == auth.user.id).select(orderby=~db.cart_entry.date_entered)

    for e in entries:
        e.book = db(db.book.id == e.book_id).select().first()

    return response.json(dict(entries=entries))

@auth.requires_login()
def update_cart_entry():
    db.cart_entry.update_or_insert(
        ( (db.cart_entry.book_id == request.vars.book_id) & (db.cart_entry.user_id == auth.user.id) ),
        user_id=request.vars.user_id,
        book_id=request.vars.book_id,
        quantity=request.vars.quantity
    )

    entry = db( (db.cart_entry.book_id == request.vars.book_id) & (db.cart_entry.user_id == auth.user.id) ).select().first()
    entry.book = db(db.book.id == request.vars.book_id).select().first()

    return response.json(dict(entry=entry))