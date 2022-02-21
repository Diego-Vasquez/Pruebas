from odoo import models, fields, api


class LibraryBookRent(models.Model):
    _name = 'library.book.rent'

    book_id = fields.Many2one('library.book', 'Book', required=True)
    borrower_id = fields.Many2one('res.partner', 'Borrower', required=True)
    state = fields.Selection([('ongoing', 'Ongoing'), ('returned', 'Returned'),('lost', 'Lost')],
                             'State', default='ongoing', required=True)
    rent_date = fields.Date(default=fields.Date.today)
    return_date = fields.Date()
    stage_id = fields.Many2one(
        'library.rent.stage',
        #default=_default_rent_stage,
        group_expand='_group_expand_stages'
    )

    color = fields.Integer()
    popularity = fields.Selection(
        [('no', 'No Demand'), ('low', 'Low Demand'), ('medium', 'Average Demand'), ('high', 'High Demand'), ])
    tag_ids = fields.Many2many('library.rent.tag')

    @api.model
    def _default_rent_stage(self):
        Stage = self.env['library.rent.stage']
        return Stage.search([], limit=1)

    @api.model
    def _group_expand_stages(self, stages, domain, order):
        return stages.search([], order=order)

    '''
    @api.model
    def create(self, vals):
        book_rec = self.env['library.book'].browse(vals['book_id'])  # returns record set from for given id
        book_rec.make_borrowed()
        return super(LibraryBookRent, self).create(vals)
    '''

    @api.model
    def create(self, vals):
        rent = super(LibraryBookRent, self).create(vals)
        if rent.stage_id.book_state:
            rent.book_id.state = rent.stage_id.book_state
        return rent

    def write(self, vals):
        rent = super(LibraryBookRent, self).write(vals)
        if self.stage_id.book_state:
            self.book_id.state = self.stage_id.book_state
        return rent

    def book_return(self):
        self.ensure_one()
        self.book_id.make_available()
        self.write({
            'state': 'returned',
            'return_date': fields.Date.today()
        })

    def book_lost(self):
        self.ensure_one()
        self.sudo().state = 'lost'
        book_with_different_context = self.book_id.with_context(avoid_deactivate=True)
        book_with_different_context.sudo().make_lost()

class LibraryRentWizard(models.TransientModel):
    _name = 'library.rent.wizard'
    borrower_id = fields.Many2one('res.partner',
        string='Borrower')
    book_ids = fields.Many2many('library.book',
        string='Books')

    def add_book_rents(self):
        rentModel = self.env['library.book.rent']

        for wiz in self:
            for book in wiz.book_ids:
                rentModel.create({
                    'borrower_id': wiz.borrower_id.id,
                    'book_id': book.id
                })
        borrowers = self.mapped('borrower_id')
        action = borrowers.get_formview_action()
        if len(borrowers.ids) > 1:
            action['domain'] = [('id', 'in', tuple(borrowers.
                                                   ids))]
        action['view_mode'] = 'tree,form'
        return action

class LibraryRentStage(models.Model):
    _name = 'library.rent.stage'
    _order = 'sequence,name'

    name = fields.Char()
    sequence = fields.Integer()
    fold = fields.Boolean()
    book_state = fields.Selection(
        [('available', 'Available'),
         ('borrowed', 'Borrowed'),
         ('lost', 'Lost')],
        'State', default="available")

class LibraryRentTags(models.Model):
    _name = 'library.rent.tag'

    name = fields.Char()
    color = fields.Integer()

class ResPartner(models.Model):
    _inherit = 'res.partner'

    rent_ids = fields.One2many('library.book.rent', 'borrower_id')