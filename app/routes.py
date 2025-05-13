from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from app.models import User
from app import db, bcrypt, app
from app.forms import RegistrationForm, LoginForm, EditProfileForm

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Ваш аккаунт был создан! Вы можете войти', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('home'))
        else:
            flash('Неверный логин или пароль', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = EditProfileForm(obj=current_user)  # Автозаполнение из объекта пользователя

    if form.validate_on_submit():
        # Проверка старого пароля (если меняются данные)
        if not current_user.check_password(form.old_password.data):
            flash('Неверный старый пароль!', 'danger')
            return redirect(url_for('account'))

        # Обновляем только заполненные поля
        if form.username.data:  # Если имя введено
            current_user.username = form.username.data

        if form.email.data:  # Если email введён
            current_user.email = form.email.data

        if form.new_password.data:  # Если пароль введён
            current_user.set_password(form.new_password.data)

        db.session.commit()
        flash('Данные обновлены!', 'success')
        return redirect(url_for('account'))

    return render_template('account.html', form=form)