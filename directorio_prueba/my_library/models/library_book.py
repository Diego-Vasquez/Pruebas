from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _
from odoo.tests.common import Form

class LibraryBook(models.Model):
    _name = 'library.book'
    manager_remarks = fields.Text('Manager Remarks')
    _description = 'Library Book'
    _rec_name = 'short_name'
    _order = 'short_name, name, lastname, date_release, author_ids'
    active = fields.Boolean(default=True)
    name = fields.Char('Title of Book', required=True)
    lastname = fields.Char('Lastname')
    short_name = fields.Char('Short Title', required=False)
    date_release = fields.Date('Release Date')
    date_updated = fields.Datetime('Last Updated')
    out_of_print = fields.Boolean('Out of Print?')
    indicador = fields.Boolean('Indicador?')
    color = fields.Integer()
    cost_price = fields.Float(
        'Book Cost', digits='precision')
    author_ids = fields.Many2many(
        'res.partner',
        string='Authors'
    )

    #is_public = fields.Boolean(groups='my_library.group_library_librarian')
    #private_notes = fields.Text(groups='my_library.group_library_librarian')

    def book_rent(self):
        self.ensure_one()

        if self.state != 'available':
            raise UserError(_('Book is not available for renting '))
        rent_as_superuser = self.env['library.book.rent'].sudo()
        rent_as_superuser.create({
            'book_id': self.id,
            'borrower_id': self.env.user.partner_id.id,
        })

    num_1= fields.Float('numero 1', digits='precision')
    num_2 = fields.Float('numero 2', digits='precision')
    num_3= fields.Float(string='numero 3', compute='_compute_number3')

    currency_id = fields.Many2one('res.currency', string='Currency')
    retail_price = fields.Monetary(
        'Retail Price')  # optional attribute: currency_field='currency_id' incase currency field have another name then 'currency_id'

    publisher_id = fields.Many2one('res.partner', string='Publisher',
                                   # optional:
                                   ondelete='set null',
                                   context={},
                                   domain=[],
                                   )
    category_id = fields.Many2one('library.book.category')



    state = fields.Selection(
        [('draft', 'Not Available'),
         ('available', 'Available'),
         ('lost', 'Lost'),('borrowed', 'Borrowed')],
        'State')


    notes = fields.Text('Internal Notes')
    description = fields.Html('Description', sanitize=True, strip_style=False)
    cover = fields.Binary('Book Cover')
    pages = fields.Integer('Number of Pages',
        groups='base.group_user',
        states={'lost': [('readonly', True)]},
        help='Total book page count', company_dependent=False)
    reader_rating = fields.Float(
        'Reader Average Rating',
        digits=(14, 4),  # Optional precision (total, decimals),
    )

    def name_get(self):
        """ This method used to customize display name of the record """
        result = []
        for record in self:
            rec_name = "%s (%s)" % (record.name, record.date_release)
            result.append((record.id, rec_name))
        return result

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
        self.ensure_one()
        self.state = 'lost'
        if not self.env.context.get('avoid_deactivate'):
            self.active = False

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



    '''
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
'''

    '''or
        def predicate(book):
        if len(book.author_ids) > 1:
            return True
    

    return False'''

    @api.model
    def create(self, values):
        '''
        if not self.user_has_groups('my_library.acl_book_librarian'):
            if 'manager_remarks' in values:
                raise UserError(
                    'You are not allowed to modify '
                    'manager_remarks'
                )'''
        temp=super(LibraryBook, self).create(values)
        temp.state='available'
        return temp

    def return_all_books(self):
        self.ensure_one()
        wizard = self.env['library.return.wizard']
        with Form(wizard) as return_form:
            return_form.borrower_id = self.env.user.partner_id
            record = return_form.save()
            record.books_returns()

    def write(self, values):
        '''
        if not self.user_has_groups('my_library.acl_book_librarian'):
            if 'manager_remarks' in values:
                raise UserError(
                    'You are not allowed to modify '
                    'manager_remarks'
                )'''

        return super(LibraryBook, self).write(values)


class LibraryMember(models.Model):
    _name = 'library.member'
    _inherits = {'res.partner': 'partner_id'}
    partner_id = fields.Many2one('res.partner',ondelete='cascade')
    date_start = fields.Date('Member Since')
    date_end = fields.Date('Termination Date')
    member_number = fields.Char()
    date_of_birth = fields.Date('Date of birth')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    published_book_ids = fields.One2many('library.book', 'publisher_id', string='Published Books')
    authored_book_ids = fields.Many2many(
        'library.book',
        string='Authored Books',
        # relation='library_book_res_partner_rel'  # optional
    )