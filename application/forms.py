#!/usr/bin/python

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length


class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=255)])
    submit = SubmitField('Add User')


class CatForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=255)])
    owner_id = SelectField('Owner', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Add Cat')

    def update_owners(self):
        self.owner_id.choices = CatForm.__get_users()

    @classmethod
    def __get_users(cls):
        return [(user['id'], user['name']) for user in [{'id': 1, 'name': 'User 1'}, {'id': 2, 'name': 'User 2'}]]


class DeleteForm(FlaskForm):
    submit = SubmitField('Delete')


class EditForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=255)])
    submit = SubmitField('Save changes')
