# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import AccessError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class SaleOrderLine(models.Model):
	_inherit = "sale.order.line"

	mrp_id = fields.Many2one("mrp.production",copy=False, string="Manufacturing Order", readonly="1")
	invisible_mrp = fields.Boolean(string="invisible MRP", default=False)

class ManufacturingOrder(models.Model):
	_inherit = "mrp.production"

	sale_order_lines = fields.Many2one("sale.order.line",copy=False, string="SO Products")
	editable_product = fields.Boolean(string="Editable Product", default=True)


	@api.onchange('sale_order_lines')
	def get_product_order(self):
		if self.sale_order_lines:
			self.product_id = self.sale_order_lines.product_id.id
			self.product_uom_qty = self.sale_order_lines.product_uom_qty
			self.product_qty = self.sale_order_lines.product_uom_qty
			self.product_uom_id = self.sale_order_lines.product_uom.id
			self.editable_product = False
		else:
			self.editable_product = True

	def button_action_confirm(self):
		if self.sale_order_lines and self.product_id:
			date=self.create_date.date()
			d2=datetime.strftime(date, "%Y-%m-%d")
			data = self.env['sale.order.line'].search([('id', '=', self.sale_order_lines.id)])
			for x in data:
				if not x.mrp_id and x.invisible_mrp == False:
					x.mrp_id = self.id
					x.invisible_mrp = True
					self.origin = self.sale_order_lines.order_id.name
					self.action_confirm()
				else:
					raise ValidationError(_('\n\n''%s,''\n\n''Item SO ini telah digunakan oleh MO : %s''\n\n''Dibuat oleh %s pada tanggal %s')
					%(self.product_id.name, x.mrp_id.name, self.create_uid.name, d2))
		else:
			self.action_confirm()