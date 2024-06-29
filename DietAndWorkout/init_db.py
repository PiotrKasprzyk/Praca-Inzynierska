from app import app, db
from models import User, DietPlan, WorkoutPlan, FoodCategory, FoodItem, Post, Comment, Like

def init_db():
    with app.app_context():
        db.create_all()

        if FoodCategory.query.count() == 0:
            categories = ['Warzywa', 'Owoce', 'Białka', 'Węglowodany', 'Tłuszcze']
            for category_name in categories:
                category = FoodCategory(name=category_name)
                db.session.add(category)
            db.session.commit()

if __name__ == '__main__':
    init_db()
