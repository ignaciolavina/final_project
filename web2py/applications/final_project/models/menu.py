# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    (T('Home'), False, URL('default', 'index'), []),
    (T('Books'), False, URL('default', 'books'), []),
    (T('Add Book'), False, URL('default', 'new_book3'), []),
    (T('Add Book2'), False, URL('default', 'new_book'), []),
    (T('Profile'), False, URL('default', 'profile'), []),
    (T('Tags (testing)'), False, URL('default', 'tags'), [])
]

# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. you can remove everything below in production
# ----------------------------------------------------------------------------------------------------------------------

if not configuration.get('app.production'):
    _app = request.application
    response.menu += []

