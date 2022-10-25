from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, DataRequired


class LoginForm(FlaskForm):
    login = StringField(
        label=None,
        validators=[DataRequired(), Length(max=50)],
        render_kw={"placeholder": "Логін",
                   "autocomplete": "off"}
    )

    password = PasswordField(
        label=None,
        validators=[DataRequired(), Length(max=256)],
        render_kw={"placeholder": "Пароль"}
    )

    remember = BooleanField(
        label='Запам\'ятати'
    )

    sign_in = SubmitField(
        label="Увійти"
    )


class RegisterForm(FlaskForm):
    login = StringField(
        label=None,
        validators=[DataRequired(), Length(max=50)],
        render_kw={"placeholder": "Придумайте логін",
                   "autocomplete": "off"}
    )

    password = PasswordField(
        label=None,
        validators=[DataRequired(), Length(max=256)],
        render_kw={"placeholder": "Придумайте пароль"}
    )

    sign_up = SubmitField(
        label="Зареєструватись"
    )


class DeleteAccountForm(FlaskForm):
    token_field = StringField(
        label=None,
        validators=[DataRequired()],
        render_kw={"placeholder": "Введіть токен сюди...",
                   "id": "user__token",
                   "autocomplete": "off"}
    )

    confirm = SubmitField(
        label="Видалити",
        render_kw = {"id": "confirm__delete__btn"}
    )