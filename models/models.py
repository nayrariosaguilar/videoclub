# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

#Taula amb els films
#Este campo tiene relaciones importantes con product_id donde crea un producto que simboliza la pelicula
#Tiene una relacion con client_id que simboliza el cliente que alquila la pelicula (solamente cuando elige rented)
#Tiene una relacion con actor_ids que simboliza los actores que actuan en la pelicula
#Tiene una relacion con director_ids que simboliza los directores que dirigen la pelicula, puede ser mas de uno

class videoclub_film(models.Model):
    """Films by videoclub"""   
    
    _name = 'videoclub.film'
    _description = "Film data"
    
    category_id = fields.Many2one('videoclub.film.category', string='Category', help="Category of the film")
    
    description = fields.Text(string="Description of the film", help="Description of the film")

    duration = fields.Integer(string="minutes of the film", help="minutes of the film")

    product_id = fields.Many2one('product.product', string='Product name', help="Product related to the film")

    client_id = fields.Many2one('res.partner', string='Client', help="Client who rents the film")

    state = fields.Selection([('rented','Rented'),('free','Free'),('notAvailable','Not available')], string="State of the film", help="State of the film", default = 'free')

    tipus = fields.Selection([('allPublic','Film for all public'),('more13age','Film appropriate for age over 13'),('more18age','Film appropriate for age over 18')], 'Type of film', help="Type of film", default = 'allPublic')

    reserved = fields.Boolean(string="Film reserved", help="Film reserved", default=False)

    reservation_date = fields.Date(string="Date when the film has been reserved", help="Date when the film has been reserved")

    actor_ids = fields.Many2many('videoclub.actor', string='Actors', help="Actors in this film")

    director_ids = fields.Many2many('videoclub.director', string='Directors', help="Directors of this film")

#Categories dels films
#Puede heredar una categoria superior
#Tiene una descripcion de la categoria
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


#Taula amb els directors
#Un director pot haber participat en més d'una
#La nacionalidad la heredamos de res.country (un modulo de odoo)
#Los años de experiencia no pueden ser negativos
class videoclub_director(models.Model):
    """ director or directors of the films"""

    _name = 'videoclub.director'
    _description = "Director of the films"
    name = fields.Char(string="Complete name of the director", size=150, required=True, help='Complete name of the director')
    #Cuento que puede haber mas de un director por pelicula
    film_id = fields.Many2many('videoclub.film', string='Film', help="Film produced by the director")
    #Cannot be negative
    years_of_experience = fields.Integer(string="Director years of work experience", digits=2, help="Years of experience")
    studies = fields.Selection([('1', 'Autodidacta'), ('2', 'Formación Profesional de Cine'), ('3', 'Grado Universitario'), ('4','Máster'),('5','Licenciatura')],
                             string="Level of studie of the director", help="Studies of the director", default='Grado Universitario')
    nationality = fields.Many2one('res.country', string="Nationality of the director", help="Nationality of the director")

    @api.constrains('years_of_experience')
    def _check_experience_positive(self):
        for record in self:
            if record.years_of_experience <= 0:
                raise ValidationError('The years_of_experience must be greater than zero!')

#Taula amb els actors
#Un actor pot haber participat en més d'una
#La nacionalidad la heredamos de res.country (un modulo de odoo)
#Los años de experiencia no pueden ser negativos
class videoclub_actor(models.Model):
    """Actors of the films"""

    _name = 'videoclub.actor'
    _description = "Actor of the films"
    name = fields.Char(string="actor name", size=50, required=True, help='Actor entire name')
    film_id = fields.Many2many('videoclub.film', string='Film', help="Film acted by the actor")
    years_of_experience = fields.Integer(string="Actor years of work experience", digits=2, help="Years of experience")
    studies = fields.Selection([('1', 'Autodidacta'), ('2', 'Formación Profesional de Cine'), ('3', 'Grado Universitario'), ('4','Máster'),('5','Licenciatura')],
                             string="Level of studie of the actor", help="Studies of the actor", default='Grado Universitario')
    nationality = fields.Many2one('res.country', string="Nationality of the director", help="Nationality of the director")


    @api.constrains('years_of_experience')
    def _check_experience_positive(self):
        for record in self:
            if record.years_of_experience <= 0:
                raise ValidationError('The years_of_experience must be greater than zero!')
