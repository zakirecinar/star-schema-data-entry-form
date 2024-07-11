from . import db

class Dimension1(db.Model):
    __tablename__ = 'dimension1'
    urunID = db.Column(db.Integer, primary_key=True)
    urunAdi = db.Column(db.String(50), nullable=False)
    urunGrubu = db.Column(db.String(50), nullable=False)

class Dimension2(db.Model):
    __tablename__ = 'dimension2'
    musteriID = db.Column(db.Integer, primary_key=True)
    musteriAdi = db.Column(db.String(50), nullable=False)

class Dimension3(db.Model):
    __tablename__ = 'dimension3'
    zamanID = db.Column(db.Integer, primary_key=True)
    zamanAdi = db.Column(db.String(50), nullable=False)
    ay = db.Column(db.Integer, nullable=False)
    yil = db.Column(db.String(50), nullable=False)

class Fact(db.Model):
    __tablename__ = 'fact'
    id = db.Column(db.Integer, primary_key=True)
    urunID = db.Column(db.Integer, db.ForeignKey('dimension1.urunID'), nullable=False)
    musteriID = db.Column(db.Integer, db.ForeignKey('dimension2.musteriID'), nullable=False)
    zamanID = db.Column(db.Integer, db.ForeignKey('dimension3.zamanID'), nullable=False)
    tutar = db.Column(db.Numeric, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'urunID': self.urunID,
            'musteriID': self.musteriID,
            'zamanID': self.zamanID,
            'tutar': self.tutar
        }
