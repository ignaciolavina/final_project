# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.


import datetime

def get_user_id():
    return None if auth.user is None else auth.user.id

def get_product_name(p):
    return None if p is None else p.product_name


db.define_table('products',
                Field('product_name'),
                Field('product_stock', 'integer'),
                Field('product_price', 'float'),
                Field('product_description'),   # set to text?!
                # Field('product_sold', 'integer',  default = 0),
                # Field('product_cost', 'float'),
                Field('user_id', 'reference auth_user', default=get_user_id())
                )

db.products.product_name.requires = IS_NOT_EMPTY(error_message='Product name cannot be empty')
db.products.product_stock.requires = IS_INT_IN_RANGE(0, None, error_message='missing, negative or too large!')
# db.products.product_sold.requires = IS_INT_IN_RANGE(0, None, error_message='negative or too large!')
db.products.product_price.requires = IS_FLOAT_IN_RANGE(0, None, error_message='negative or too large!')
# db.products.product_cost.requires = IS_FLOAT_IN_RANGE(0, None, error_message='negative or too large!')



db.define_table('user_profile',
                Field('user_email',  default=get_user_id()),
                Field('user_name'),
                Field('user_street'),
                Field('user_city'),   
                Field('user_zip_code')
                )

db.user_profile.user_street.requires = IS_NOT_EMPTY(error_message='Field name cannot be empty')
db.user_profile.user_city.requires = IS_NOT_EMPTY(error_message='Field name cannot be empty')
db.user_profile.user_zip_code.requires = IS_NOT_EMPTY(error_message='Field cannot be empty')


db.define_table('orders',
                Field('order_email'),
                Field('product_id'),
                Field('order_quantity'),
                Field('order_date', 'datetime'), #Get date as default
                Field('order_amount_paid', 'float')
                )




# after defining tables, uncomment below to enable auditing
auth.enable_record_versioning(db)
