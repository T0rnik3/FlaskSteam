from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from project import app, db
from project.forms import (AddGameForm, LoginForm, RegisterForm,
                           RemoveGameForm, UpdateAccountForm,
                           UpdatePasswordForm)
from project.models import Game, User


@app.template_filter()
def numberFormat(value):
    return format(int(value), ',d')


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


ROWS_PER_PAGE = 25
@app.route('/games', methods=['GET', 'POST'])
@login_required
def games():
    #* Set the pagination CONFIG
    page = request.args.get('page', 1, type=int)
    add_form = AddGameForm()
    if request.method == "POST":

        #! ADDING GAME LOGIC
        add_game = request.form.get('wishlist_game')
        if a_game_obj := Game.query.filter_by(title=add_game).first():
            if current_user.can_add(a_game_obj):
                a_game_obj.add_to_wishlist(current_user)
                flash(f"{a_game_obj.title} has been added to your Wishlist!", 'success')
            else:
                flash(f"{a_game_obj.title} is already in your Wishlist!", 'warning')

        return redirect(url_for('games'))

    if request.method == "GET":
        all_games = Game.query.paginate(page=page, per_page=ROWS_PER_PAGE)
        return render_template('games.html', games=all_games, add_form=add_form)


@app.route('/wishlist', methods=['POST', 'GET'])
@login_required
def wishlist():
    remove_form = RemoveGameForm()
    
    if request.method == "POST":

        #! REMOVE Game LOGIC
        remove_game = request.form.get('remove_game')
        if r_game_obj := Game.query.filter_by(title=remove_game).first():
            if current_user.can_remove(r_game_obj):
                r_game_obj.remove_from_wishlist(current_user)
                flash(f"{r_game_obj.title} has been Removed from your Wishlist!", 'success')
            else:
                flash(f"Something went wrong Removing {r_game_obj.title}!", 'danger')

    owned_games = current_user.games
    return render_template('wishlist.html', remove_form=remove_form, owned_games=owned_games)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('games'))

    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('games'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)


@app.route('/user', methods=['POST', 'GET'])
@login_required
def account():
    form = UpdateAccountForm()
    if request.method == 'GET':
        form.username.data = current_user.username

    elif request.method == 'POST':
        if form.validate_on_submit():
            current_user.username = form.username.data
            db.session.commit()
            flash('Your Account has been updated!', 'success')
            return redirect(url_for('account'))

        if form.errors != {}: #If there are not errors from the validations
            for err_msg in form.errors.values():
                flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('account.html', form=form)


@app.route('/user/password', methods=['POST', 'GET'])
@login_required
def password_change():
    pass_form = UpdatePasswordForm()
    if request.method == 'POST':
        if pass_form.validate_on_submit() and current_user.check_password_correction(pass_form.old_password.data):
            current_user.password = pass_form.password1.data
            db.session.commit()
            flash('Your Password has been updated', 'success')
            return redirect(url_for('account'))
        else:
            flash('There was an Error!', category='danger')

    return render_template('password.html', pass_form=pass_form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out!", category='primary')
    return redirect(url_for("home"))
