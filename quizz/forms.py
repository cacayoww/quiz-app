from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, SubmitField, ValidationError, RadioField, HiddenField
from wtforms.validators import Length, EqualTo, DataRequired

from quizz.models import User

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists!')
    username = StringField(label="User Name", validators=[Length(min=2, max=30), DataRequired()])
    password1 = PasswordField(label="Password", validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label="Confirmation Password", validators=[EqualTo('password1', message='Password confirmation does not match!'), DataRequired()])
    submit = SubmitField(label="Register")

class LoginForm(FlaskForm):
    username = StringField(label="User Name",  validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Log In")

class QuizForm(FlaskForm):
    question_id = IntegerField()
    answer = RadioField('Pilih jawaban:', 
                       choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')],
                       validators=[DataRequired()])
    submit = SubmitField('Submit Jawaban')

class CitySearchForm(FlaskForm):
    city = StringField('Cari City', validators=[DataRequired()])