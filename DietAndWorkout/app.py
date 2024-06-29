from flask import Flask, render_template, redirect, url_for, request, flash, session, abort
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm, DietPlanForm, WorkoutPlanForm, UpdateProfileForm, FoodItemForm, BMIForm, CommentForm, PostForm,LikeForm,CommentForm
from models import db, User, DietPlan, WorkoutPlan, FoodCategory, FoodItem, Post, Comment, Like
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Konto zostało utworzone! Możesz się teraz zalogować.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Logowanie nieudane. Sprawdź email i hasło', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.age = form.age.data
        current_user.height = form.height.data
        current_user.weight = form.weight.data
        current_user.target_weight = form.target_weight.data
        current_user.exercise_frequency = form.exercise_frequency.data
        db.session.commit()
        flash('Twój profil został zaktualizowany!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.age.data = current_user.age
        form.height.data = current_user.height
        form.weight.data = current_user.weight
        form.target_weight.data = current_user.target_weight
        form.exercise_frequency.data = current_user.exercise_frequency
        
    theme=session.get('theme', 'light')

    return render_template('profile.html', form=form)


@app.route('/news', methods=['GET', 'POST'])
@login_required
def news():
    posts = Post.query.all()
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post został utworzony!', 'success')
        return redirect(url_for('news'))

    theme = session.get('theme', 'light')
    return render_template('news.html', posts=posts, form=form, theme=theme)

@app.route('/diet', methods=['GET', 'POST'])
@login_required
def diet():
    diet_plans = DietPlan.query.filter_by(user_id=current_user.id).all()
    theme = session.get('theme', 'light')
    return render_template('diet.html', title='Diet', diet_plans=diet_plans)

@app.route('/edit_diet/<int:diet_id>', methods=['GET', 'POST'])
@login_required
def edit_diet(diet_id):
    diet = DietPlan.query.get_or_404(diet_id)
    if diet.user_id != current_user.id:
        abort(403)
    form = DietPlanForm()
    if form.validate_on_submit():
        diet.meal_name = form.meal_name.data
        diet.recipe = form.recipe.data
        diet.meal_type = form.meal_type.data
        diet.kcal = form.kcal.data
        diet.carbs = form.carbs.data
        diet.protein = form.protein.data
        diet.fat = form.fat.data
        db.session.commit()
        flash('Twoja dieta została zaktualizowana!', 'success')
        return redirect(url_for('diet'))
    elif request.method == 'GET':
        form.meal_name.data = diet.meal_name
        form.recipe.data = diet.recipe
        form.meal_type.data = diet.meal_type
        form.kcal.data = diet.kcal
        form.carbs.data = diet.carbs
        form.protein.data = diet.protein
        form.fat.data = diet.fat
    theme = session.get('theme', 'light')
    return render_template('edit_diet.html', form=form,diet=diet, theme=theme)

@app.route('/delete_diet/<int:diet_id>', methods=['POST'])
@login_required
def delete_diet(diet_id):
    diet_plan = DietPlan.query.get_or_404(diet_id)
    if diet_plan.user_id != current_user.id:
        abort(403)
    db.session.delete(diet_plan)
    db.session.commit()
    flash('Plan diety został usunięty!', 'success')
    return redirect(url_for('diet'))

@app.route('/workout', methods=['GET', 'POST'])
@login_required
def workout():
    workout_plans = WorkoutPlan.query.filter_by(user_id=current_user.id).all()
    theme = session.get('theme', 'light')
    return render_template('workout.html', title='Workout', workout_plans=workout_plans)

@app.route('/edit_workout/<int:workout_id>', methods=['GET', 'POST'])
@login_required
def edit_workout(workout_id):
    workout = WorkoutPlan.query.get_or_404(workout_id)
    if workout.user_id != current_user.id:
        abort(403)
    form = WorkoutPlanForm()
    if form.validate_on_submit():
        workout.exercise_name = form.exercise_name.data
        workout.day = form.day.data
        workout.sets = form.sets.data
        workout.reps = form.reps.data
        db.session.commit()
        flash('Plan treningowy został zaktualizowany!', 'success')
        return redirect(url_for('workout'))
    elif request.method == 'GET':
        form.exercise_name.data = workout.exercise_name
        form.day.data = workout.day
        form.sets.data = workout.sets
        form.reps.data = workout.reps
    theme = session.get('theme', 'light')
    return render_template('edit_workout.html', form=form, workout=workout, theme=theme)


@app.route('/delete_workout/<int:workout_id>', methods=['POST'])
@login_required
def delete_workout(workout_id):
    workout_plan = WorkoutPlan.query.get_or_404(workout_id)
    if workout_plan.user_id != current_user.id:
        abort(403)
    db.session.delete(workout_plan)
    db.session.commit()
    flash('Plan treningowy został usunięty!', 'success')
    return redirect(url_for('workout'))

@app.route('/bmi', methods=['GET', 'POST'])
def bmi():
    form = BMIForm()
    bmi = None
    category = None
    if form.validate_on_submit():
        weight = form.weight.data
        height = form.height.data
        bmi, category = calculate_bmi(weight, height)
        theme=session.get('theme', 'light')
    return render_template('bmi.html', form=form, bmi=bmi, category=category)

def calculate_bmi(weight, height):
    if weight and height:
        bmi = weight / ((height / 100) ** 2)
        if bmi < 18.5:
            category = "Niedowaga"
        elif 18.5 <= bmi < 24.9:
            category = "Waga w normie"
        elif 25 <= bmi < 29.9:
            category = "Nadwaga"
        else:
            category = "Otyłość"
        return bmi, category
    return None, None

@app.route('/products', methods=['GET', 'POST'])
@login_required
def products():
    form = FoodItemForm()
    form.category.choices = [(category.id, category.name) for category in FoodCategory.query.all()]
    if form.validate_on_submit():
        food_item = FoodItem(
            name=form.name.data,
            kcal=form.kcal.data,
            carbs=form.carbs.data,
            protein=form.protein.data,
            fat=form.fat.data,
            category_id=form.category.data
        )
        db.session.add(food_item)
        db.session.commit()
        flash('Produkt dodany pomyślnie!', 'success')
        return redirect(url_for('products'))
    food_items = FoodItem.query.all()
    theme=session.get('theme', 'light')
    return render_template('products.html', food_items=food_items, form=form)


@app.route('/create_plan', methods=['GET', 'POST'])
@login_required
def create_plan():
    diet_form = DietPlanForm()
    workout_form = WorkoutPlanForm()

    if diet_form.validate_on_submit() and diet_form.submit_diet.data:
        new_diet = DietPlan(
            user_id=current_user.id,
            meal_name=diet_form.meal_name.data,
            recipe=diet_form.recipe.data,
            meal_type=diet_form.meal_type.data,
            kcal=diet_form.kcal.data,
            carbs=diet_form.carbs.data,
            protein=diet_form.protein.data,
            fat=diet_form.fat.data
        )
        db.session.add(new_diet)
        db.session.commit()
        flash('Plan diety został zapisany!', 'success')
        return redirect(url_for('create_plan'))

    if workout_form.validate_on_submit() and workout_form.submit_workout.data:
        new_workout = WorkoutPlan(
            user_id=current_user.id,
            exercise_name=workout_form.exercise_name.data,
            day=workout_form.day.data,
            sets=workout_form.sets.data,
            reps=workout_form.reps.data
        )
        db.session.add(new_workout)
        db.session.commit()
        flash('Plan treningowy został zapisany!', 'success')
        return redirect(url_for('create_plan'))
    theme = session.get('theme', 'light')
    return render_template('create_plan.html', diet_form=diet_form, workout_form=workout_form)

@app.route('/change_theme')
def change_theme():
    current_theme = session.get('theme', 'light')
    new_theme = 'dark' if current_theme == 'light' else 'light'
    session['theme'] = new_theme
    flash(f'Motyw zmieniony na {new_theme}', 'success')
    return redirect(url_for('home'))
@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id).all()
    like_form = LikeForm()
    comment_form = CommentForm()
    
    if comment_form.validate_on_submit() and 'submit' in request.form:
        if not current_user.is_authenticated:
            flash('You need to be logged in to comment.', 'danger')
            return redirect(url_for('login'))
        comment = Comment(content=comment_form.comment.data, author=current_user, post_id=post_id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('post', post_id=post_id))
    
    return render_template('post.html', post=post, comments=comments, like_form=like_form, comment_form=comment_form)

@app.route('/like/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    like = Like.query.filter_by(user_id=current_user.id, post_id=post.id).first()
    if like:
        db.session.delete(like)
    else:
        like = Like(user_id=current_user.id, post_id=post.id)
        db.session.add(like)
    db.session.commit()
    return redirect(url_for('post', post_id=post_id))

@app.route('/add_comment/<int:post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.comment.data, author=current_user, post=post)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added.', 'success')
    return redirect(url_for('post', post_id=post_id))
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
