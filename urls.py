"""
Page controller module. To add controller for path - add tuple(path, callable) to urls
variable
"""


from views import index_view, contacts_view, address_view

urls = [
    ('/', index_view),
    ('/contact/', contacts_view),
    ('/address/', address_view)
]
