def get_user_email():
    return None if auth.user is None else auth.user.email

def get_name():
    return None if auth.user is None else auth.user.first_name + ' ' + auth.user.last_name

db.define_table('book',
    Field('title', default=''),
    Field('author', default='')
)

db.define_table('review',
    Field('book_id', 'reference book'),
    Field('rating', 'integer', default=0),
    Field('email', default=get_user_email()),
    Field('name', default=get_name())
)