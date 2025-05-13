from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo, Optional
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password', message='Пароли должны совпадать')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Это имя занято. Используйте другое.')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Этот email уже зарегистрирован. Используйте другой.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Вход')


class EditProfileForm(FlaskForm):
    username = StringField('Новое имя', validators=[Optional(), Length(min=2, max=20)])  # Необязательное
    email = StringField('Новый email', validators=[Optional(), Email()])  # Email проверяется только если введён
    old_password = PasswordField('Старый пароль', validators=[DataRequired()])  # Обязателен для смены данных
    new_password = PasswordField('Новый пароль', validators=[Optional(), Length(min=6)])
    confirm_password = PasswordField('Повторите пароль', validators=[Optional(),
                    EqualTo('new_password', message='Пароли должны совпадать')])
    submit = SubmitField('Сохранить изменения')