# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def store():
    links = []

    links.append(
        dict(
            header = 'Buy',
            body = lambda row:
                A('', _href=URL('default', 'create_order', user_signature=True,
                    args=[row.id]), _class='btn btn-primary fa fa-shopping-cart')
                    if auth.user else
                A('', _class='hidden')
        )
    )

    query = db.products

    # fields = ['product_name', 'product_stock','product_description', 'product_price']
    fields = (db.products.product_name, db.products.product_description, db.products.product_stock, db.products.product_price)
    grid = SQLFORM.grid(
        query,
        fields = fields,
        links=links,
        searchable=True, 
        details=False, 
        create=False, 
        deletable=True, 
        editable=False,
        csv=False,
        # user_signature=True,
    )
    return dict(grid = grid)

@auth.requires_login()
def create_order():

    product_id = request.args[0]
    print("product_id_received", product_id)
    
    #how to obtain the session member?
    print("session member:")    
    user = db(db.user_profile.user_email == auth.user.email).select().first()
    # print(user.user_email)
    
    
    product = db(db.products.id == product_id).select().first()
    print(product.product_name)

    if (user is None):
        # user has not a profile
        return redirect(URL('default', 'profile_page', vars=dict(
            next=URL('default', 'create_order', args=[product_id]), edit='y')))

    # else:

    # fields = ['order_email', 'product_id', 'order_quantity', 'order_date', 'order_amount_paid']
    # db.product_orders.product_id.default = product.product_id
    # db.product_orders.order_date.default = datetime.datetime.utcnow()
    else:

        db.orders.order_email.default = auth.user.email
        db.orders.order_email.writable = False
        db.orders.product_id.default = product.id    
        db.orders.product_id.writable = False  
        db.orders.order_date.default =  datetime.datetime.utcnow()    
        db.orders.order_date.writable = False
        db.orders.order_amount_paid.default = product.product_price #* db.orders.order_quantity
        db.orders.order_amount_paid.writable = False
        # db.orders.order_date.readonly = True    
        db.orders.order_quantity.default = 1
        db.orders.order_quantity.requires = IS_INT_IN_RANGE(1, product.product_stock)
        
    # METER SOLO LOS FIELDS QUE QUIERO (NO DATE)
    # METER PRODUCT PRICE, calcular la ampount directamente, etc
        form = SQLFORM(db.orders)
        # readonly_fields = "order_date") #, fields= fields)
        insert_was_succesful = form.process().accepted
        if insert_was_succesful:
            # value = db.orders.insert(order_email = auth.user.email , product_id = product.id, order_date= datetime.datetime.utcnow(), order_amount_paid=product.product_price)
            # # db.orders.update()
            # # db.commit()
            # print ("values: ", value)
            return redirect(URL('default', 'order_list'))
        elif form.errors:
            response.flash = 'could not insert your profile'
        return dict(form=form)


def order_list():
    links = []

    # query = db(db.orders.id == 2).select().first()
    query = db.orders
    # print("QUERYYYY")
    # print(query.length)
    db.orders.order_email.represent = lambda v, r : A(v, _href=URL('default', 'profile_page', vars=dict(email=v)))
    db.orders.product_id.represent = lambda v, r : A(get_product_name(db.products(v)), _href=URL('default', 'product_view', args=[v]))
    
    grid = SQLFORM.grid(
        query,
        links=links,
        searchable=True, 
        details=False, 
        create=False, 
        deletable=True, 
        editable=True,
        csv=False,
        user_signature=True,
    )


    return dict(grid = grid)


def product_view():

    #  id_product sent by args[]
    #  print("request: ", request.args.size)
    print(request.args)
    query = db(db.products.id == request.args[0]).select().first()
    print(query)
    form = SQLFORM(
    db.products, query,
    readonly=True
    )
    return dict(form=form)

    # return "hola"
    # if(len(request.args) != 0):
    #     print(query)
        # return "hols"



# @auth.requires_login()
# def check_profile():
#     user = db(db.user_profile.user_email == auth.user.email).select().first()
#     print("user: ", user)
#     if user == None:        
#         return redirect(URL('default', 'profile_page', vars=dict(
#             next=URL('default', 'store'), edit='y')))
#     else:
#         # to change
#         return redirect(URL('default', 'profile_page'))
#         # return "user has profile, to profile page"


def edit_profile():
    return redirect(URL('default', 'profile_page', vars=dict(
        next=URL('default', 'store'), edit='y')))

@auth.requires_login()
def profile_page():
    
    # print("\n\nrequest vars: ", request.vars)
    # print('\n\n')
    # if request vars = y, then create/edit profile"
    if (request.vars.edit == 'y'):
        db.user_profile.user_email.default = auth.user.email  
        db.user_profile.user_email.writable = False      
        db.user_profile.user_name.default = auth.user.first_name
        db.user_profile.user_name.writable = False
        fields = ['user_email', 'user_name', 'user_street', 'user_city', 'user_zip_code']
        form = SQLFORM(db.user_profile, fields= fields)
        insert_was_succesful = form.process().accepted
        
        if insert_was_succesful:
            print("succesful profile entry, redirecting to ", request.vars.next )
            return redirect(request.vars.next)
        # elif: form.errors:
        #     response.flash = 'could not insert your profile'
        return dict(form=form)          
        
    else:

        user = db(db.user_profile.user_email == auth.user.email).select().first()
        print("user: ", user)

        # If the user is new and is not registered
        if user == None:        
            # send to profile with edit = y
            return redirect(URL('default', 'profile_page', vars=dict(
                next=URL('default', 'store'), edit='y')))
        else:

            form = SQLFORM(
            db.user_profile, user,
            readonly=True,
            deletable = False,
            editable = True
            )
            return dict(form=form)


@auth.requires_login()
def create_product():    

    # print("insert product called")
    fields = ['product_name', 'product_description', 'product_stock', 'product_price']
    # insertr fields
    form = SQLFORM(db.products, fields=fields)
    
    insert_was_succesful = form.process().accepted
    if insert_was_succesful:
        return redirect(URL('default', 'store'))
    elif form.errors:
        response.flash = 'could not insert your product'
    return dict(form=form)


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    # response.flash = T("Hello World")
    # return dict(message=T('Welcome to web2py!'))
    return redirect(URL('default', 'store'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()



# borrar at the end!
def user_profiles_list():
    query = db(db.user_profile)
    grid = SQLFORM.grid(
    query,
    searchable=True, 
    details=False, 
    create=True, 
    deletable=True, 
    editable=True,
    csv=False,
    user_signature=True,
    )
    return dict(grid = grid)

# def myweb():
#     return "www.ignaciolavina.com"
