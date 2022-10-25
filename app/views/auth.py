from datetime import datetime
from uuid import uuid4
from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.models import User, Save
from app.forms import LoginForm, RegisterForm, DeleteAccountForm
from .weather_parser import search_weather


auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    data = search_weather("Київ")

    if form.validate_on_submit():
        login = form.login.data
        password = form.password.data
        remember = form.remember.data

        user = User.query.filter_by(user_login=login).first()

        if user and check_password_hash(user.user_password, password):
            login_user(user, remember=remember)
            return redirect(request.args.get("next") or url_for('gener.home'))
        
        flash("Ви ввели неправильні дані для входу!", "error")

    return render_template("login.html", data=data, form=form)


@auth_blueprint.route("/register", methods=['GET', "POST"])
def register():
    form = RegisterForm()
    data = search_weather("Київ")

    if form.validate_on_submit():
        login = form.login.data
        password = form.password.data
        regtime = datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")

        user = User.query.filter_by(user_login=login).first()

        if not user and len(password) > 8:
            new_user = User(user_token=str(uuid4()),
                            user_login=login,
                            user_password=generate_password_hash(password, method='sha256'),
                            user_date=regtime)

            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))

        flash('Дані введені некоректно!', 'error')

    return render_template("register.html", data=data, form=form)


@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('gener.home'))


@auth_blueprint.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    df = DeleteAccountForm()
    user = User.query.filter_by(id=current_user.id).first()
    saved_data = Save.query.filter_by(user_id=current_user.id).all()
    w_data = []

    for data in saved_data:
        s = search_weather(search_url=data.save_url)
        w_uuid = data.w_uuid
        name = data.save_name.split(", ")[0]
        s_info = s['temp'] #+ " " + s['sky'].split()[-1]

        w_s_data = {
            "w_uuid": w_uuid,
            "name": name,
            "s_info": s_info
        }

        w_data.append(w_s_data)

    if not w_data:
        data = search_weather("Київ")
    else:
        for data in saved_data:
            data = search_weather(search_url=data.save_url)
            break

    return render_template('profile.html', data=data, user=user, w_data=w_data, user_token=user.user_token, form=df)


@auth_blueprint.route("/delete_account", methods=["GET", "POST"])
@login_required
def delete_account():
    df = DeleteAccountForm()

    if df.validate_on_submit:
        user_token = df.token_field.data
        user = User.query.filter_by(user_token=user_token).first()

        if user:
            saves = Save.query.filter_by(user_id=user.id).all()

            for save in saves:
                db.session.delete(save)

            db.session.delete(user)
            db.session.commit()
        else:
            flash("Ви ввели неправильний токен!", "error")
            return redirect(url_for("auth.profile"))

    return redirect(url_for("gener.home"))