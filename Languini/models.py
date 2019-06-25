from Languini import db


class Movement(db.Model):
    id = db.column(db.Integer, primary_Key=True)
    vidUrl = db.column(db.String(120), unique=True, nullable=False)


class Link(db.Model):
    id = db.column(db.Integer, primary_Key=True)
    strainId = db.column(db.Integer, db.ForeignKey('Strain.id'), nullable=False)
    nextId = db.column(db.Integer, nullable=False)

class AnswersSet(db.model):
    id = db.column(db.Integer, primary_Key=True)
    linkId = db.column(db.Integer, db.ForeignKey('Link.id'), nullable=False)
    movementId = db.column(db.Integer, db.ForeignKey('Movement.id'), nullable=False)

class Strain(db.model):
    id = db.column(db.Integer, primary_Key=True)
    strainType = db.column(db.String(20))
    vidnum = db.column(db.Integer)

class vidList(db.model):
    moveId = db.column(db.integer, db.ForeignKey('Movement.id'), nullable = False)
    StrainID = db.column(db.Integer, db.ForeignKey('Strain.id'), nullable=False)