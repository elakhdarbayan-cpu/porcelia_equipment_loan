from odoo import models, fields, api

class LoanReturnWizard(models.TransientModel):
    _name = 'equipment.loan.return.wizard'
    _description = 'Return Equipment Loan Wizard'

    date_return = fields.Datetime(
        string='Return Date',
        required=True,
        default=fields.Datetime.now
    )
    condition_score = fields.Integer(
        string='Condition Score',
        required=True,
        default=100
    )
    note = fields.Text(string='Note')

    def action_confirm_return(self):
        self.ensure_one()
        loans = self.env['equipment.loan'].browse(
            self.env.context.get('active_ids', [])
        )

        for loan in loans:
            if loan.state != 'confirmed':
                continue

            loan.write({
                'date_return': self.date_return,
                'state': 'returned',
                'notes': (loan.notes or '') + (f"<p>{self.note}</p>" if self.note else ''),
            })

            # تحديث حالة الجهاز
            if loan.item_id:
                loan.item_id.condition_score = self.condition_score

            loan.message_post(
                body=f"Loan returned on {self.date_return}. Condition score: {self.condition_score}"
            )

        return {'type': 'ir.actions.act_window_close'}