{
    'name': 'My Library',
    'summary': "Manage books easily",
    'description': """
    Libreria de prueba
    """,
    'author': "DiegoV",
    'depends': ['base'],
    'data': ['security/groups.xml',
            'security/ir.model.access.csv',
            'views/library_book.xml',
            'views/library_book_rent.xml',
            'views/library_rent_wizard.xml',
            'views/library_book_return_wizard.xml',
            'data/data.xml',
            'data/demo.xml',
             ],

    'demo': [
            'data/demo.xml',
            ],

 }