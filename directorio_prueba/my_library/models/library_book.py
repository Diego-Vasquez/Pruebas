from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _

class LibraryBook(models.Model):
    _name = 'library.book'
    manager_remarks = fields.Text('Manager Remarks')
    _description = 'Library Book'
    _rec_name = 'short_name'
    _order = 'short_name, name, lastname, date_release, author_ids'

    name = fields.Char('Title of Book', required=True)
    lastname = fields.Char('Lastname', required=True)
    short_name = fields.Char('Short Title', required=True)
    date_release = fields.Date('Release Date')
    date_updated = fields.Datetime('Last Updated')
    out_of_print = fields.Boolean('Out of Print?')
    indicador = fields.Boolean('Indicador?')
    cost_price = fields.Float(
        'Book Cost', digits='precision')
    author_ids = fields.Many2many(
        'res.partner',
        string='Authors'
    )



    num_1= fields.Float('numero 1', digits='precision')
    num_2 = fields.Float('numero 2', digits='precision')
    num_3= fields.Float(string='numero 3', compute='_compute_number3')

    category_id = fields.Many2one('library.book.category')

    state = fields.Selection(
        [('draft', 'Not Available'),
         ('available', 'Available'),
         ('lost', 'Lost')],
        'State')


    @api.depends('num_1', 'num_2')
    def _compute_number3(self):

        for i in self:
            if i.num_1 and i.num_2:
                i.num_3= i.num_1+i.num_2
            elif i.num_1:
                i.num_3= i.num_1
            elif i.num_2:
                i.num_3= i.num_2
            else:
                i.num_3=0

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('draft', 'available'),
                   ('available', 'borrowed'),
                   ('borrowed', 'available'),
                   ('available', 'lost'),
                   ('borrowed', 'lost'),
                   ('lost', 'available')]
        return (old_state, new_state) in allowed

    def change_state(self, new_state):
        for book in self:
            if book.is_allowed_transition(book.state,new_state):
                book.state = new_state
            else:
                msg = _('Moving from %s to %s is not allowed') % (book.state, new_state)
                raise UserError(msg)

    def make_available(self):
        self.change_state('available')

    def make_borrowed(self):
        self.change_state('borrowed')

    def make_lost(self):
        self.change_state('lost')

    @api.onchange('name')
    def cambio(self):
        if self.name == 'Diego':
            self.lastname='Vasquez'

    def log_all_library_members(self):

        # This is an empty recordset of model library.member
        library_member_model = self.env['library.member']
        all_members = library_member_model.search([])
        print("ALL MEMBERS:", all_members)
        return True

    def change_release_date(self):
        self.ensure_one()
        self.date_release = fields.Date.today()
        '''
        self.update({
        'date_release': fields.Datetime.now(),
        'another_field': 'value'
        ...
        })
        '''

    def find_book(self):
        domain = [
            '&', ('name', 'ilike', 'Hola2'),
                ('cost_price', '=', 13.21)]
        books = self.search(domain)

        if books:
            print("\n\n\nPrueba1 funciona\n\n\n")
            print(books)

        for i in books:
            i.indicador = True

    def predicate(book):
        if len(book.author_ids) > 1:
            return True

    @api.model
    def books_with_multiple_authors(self, all_books):
        return all_books.filter(predicate)

    @api.model
    def expensive_books(self, all_books):
        def predicate(book):
            if len(book.cost_price) > 0.54:
                return True

        return all_books.filter(predicate)

    @api.model
    def cheaper_books(self, all_books):
        def predicate(book):
            if len(book.cost_price) <1:
                return True

        return all_books.filter(predicate(all_books))

    def prueba_2(self):
        conj1=self.expensive_books(self)
        conj2=self.cheaper_books(self)

        if conj1+conj2:
            print("\n\n\nPrueba2 funciona\n\n\n")
            print(conj1+conj2)

        for i in conj1+conj2:
            i.indicador = True


    '''or
        def predicate(book):
        if len(book.author_ids) > 1:
            return True
    

    return False'''

    @api.model
    def create(self, values):
        if not self.user_has_groups('my_library.acl_book_librarian'):
            if 'manager_remarks' in values:
                raise UserError(
                    'You are not allowed to modify '
                    'manager_remarks'
                )

        return super(LibraryBook, self).create(values)

    def write(self, values):
        if not self.user_has_groups('my_library.acl_book_librarian'):
            if 'manager_remarks' in values:
                raise UserError(
                    'You are not allowed to modify '
                    'manager_remarks'
                )

        return super(LibraryBook, self).write(values)


class LibraryMember(models.Model):
    _name = 'library.member'
    _inherits = {'res.partner': 'partner_id'}
    partner_id = fields.Many2one('res.partner',ondelete='cascade')
    date_start = fields.Date('Member Since')
    date_end = fields.Date('Termination Date')
    member_number = fields.Char()
    date_of_birth = fields.Date('Date of birth')
