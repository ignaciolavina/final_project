# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
# @auth.requires_login()
def index():
    return dict()

def books():
    # db.book.id.readable = db.book.id.writable = False
    grid = SQLFORM.grid(
        db.book,
        create= True,
        editable = True,
        csv=False
    )
    return dict(grid=grid)


# form for adding a new book
def new_book():
    return dict()

# def user(): return dict(form=auth())

def clear():
    db(db.book).delete()
    db(db.tags).delete()
    return "tags db deleted"


def first():
    if request.vars.visitor_name:
        session.visitor_name = request.vars.visitor_name
        redirect(URL('second'))
    return dict()
    
def second():
    return "redirection"

# NOT Working properly
@auth.requires_login()
def profile():
    user = auth.user

    print (user.email, user.first_name, user.last_name)
    

    # print( auth.first_name)
    # return dict(message='hello %(first_name)s' % auth.user)
    # string = auth.user.email
    # user = db(db.user_profile.user_email == auth.user.email).select().first()
    return dict(name = user)


# Just for testing purposes, for checking the list of tags
# do /default/tags on the browser
def tags():
    # db.tags.id.readable = db.tags.id.writable = False
    query = db.tags
    # fields = (db.tags.name)
    grid = SQLFORM.grid(
        query,
        # fields = fields,
        create= True,
        editable = True,
        csv=False
    )
    return dict(grid=grid)



# # ---- API (example) -----
# @auth.requires_login()
# def api_get_user_email():
#     if not request.env.request_method == 'GET': raise HTTP(403)
#     return response.json({'status':'success', 'email':auth.user.email})




# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
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

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
