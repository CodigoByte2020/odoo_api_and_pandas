# -*- coding: utf-8 -*-

from odoo import fields, models


class StudentGrade(models.Model):
    _name = 'student.grade'
    # TODO: PREGUNTAR SI ES LA MEJORA MANERA DEFINIR OTRO MODELO, O SACAR LAS NOTAS DE ALGUN OTRO LADO

    grade_id = fields.Float(string='ID grade')
    mdl_groups_name = fields.Char(string='Grupo')
    course_idnumber = fields.Char(string='Id Number')
    shortname = fields.Char(string='Nombre Corto')
    fullname = fields.Char(string='Asignatura')
    finalgrade = fields.Float(string='Nota')
    student_id = fields.Many2one('op.student')
    sequence = fields.Integer(string="Secuencia")
