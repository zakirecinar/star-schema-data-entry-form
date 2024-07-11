from flask import Blueprint, render_template, jsonify, request
from app.models import Dimension1, Dimension2, Dimension3, Fact
from app import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/add_sample_data', methods=['POST'])
def add_sample_data():
    urun1 = Dimension1(urunID='P1', urunAdi='Product 1', urunGrubu='Group 1')
    urun2 = Dimension1(urunID='P2', urunAdi='Product 2', urunGrubu='Group 2')
    urun3 = Dimension1(urunID='P3', urunAdi='Product 3', urunGrubu='Group 3')

    musteri1 = Dimension2(musteriID=1, musteriAdi='Sadi')
    musteri2 = Dimension2(musteriID=2, musteriAdi='Ali')
    musteri3 = Dimension2(musteriID=3, musteriAdi='Ada')

    zaman1 = Dimension3(zamanID=1, zamanAdi='Time 1', ay=1, yil='2022')
    zaman2 = Dimension3(zamanID=2, zamanAdi='Time 2', ay=2, yil='2022')
    zaman3 = Dimension3(zamanID=3, zamanAdi='Time 3', ay=3, yil='2022')

    try:
        db.session.add_all([urun1, urun2, urun3, musteri1, musteri2, musteri3, zaman1, zaman2, zaman3])
        db.session.commit()

        fact1 = Fact(urunID=urun1.urunID, musteriID=musteri1.musteriID, zamanID=zaman1.zamanID, tutar=1500)
        fact2 = Fact(urunID=urun2.urunID, musteriID=musteri2.musteriID, zamanID=zaman2.zamanID, tutar=700)
        fact3 = Fact(urunID=urun3.urunID, musteriID=musteri3.musteriID, zamanID=zaman3.zamanID, tutar=200)

        db.session.add_all([fact1, fact2, fact3])
        db.session.commit()

        return "Sample data added successfully!"
    except Exception as e:
        return f"Error adding sample data: {str(e)}"


@main.route('/create_dynamic_form', methods=['POST'])
def create_dynamic_form():
    data = request.get_json()
    row_dimensions = data.get('row_dimensions')
    column_dimension = data.get('column_dimension')

    html = "<form id='dynamicForm' method='POST'><table><tr><th></th>"
    times = Dimension3.query.all()

    if column_dimension == "dimension3":
        for time in times:
            html += f"<th>{time.zamanAdi}</th>"
    html += "</tr>"

    for row_dimension in row_dimensions:
        if row_dimension == "dimension1":
            urunler = Dimension1.query.all()
            for urun in urunler:
                html += f"<tr><td>{urun.urunAdi}</td>"
                if column_dimension == "dimension3":
                    for time in times:
                        html += f"<td><input type='number' name='value_{urun.urunID}_{time.zamanID}' placeholder='Value'></td>"
                html += "</tr>"
        elif row_dimension == "dimension2":
            musteriler = Dimension2.query.all()
            for musteri in musteriler:
                html += f"<tr><td>{musteri.musteriAdi}</td>"
                if column_dimension == "dimension3":
                    for time in times:
                        html += f"<td><input type='number' name='value_{musteri.musteriID}_{time.zamanID}' placeholder='Value'></td>"
                html += "</tr>"
    html += "</table><button type='submit'>Veri Girişi</button></form>"

    return jsonify({'html': html})

@main.route('/api/facts', methods=['POST'])
def add_fact():
    data = request.json
    urunID = data.get('urunID')
    row_dimensions = data.get('row_dimensions')
    column_dimension = data.get('column_dimension')

    if not column_dimension:
        return jsonify({'error': 'Column dimension not provided'}), 400
    
    for key, value in data.items():
        if key.startswith('value_'):
            values = key.split('_')
            musteriID = int(values[1])
            zamanID = int(values[2])
            new_fact = Fact(
                urunID=urunID,
                musteriID=musteriID,
                zamanID=zamanID,
                tutar=value
            )
            db.session.add(new_fact)
    
    db.session.commit()
    print(f"Received data: {data}")
    return jsonify({'message': 'Fact added successfully'}), 201

@main.route('/show_records', methods=['GET'])
def show_records():
    records = Fact.query.all()
    return render_template('show_records.html', records=records)
