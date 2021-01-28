from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///laba5.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class ReservationData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reservationdate = db.Column(db.Integer, nullable=False)
    complete_reservation = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<ReservationData %r>' % self.id


class Editions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    received_editions = db.Column(db.String(100), nullable=False)
    name_of_editions = db.Column(db.String(100), nullable=False)
    index = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return '<Editions %r>' % self.id


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Integer, nullable=False)
    end_date = db.Column(db.Integer, nullable=False)
    for_year = db.Column(db.Boolean, nullable=False)
    half_year = db.Column(db.Boolean, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    name_of_editions = db.Column(db.String(100), nullable=False)
    method_of_receiving = db.Column(db.String(100), nullable=False)


    def __repr__(self):
        return '<Subscription %r>' % self.id


class Method_of_delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    method_of_receiving = db.Column(db.String(100), nullable=False)
    estimated_date = db.Column(db.Integer, nullable=False)
    

    def __repr__(self):
        return '<Method_of_delivery %r>' % self.id


class Received_editions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_of_received = db.Column(db.Integer, nullable=False)
    name_of_editions = db.Column(db.String(100), nullable=False)
    number_of_editions = db.Column(db.Integer, nullable=False)
    index = db.Column(db.String(100), nullable=False)
    name_of_stuff = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Received_editions %r>' % self.id


class Stuff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_of_stuff = db.Column(db.String(100), nullable=False)
    adress_of_stuff = db.Column(db.String(100), nullable=False)
    numberphone = db.Column(db.Integer, nullable=False)

    
    def __repr__(self):
        return '<Stuff %r>' % self.id


@app.route('/reservation')
def reservation():
    reservation = ReservationData.query.order_by(ReservationData.id.desc()).all()
    return render_template("reservation.html", reservation=reservation)


@app.route('/reservation/<int:id>/update', methods=['POST', 'GET'])
def reservation_update(id):
    reservation = ReservationData.query.get(id)
    if request.method == "POST":
        reservation.reservationdate = request.form['reservationdate']
        reservation.complete_reservation = request.form['complete_reservation']

        try:
            db.session.commit()
            return redirect('/reservation')
        except:
            return "При радактировании резервированных данных произошла ошибка"
    else:
        return render_template("update_reservation.html", reservation=reservation)


@app.route('/create_reservation', methods=['GET', 'POST'])
def reservation_create():
    if request.method == "POST":
        reservationdate = request.form['reservationdate']
        complete_reservation = request.form['complete_reservation']

        reservation = ReservationData(reservationdate=reservationdate, complete_reservation=complete_reservation)

        try:
            db.session.add(reservation)
            db.session.commit()
            return redirect('/reservation')
        except:
            return "При резервировании произошла ошибка"
    else:
        return render_template("create_reservation.html")


@app.route('/reservation/<int:id>/delete')
def reservation_delete(id):
    reservation = ReservationData.query.get_or_404(id)

    try:
        db.session.delete(reservation)
        db.session.commit()
        return redirect('/reservation')
    except:
        return "При удалении резервирования произошла ошибка"


@app.route('/reservation/<int:id>')
def reservation_detail(id):
    reservation = ReservationData.query.get(id)
    return render_template("reservation_detail.html", reservation=reservation)


@app.route('/editions')
def editions():
    editions = Editions.query.order_by(Editions.id.desc()).all()
    return render_template("editions.html", editions=editions)


@app.route('/editions/<int:id>/update', methods=['POST', 'GET'])
def editions_update(id):
    editions = Editions.query.get(id)
    if request.method == "POST":
        editions.received_editions = request.form['received_editions']
        editions.name_of_editions = request.form['name_of_editions']
        editions.index = request.form['index']
        
        try:
            db.session.commit()
            return redirect('/editions')
        except:
            return "При радактировании изданий произошла ошибка"
    else:
        return render_template("update_editions.html", editions=editions)


@app.route('/create_editions', methods=['GET', 'POST'])
def editions_create():
    if request.method == "POST":
        received_editions = request.form['received_editions']
        name_of_editions = request.form['name_of_editions']
        index = request.form['index']
        
        editions = Editions(received_editions=received_editions, name_of_editions=name_of_editions, index=index)      

        try:
            db.session.add(editions)
            db.session.commit()
            return redirect('/editions')
        except:
            return "При добавлении издания произошла ошибка"
    else:
        return render_template("create_editions.html")


@app.route('/editions/<int:id>/delete')
def editions_delete(id):
    editions = Editions.query.get_or_404(id)

    try:
        db.session.delete(editions)
        db.session.commit()
        return redirect('/editions')
    except:
        return "При удалении издания произошла ошибка"


@app.route('/editions/<int:id>')
def editions_detail(id):
    editions = Editions.query.get(id)
    return render_template("editions_detail.html", editions=editions)


@app.route('/subscription')
def subscription():
    subscription = Subscription.query.order_by(Subscription.id.desc()).all()
    return render_template("subscription.html", subscription=subscription)


@app.route('/subscription/<int:id>/delete')
def subscription_delete(id):
    subscription = Subscription.query.get_or_404(id)

    try:
        db.session.delete(subscription)
        db.session.commit()
        return redirect('/subscription')
    except:
        return "При удалении подписки произошла ошибка"


@app.route('/subscription/<int:id>/update', methods=['POST', 'GET'])
def subscription_update(id):
    subscription = Subscription.query.get(id)
    if request.method == "POST":
        subscription.start_date = request.form['start_date']
        subscription.end_date = request.form['end_date']
        subscription.for_year = request.form['for_year']
        subscription.half_year = request.form['half_year']
        subscription.price = request.form['price']
        subscription.name_of_editions = request.form['name_of_editions']
        subscription.method_of_receiving = request.form['method_of_receiving']

        try:
            db.session.commit()
            return redirect('/subscription')
        except:
            return "При радактировании подписки произошла ошибка"
    else:
        return render_template("update_subscription.html", subscription=subscription)


@app.route('/create_subscription', methods=['POST', 'GET'])
def subscription_create():
    if request.method == "POST":
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        for_year = request.form['for_year']
        half_year = request.form['half_year']
        price = request.form['price']
        name_of_editions = request.form['name_of_editions']
        method_of_receiving = request.form['method_of_receiving']

        subscription = Subscription(start_date=start_date, end_date=end_date, 
        for_year=for_year, half_year=half_year, price=price, name_of_editions=name_of_editions,
        method_of_receiving=method_of_receiving)

        try:
            db.session.add(subscription)
            db.session.commit()
            return redirect('/subscription')
        except:
            return "При добавлении подписки произошла ошибка"
    else:
        return render_template("create_subscription.html")


@app.route('/subscription/<int:id>')
def subscription_detail(id):
    subscription = Subscription.query.get(id)
    return render_template("subscription_detail.html", subscription=subscription)


@app.route('/method_of_delivery')
def method_of_delivery():
    method_of_delivery = Method_of_delivery.query.order_by(Method_of_delivery.id.desc()).all()
    return render_template("method_of_delivery.html", method_of_delivery=method_of_delivery)


@app.route('/method_of_delivery/<int:id>')
def method_of_delivery_detail(id):
    method_of_delivery = Method_of_delivery.query.get(id)
    return render_template("method_of_delivery_detail.html", method_of_delivery=method_of_delivery)


@app.route('/method_of_delivery/<int:id>/delete')
def method_of_delivery_delete(id):
    method_of_delivery = Method_of_delivery.query.get_or_404(id)

    try:
        db.session.delete(method_of_delivery)
        db.session.commit()
        return redirect('/method_of_delivery')
    except:
        return "При удалении способа доставки произошла ошибка"


@app.route('/method_of_delivery/<int:id>/update', methods=['POST', 'GET'])
def method_of_delivery_update(id):
    method_of_delivery = Method_of_delivery.query.get(id)
    if request.method == "POST":
        method_of_delivery.method_of_receiving = request.form['method_of_receiving']
        method_of_delivery.estimated_date = request.form['estimated_date']
        

        try:
            db.session.commit()
            return redirect('/method_of_delivery')
        except:
            return "При радактировании способа доставки произошла ошибка"
    else:
        return render_template("update_method_of_delivery.html", method_of_delivery=method_of_delivery)


@app.route('/create_method_of_delivery', methods=['GET', 'POST'])
def method_of_delivery_create():
    if request.method == "POST":
        method_of_receiving = request.form['method_of_receiving']
        estimated_date = request.form['estimated_date']
        

        method_of_delivery = Method_of_delivery(method_of_receiving=method_of_receiving, estimated_date=estimated_date)

        try:
            db.session.add(method_of_delivery)
            db.session.commit()
            return redirect('/method_of_delivery')
        except:
            return "При добавлении способа доставки произошла ошибка"
    else:
        return render_template("create_method_of_delivery.html")


@app.route('/received_editions')
def received_editions():
    received_editions = Received_editions.query.order_by(Received_editions.id.desc()).all()
    return render_template("received_editions.html", received_editions=received_editions)


@app.route('/received_editions/<int:id>')
def received_editions_detail(id):
    received_editions = Received_editions.query.get(id)
    return render_template("received_editions_detail.html", received_editions=received_editions)


@app.route('/received_editions/<int:id>/delete')
def received_editions_delete(id):
    received_editions = Received_editions.query.get_or_404(id)

    try:
        db.session.delete(received_editions)
        db.session.commit()
        return redirect('/received_editions')
    except:
        return "При удалении полученных изданий произошла ошибка"


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/received_editions/<int:id>/update', methods=['POST', 'GET'])
def received_editions_update(id):
    received_editions = Received_editions.query.get(id)
    if request.method == "POST":
        received_editions.date_of_received = request.form['date_of_received']
        received_editions.name_of_editions = request.form['name_of_editions']
        received_editions.number_of_editions = request.form['number_of_editions']
        received_editions.index = request.form['index']
        received_editions.name_of_stuff = request.form['name_of_stuff']

        try:
            db.session.commit()
            return redirect('/received_editions')
        except:
            return "При радактировании полученных изданий произошла ошибка"
    else:
        return render_template("update_received_editions.html", received_editions=received_editions)


@app.route('/create_received_editions', methods=['GET', 'POST'])
def received_editions_create():
    if request.method == "POST":

        date_of_received = request.form['date_of_received']
        name_of_editions = request.form['name_of_editions']
        number_of_editions = request.form['number_of_editions']
        index = request.form['index']
        name_of_stuff = request.form['name_of_stuff']

        received_editions = Received_editions(date_of_received=date_of_received, name_of_editions=name_of_editions,
         number_of_editions=number_of_editions, index=index, name_of_stuff=name_of_stuff)

        try:
            db.session.add(received_editions)
            db.session.commit()
            return redirect('/received_editions')
        except:
            return "При добавлении полученных изданий произошла ошибка"
    else:
        return render_template("create_received_editions.html")




@app.route('/stuff')
def stuff():
    stuff = Stuff.query.order_by(Stuff.id.desc()).all()
    return render_template("stuff.html", stuff=stuff)


@app.route('/stuff/<int:id>')
def stuff_detail(id):
    stuff = Stuff.query.get(id)
    return render_template("stuff_detail.html", stuff=stuff)


@app.route('/stuff/<int:id>/delete')
def stuff_delete(id):
    stuff = Stuff.query.get_or_404(id)

    try:
        db.session.delete(stuff)
        db.session.commit()
        return redirect('/stuff')
    except:
        return "При удалении сотрудника произошла ошибка"



@app.route('/stuff/<int:id>/update', methods=['POST', 'GET'])
def stuff_update(id):
    stuff = Stuff.query.get(id)
    if request.method == "POST":
        stuff.name_of_stuff = request.form['name_of_stuff']
        stuff.adress_of_stuff = request.form['adress_of_stuff']
        stuff.numberphone = request.form['numberphone']

        try:
            db.session.commit()
            return redirect('/stuff')
        except:
            return "При радактировании сотрудника произошла ошибка"
    else:
        return render_template("update_stuff.html", stuff=stuff)


@app.route('/create_stuff', methods=['GET', 'POST'])
def stuff_create():
    if request.method == "POST":
        name_of_stuff = request.form['name_of_stuff']
        adress_of_stuff = request.form['adress_of_stuff']
        numberphone = request.form['numberphone']
        
        stuff = Stuff(name_of_stuff=name_of_stuff, adress_of_stuff=adress_of_stuff,
         numberphone=numberphone)

        try:
            db.session.add(stuff)
            db.session.commit()
            return redirect('/stuff')
        except:
            return "При добавлении сотрудника произошла ошибка"
    else:
        return render_template("create_stuff.html")


if __name__ == "__main__":
    app.run(debug=True)