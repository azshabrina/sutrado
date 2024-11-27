# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class ApprovalProductLine(models.Model):
	_inherit = "approval.product.line"

	@api.onchange('quantity')
	def onchange_quantity(self):
		self.quantity_wait_order = self.quantity

	quantity_to_order = fields.Float('Qty To Order', default=0)
	quantity_on_order = fields.Float('Qty On Progress')
	quantity_wait_order = fields.Float('Qty Available Order')


	def update_qty_progress_pr(self):
		for line in self:
			quantity_on_order = 0
			qty_on_order = 0
			data = line.env['purchase.order.line'].search(
			[('product_id', '=', line.product_id.id),('purchase_request_lines', '=', line.id),('state', '!=', 'cancel')])
			for record in data:
				quantity_on_order += record.product_qty
				quantity_wait_order = line.quantity - quantity_on_order
				line.write({
								# 'purchase_order_line_id': record.id,
								'quantity_on_order': quantity_on_order,
								'quantity_wait_order': quantity_wait_order
							})


class PurchaseOrderLine(models.Model):
	_inherit = "purchase.order.line"

	purchase_request_id = fields.Char("PR Number",copy=False, readonly="1")
	purchase_request_lines = fields.Many2one("approval.product.line",copy=False, string="PR Line",readonly="1")

class PurchaseOrder(models.Model):
	_inherit = "purchase.order"

	def button_action_cancel(self):
		for line in self.order_line:
			if line.purchase_request_lines and line.purchase_request_id:
				data = line.env['approval.product.line'].search(
				[('product_id', '=', line.product_id.id),('id', '=', line.purchase_request_lines.id)])
				for x in data:
					if x.quantity_on_order > 0 or x.quantity_wait_order > 0:
						x.quantity_on_order = x.quantity_on_order - line.product_qty
						x.quantity_wait_order = x.quantity_wait_order + line.product_qty
					else:
						x.quantity_on_order = 0
						x.quantity_wait_order = x.quantity
				line.unlink()
				self.button_cancel()
			else:
				self.button_cancel()


class SKIMultiProductpurchase(models.TransientModel):
	_name = 'ski.multi.product.purchase'

	purchase_request_ids = fields.Many2many('approval.product.line', string="Product")

	def add_product(self):
		for line in self.purchase_request_ids:
			self.env['purchase.order.line'].create({
				'purchase_request_id': line.approval_request_id.name,
				'purchase_request_lines': line.id,
				'product_id': line.product_id.id,
				'name':line.description,
				'product_qty':line.quantity_to_order,
				'price_unit':line.product_id.standard_price,
				'order_id': self._context.get('active_id'),
				'date_planned':datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
				'product_uom' : line.product_uom_id.id
			})
			line.update_qty_progress_pr()
			line.quantity_to_order = 0
			self.clear_record_wizard()			
		return

	def clear_record_wizard(self):
		for line in self:
			line.unlink()

	def cancel_action(self):
		self.unlink()
		return {'type': 'ir.actions.act_window_close'}
