# -*- coding: utf-8 -*-

from odoo import models, fields, api

       
#Taula amb els films  
class videoclub_film(models.Model):
    """Films by videoclub"""   
    
    _name = 'videoclub.film'
    _description = "Film data"
    
    name = fields.Char(string="Name of the film", size=150, required=True, help='Name of the film')
    
    category_id = fields.Many2one('videoclub.film.category', string='Category', help="Category of the film")
    
    description = fields.Text(string="Description of the film", help="Description of the film")

    hours = fields.Float(string="Hours of the film", digits=(2, 2), help="Hours of the film")

    product_id = fields.Many2one('product.product', string='Product', help="Product related to the film")

    client_id = fields.Many2one('res.partner', string='Client', help="Client who rents the film")

    state = fields.Selection([('rented','Rented'),('free','Free'),('notAvailable','Not available')], string="State of the film", help="State of the film", default = 'free')

    tipus = fields.Selection([('allPublic','Film for all public'),('more13age','Film appropriate for age over 13'),('more18age','Film appropriate for age over 18')], 'Type of film', help="Type of film", default = 'allPublic')

    reserved = fields.Boolean(string="Film reserved", help="Film reserved", default=False)

    reservation_date = fields.Date(string="Date when the film has been reserved", help="Date when the film has been reserved")

#Categories dels films    
class videoclub_film_category(models.Model):
    """Films Categories"""
    _name = 'videoclub.film.category'
    _description = "Films categories"
    _parent_name = "parent_id"

    name = fields.Char(string="Category", size=150, help="Name of the category", required=True)
    complete_name = fields.Char(
        'Complete Name', compute='_compute_complete_name',
        store=True)
        
    description = fields.Text("Description", help="Description of the category")

    parent_id = fields.Many2one('videoclub.film.category', string="Parent Category", help="Name of the parent category", required=False, index=True, ondelete='cascade')    
    
