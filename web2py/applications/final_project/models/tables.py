import datetime

def get_user_email():
    return None if auth.user is None else auth.user.email

def get_name():
    return None if auth.user is None else auth.user.first_name + ' ' + auth.user.last_name


# Check if we need it for display the user profile
db.define_table('user_profile',
            Field('user_email',  default=get_user_email()),
            Field('user_name',  default=get_name())
            )

db.define_table('book',
    Field('title', default=''),
    Field('author', default=''),
    Field('price', type='float', default=''),
    Field('edition', type='float', default=''),
    Field('description', type='text', default=''),
    Field('book_condition', default=''),
    # Field('taggi', format='%(name)s'),
    Field('tags', 'list:reference tag')
    # "condition" & "state" are aparently reserved keywords
)


db.define_table('tag',
                 Field('name'),
                 format='%(name)s')
# Interesting to check:
# http://web2py.com/books/default/chapter/29/06/the-database-abstraction-layer#list_types


# ___________________ BOOK VALIDATION ____________________________
db.book.title.requires = IS_NOT_EMPTY(error_message='Title can not be empty')
# down there is just an example
db.book.book_condition.requires = IS_IN_SET(('New','Semi-New', 'Used','Very Used'))
# Should we set a length?
db.book.description.requires = IS_LENGTH(1024) 


# The database still contains stuff form the homework 4,
# At some point do rm ./database