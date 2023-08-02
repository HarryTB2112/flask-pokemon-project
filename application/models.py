from application import db, app


app.app_context().push()


class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ability = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)

    def __init__(self, name, ability, type):
        self.name = name
        self.ability = ability
        self.type = type

    def __repr__(self):
        return f"My name is {self.name} and my ability is {self.ability}"
