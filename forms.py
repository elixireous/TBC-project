from flask_wtf import FlaskForm
from wtforms import TextAreaField, FloatField
from wtforms.fields import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, equal_to, Email


class TeaForm(FlaskForm):
    name = StringField('Tea Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    submit = SubmitField('Add Tea')


class LoginForm(FlaskForm):
    username = StringField("Enter username", validators=[DataRequired()])
    email = StringField("Enter email", validators=[Email()])
    password = PasswordField("Enter Password", validators=[DataRequired(), Length(min=7, max=64)])
    login = SubmitField("Login")


class RegisterForm(FlaskForm):
    username = StringField("Enter username")
    email = EmailField("Enter email")
    password = PasswordField("Enter your password", validators=[DataRequired(), Length(min=7, max=64)])
    repeat_password = PasswordField("Repeat Password", validators=[DataRequired(),
                                                                   equal_to("password",
                                                                            message="retry password and password do not match")])

    register = SubmitField("Register")
