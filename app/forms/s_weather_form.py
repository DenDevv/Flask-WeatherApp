from flask_wtf import FlaskForm
from wtforms import SearchField, SubmitField
from wtforms.validators import Length, DataRequired


class SearchForm(FlaskForm):
    search_field = SearchField(
        label=None,
        validators=[DataRequired()],
        render_kw={"placeholder": "Оберіть місто..."}
    )

    search_btn = SubmitField(
        label="Знайти"
    )