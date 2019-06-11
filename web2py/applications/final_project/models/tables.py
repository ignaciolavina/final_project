import datetime

def get_user_email():
    return None if auth.user is None else auth.user.email

def get_name():
    return None if auth.user is None else auth.user.first_name # + ' ' + auth.user.last_name

def get_current_time():
    return datetime.datetime.today

# TO DO, Set primary keys and foreign keys


# Check if we need it for display the user profile CURRENTLY UNUSED
db.define_table('user_profile',
            Field('user_email',  default=get_user_email()),
            Field('user_name',  default=get_name())
            )


db.define_table('book',
    # User who have created the book
    # "user" a keyword RESERVED
    # Field('user', default=''),
    Field('title', type='string', default=''),
    Field('author', type='string', default=''),
    Field('price', type='float', default=''),
    Field('edition', type='text', default=''),
    Field('book_condition', default=''),
    Field('course', type='text', default=''),
    Field('topic', type='text', default=''),
    Field('description', type='text', default=''),
    Field('tags', 'list:string')
    # "condition" & "state" are aparentrly reserved keywords
    
)


db.define_table('book_owner',
            Field('user_id'), # references user?,
            Field('book_id', 'reference book')
)


db.define_table('watchlist',
    Field('user_email', default=get_user_email()),
    Field('book_id', 'reference book'),
    Field('time_watched', type='datetime', default=get_current_time())
)

# Tags is a table that has a name, and a list of books that contain that tag
db.define_table('tags',
    Field('name',  type='string', default=''), # Primary key?! SO no two tags with same name
    # Field('books', 'list:reference book')
    Field('books', 'list:reference book')
    # primarykey = ['name']
)


# db.define_table('tag',
#                  Field('name'),
#                  format='%(name)s')
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