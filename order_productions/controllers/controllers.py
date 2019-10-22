# -*- coding: utf-8 -*-
from odoo import http

# class OrderProductions(http.Controller):
#     @http.route('/order_productions/order_productions/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/order_productions/order_productions/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('order_productions.listing', {
#             'root': '/order_productions/order_productions',
#             'objects': http.request.env['order_productions.order_productions'].search([]),
#         })

#     @http.route('/order_productions/order_productions/objects/<model("order_productions.order_productions"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('order_productions.object', {
#             'object': obj
#         })