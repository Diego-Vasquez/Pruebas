from odoo.tests.common import TransactionCase

class TestBookState(TransactionCase):

    def setUp(self, *args, **kwargs):
        super(TestBookState, self).setUp(*args, **kwargs)
        self.test_book = self.env['library.book'].create({'name': 'Book 1'})
        print("\n\nTest Complete\n\n")

    def test_button_available(self):
        """Make available button"""
        self.test_book.make_available()
        self.assertEqual(self.test_book.state, 'available',
                'Book state should changed to available')
        print("\n\nTest Complete\n\n")

    def test_button_lost(self):
        """Make lost button"""
        self.test_book.make_lost()
        self.assertEqual(self.test_book.state, 'lost',
                'Book state should changed to lost')
        print("\n\nTest Complete\n\n")