#!/usr/bin/python

from application import app
from application.forms import UserForm, CatForm, DeleteForm, EditForm
from flask import flash, render_template, redirect, abort, session, request
from werkzeug.datastructures import MultiDict
from datetime import datetime

CAT_FORM_DATA = 'cat_form'
USER_FORM_DATA = 'user_form'


# ---------------------- User routes ----------------------


@app.route('/users')
def get_users():
    users = [{'id': 1, 'name': 'User 1'}, {'id': 2, 'name': 'User 2'}]
    return render_template("/users.html", users=users)


@app.route('/users/<int:user_id>')
def get_user(user_id):
    users = [{},
             {'name': 'User 1',
              'id': 1,
              'created_at': datetime.fromisoformat('2023-04-19T10:30:00'),
              'updated_at': datetime.fromisoformat('2023-04-19T10:30:00'),
              'cats': [{'name': 'Cat 1', 'id': 1}]
              },
             {'name': 'User 2',
              'id': 2,
              'created_at': datetime.fromisoformat('2023-04-19T10:30:00'),
              'updated_at': datetime.fromisoformat('2023-04-19T10:30:00'),
              }
             ]
    user = users[user_id]

    if user is None:
        abort(404)

    edit_form = EditForm()
    delete_form = DeleteForm()
    return render_template('user.html', user=user, edit_form=edit_form, delete_form=delete_form)


@app.route('/users', methods=['POST'])
def create_user():
    user_form = UserForm()

    if user_form.validate():
        name = user_form.name.data
        flash(f'{name} added successfully!')
        return redirect('/')

    session[USER_FORM_DATA] = request.form
    return redirect('/')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    flash(f'{user_id} has been deleted!')
    return redirect('/')


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    edit_form = EditForm()

    if edit_form.validate():
        name = edit_form.name.data
        flash(f'{name} has been updated!')
        return redirect(f'/users/{user_id}')

    return abort(400)


# # ---------------------- Cat routes ----------------------


@app.route('/cats')
def get_cats():
    cats = [{'id': 1, 'name': 'Cat 1', 'owner_name': 'Test user'}, {'id': 2, 'name': 'Cat 2'}]

    return render_template("/cats.html", cats=cats)


@app.route('/cats/<int:cat_id>')
def get_cat(cat_id):
    cats = [{},
            {'name': 'Test cat',
             'id': 1,
             'created_at': datetime.fromisoformat('2023-04-19T10:30:00'),
             'updated_at': datetime.fromisoformat('2023-04-19T10:30:00'),
             'owner': {
                 'id': 1,
                 'name': 'Test user',
             }
             },
            {'name': 'Test cat 2',
             'id': 2,
             'created_at': datetime.fromisoformat('2023-04-19T10:30:00'),
             'updated_at': datetime.fromisoformat('2023-04-19T10:30:00'),
             }
            ]
    cat = cats[cat_id]

    delete_form = DeleteForm()
    edit_form = EditForm()

    return render_template('cat.html', cat=cat, edit_form=edit_form, delete_form=delete_form)


@app.route('/cats', methods=['POST'])
def create_cat():
    cat_form = CatForm()
    cat_form.update_owners()

    if cat_form.validate():
        name = cat_form.name.data
        # owner_id = cat_form.owner_id.data
        flash(f'{name} added successfully!')

    session[CAT_FORM_DATA] = request.form
    return redirect('/')


@app.route('/cats/<int:cat_id>/delete', methods=['POST'])
def delete_cat(cat_id):
    flash(f'{cat_id} has been deleted!')
    return redirect('/')


@app.route('/cats/<int:cat_id>/edit', methods=['POST'])
def edit_cat(cat_id):
    edit_form = EditForm()

    if edit_form.validate():
        name = edit_form.name.data
        flash(f'{name} has been updated!')
        return redirect(f'/cats/{cat_id}')

    return abort(400)


@app.route('/')
def index():
    users_count = 2
    cats_count = 2

    cat_form_data = session.get(CAT_FORM_DATA)
    cat_form = CatForm(MultiDict(cat_form_data))
    cat_form.update_owners()

    if cat_form_data is not None:
        session.pop(CAT_FORM_DATA)
        cat_form.validate()

    user_form_data = session.get(USER_FORM_DATA)
    user_form = UserForm(MultiDict(user_form_data))

    if user_form_data is not None:
        session.pop(USER_FORM_DATA)
        user_form.validate()

    return render_template('index.html', user_form=user_form, cat_form=cat_form, users_count=users_count,
                           cats_count=cats_count)
