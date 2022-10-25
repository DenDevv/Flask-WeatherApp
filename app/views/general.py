from flask_login import current_user, login_required
from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.forms import SearchForm
from app.models import Save
from app import db
from .weather_parser import search_weather
from uuid import uuid4


general_blueprint = Blueprint("gener", __name__)


@general_blueprint.route('/', methods=["GET", "POST"])
def home():
    sf = SearchForm()
    save_status = False

    if sf.validate_on_submit():
        search_data = sf.search_field.data
        data = search_weather(search_data)
        print(data['sky'])
    else:
        search_data = "Київ"
        data = search_weather("Київ")
        
    
    if not data:
        flash(f"Не вдалось знайти інформацію за назвою {search_data}!", "error")
        search_data = "Київ"
        data = search_weather("Київ")
    else:
        check_data = Save.query.filter_by(save_url=data['url']).first()
        if not check_data: save_status = True

    return render_template("home.html", data=data, form=sf, save_name=search_data, save_status=save_status)


@general_blueprint.route('/save', methods=["POST"])
@login_required
def save():
    user_id = current_user.id
    
    if request.method == "POST":
        save_name = request.get_json()["save_name"]
        save_url = request.get_json()["url"]
        check_data = Save.query.filter_by(save_url=save_url).first()

        if not check_data:
            save_data = Save(
                w_uuid=str(uuid4()),
                user_id=user_id,
                save_name=save_name,
                save_url=save_url
            )
            db.session.add(save_data)
            db.session.commit()

    return redirect(url_for("gener.home"))


@general_blueprint.route('/check/<w_uuid>')
@login_required
def check(w_uuid):
    data = Save.query.filter_by(w_uuid=w_uuid).first()

    if data and data.user_id==current_user.id:
        data = search_weather(search_url=data.save_url)
        print(data)

    return render_template("check_saved.html", data=data, save_name=None)


@general_blueprint.route('/remove/<w_uuid>')
@login_required
def remove(w_uuid):
    data = Save.query.filter_by(w_uuid=w_uuid).first()

    if data and data.user_id==current_user.id:
        db.session.delete(data)
        db.session.commit()

    return redirect(url_for("auth.profile"))