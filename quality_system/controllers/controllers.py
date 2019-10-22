# -*- coding: utf-8 -*-
from odoo import http

# class QualitySystem(http.Controller):
#     @http.route('/quality_system/quality_system/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/quality_system/quality_system/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('quality_system.listing', {
#             'root': '/quality_system/quality_system',
#             'objects': http.request.env['quality_system.quality_system'].search([]),
#         })

#     @http.route('/quality_system/quality_system/objects/<model("quality_system.quality_system"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('quality_system.object', {
#             'object': obj
#         })