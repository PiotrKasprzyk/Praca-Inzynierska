from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User

class RegistrationForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    confirm_password = PasswordField('Potwierdź hasło', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Zarejestruj się')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ta nazwa użytkownika jest już zajęta. Wybierz inną.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Ten email jest już zajęty. Wybierz inny.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    remember = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj się')

class UpdateProfileForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('Imię')
    last_name = StringField('Nazwisko')
    age = FloatField('Wiek')
    height = FloatField('Wzrost')
    weight = FloatField('Waga')
    target_weight = FloatField('Docelowa waga')
    exercise_frequency = StringField('Częstotliwość ćwiczeń')
    submit = SubmitField('Zaktualizuj profil')

class DietPlanForm(FlaskForm):
    meal_name = StringField('Nazwa posiłku', validators=[DataRequired()])
    recipe = TextAreaField('Przepis', validators=[DataRequired()])
    meal_type = SelectField('Typ posiłku', choices=[('sniadanie', 'Śniadanie'), ('obiad', 'Obiad'), ('kolacja', 'Kolacja')])
    kcal = FloatField('Kalorie', validators=[DataRequired()])
    carbs = FloatField('Węglowodany', validators=[DataRequired()])
    protein = FloatField('Białko', validators=[DataRequired()])
    fat = FloatField('Tłuszcz', validators=[DataRequired()])
    submit_diet = SubmitField('Zapisz plan diety')

class WorkoutPlanForm(FlaskForm):
    exercise_name = StringField('Nazwa ćwiczenia', validators=[DataRequired()])
    day = StringField('Dzień', validators=[DataRequired()])
    sets = FloatField('Serie', validators=[DataRequired()])
    reps = FloatField('Powtórzenia', validators=[DataRequired()])
    submit_workout = SubmitField('Zapisz plan treningowy')

class FoodItemForm(FlaskForm):
    name = StringField('Nazwa', validators=[DataRequired()])
    kcal = FloatField('Kalorie', validators=[DataRequired()])
    carbs = FloatField('Węglowodany', validators=[DataRequired()])
    protein = FloatField('Białko', validators=[DataRequired()])
    fat = FloatField('Tłuszcz', validators=[DataRequired()])
    category = SelectField('Kategoria', coerce=int)
    submit = SubmitField('Dodaj produkt')

class BMIForm(FlaskForm):
    weight = FloatField('Waga (kg)', validators=[DataRequired()])
    height = FloatField('Wzrost (cm)', validators=[DataRequired()])
    submit = SubmitField('Oblicz BMI')

class PostForm(FlaskForm):
    title = StringField('Tytuł', validators=[DataRequired()])
    content = TextAreaField('Treść', validators=[DataRequired()])
    submit = SubmitField('Utwórz Post')
class CommentForm(FlaskForm):
    comment = StringField('Comment', validators=[DataRequired()])
    submit = SubmitField('Add Comment')
class LikeForm(FlaskForm):
    submit = SubmitField('Like')
