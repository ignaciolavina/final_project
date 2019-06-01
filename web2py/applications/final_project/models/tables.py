def get_user_email():
    return None if auth.user is None else auth.user.email

def get_name():
    return None if auth.user is None else auth.user.first_name + ' ' + auth.user.last_name

db.define_table('book',
    Field('title', default=''),
    Field('author', default=''),
    Field('price', default=''),
    Field('edition', default=''),
    Field('description', default=''),
    Field('book_condition', default='') 
    # "condition" & "state" are aparentrly reserved keywords
)

# Missing validation

# The database still contains stuff form the homework 4,
# At some point do rm ./database