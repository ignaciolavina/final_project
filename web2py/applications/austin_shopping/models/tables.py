import datetime

db.define_table('book',
    Field('title'),
    Field('author'),
    Field('price', 'float', default=0),
    Field('stock', 'integer', default=0)
)

db.define_table('cart_entry',
    Field('user_id', 'reference auth_user'),
    Field('book_id', 'reference_book'),
    Field('quantity', 'integer', default=1),
    Field('date_entered', 'datetime', default=datetime.datetime.utcnow())
)