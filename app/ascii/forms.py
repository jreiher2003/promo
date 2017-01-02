from flask_wtf import Form 
from wtforms import TextField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class AsciiForm(Form):
    title = TextField("Title", validators=[DataRequired(message="Hey, you need a title."), Length(max=75, message="Hey, that title is a little long.")])
    art = TextAreaField("Art", validators=[DataRequired(message="Hey buddy, you need to paste in some ascii artwork.")])
    submit = SubmitField("post artwork")