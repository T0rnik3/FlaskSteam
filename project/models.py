from flask_login import UserMixin

from project import bcrypt, db, login_manager


#! IMPORTANT FOR LOGIN MANAGER INSTANCE
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Association TABLE many-to-many
user_wishes = db.Table('user_wishes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    games = db.relationship('Game', secondary=user_wishes, backref='wishers')


    @property
    def password(self):
        return self.password


    #! BCRYPTING PASSWORD
    @password.setter
    def password(self, plaint_text_password):
        self.password_hash = bcrypt.generate_password_hash(plaint_text_password).decode('utf-8')


    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


    def can_add(self, game_obj):
        return game_obj not in self.games


    def can_remove(self, game_obj):
        return game_obj in self.games


    def __repr__(self) -> str:
        return f'User: {self.username}'


class Game(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(length=50), nullable=False, unique=True)
    release_date = db.Column(db.String(length=30), nullable=False)
    discount = db.Column(db.Integer(), nullable=True)
    platforms = db.Column(db.String(length=20), nullable=False)
    old_price = db.Column(db.String(length=30), nullable=False)
    price = db.Column('new_price', db.String(length=30), nullable=False)
    positive_ratings = db.Column(db.Integer(), nullable=False)
    reviews = db.Column(db.Integer(), nullable=False)
    img = db.Column(db.String(length=2048), nullable=False)


    def add_to_wishlist(self, user):
        user.games.append(self)
        db.session.commit()


    def remove_from_wishlist(self, user):
        user.games.remove(self)
        db.session.commit()


    def __repr__(self) -> str:
        return f'Game: {self.title}'
