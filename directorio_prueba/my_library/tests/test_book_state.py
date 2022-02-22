from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import AccessError
from odoo.tests import common
from odoo.tests.common import Form

#@tagged('-at_install', 'post_install')
class TestBookState(TransactionCase):

    def setUp(self, *args, **kwargs):
        super(TestBookState, self).setUp(*args, **kwargs)
        self.test_book = self.env['library.book'].create({'name': 'Book 1'})

    def test_first(self):
        name='Diego'
        document = self.env['library.book'].create({
            'name': name,
        })

        self.assertTrue(document)
        print('------------TEST OK - CREATE------------')

    '''
    

    def test_button_available(self):
        """Make available button"""
        self.test_book.make_available()
        self.assertEqual(self.test_book.state, 'available',
                'Book state should changed to available')

    def test_button_lost(self):
        """Make lost button"""
        self.test_book.make_lost()
        self.assertEqual(self.test_book.state, 'lost',
                'Book state should changed to lost')
    '''