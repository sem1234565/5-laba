import unittest
import os
from app import app, db, ReservationData, Editions, Subscription, Method_of_delivery, Received_editions, Stuff
class TestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join('strezhnev.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home(self):
        result = self.app.get('/')

    def test_reservationdata(self):
        r = ReservationData(reservationdate='01.01.2021', complete_reservation='выполнено')
        db.session.add(r)
        db.session.commit()
        assert r.reservationdate=='01.01.2021'
        assert r.complete_reservation=='выполнено'

    def test_editions(self):
        e = Editions(received_editions='полученные издания', name_of_editions='название изданий', index='индекс')
        db.session.add(e)
        db.session.commit()
        assert e.received_editions=='полученные издания'
        assert e.name_of_editions=='название изданий'
        assert e.index=='индекс'


    def test_subscription(self):
        s = Subscription(start_date='01.01.2021', end_date='02.01.2021', for_year=True, half_year=False, price='2000 рублей', name_of_editions='название изданий', method_of_receiving='метод доставки')
        db.session.add(s)
        db.session.commit()
        assert s.start_date=='01.01.2021'
        assert s.end_date=='02.01.2021'
        assert s.for_year==True
        assert s.half_year==False
        assert s.price=='2000 рублей'
        assert s.name_of_editions=='название изданий'
        assert s.method_of_receiving=='метод доставки'
        
        

    def test_method_of_delivery(self):
        m = Method_of_delivery(method_of_receiving='метод получения', estimated_date='предположительная дата')
        db.session.add(m)
        db.session.commit()
        assert m.method_of_receiving=='метод получения'
        assert m.estimated_date=='предположительная дата'
        
        
    def test_received_editions(self):
        re = Received_editions(date_of_received='03.01.2021', name_of_editions='название изданий', number_of_editions='1 издание', index='индекс', name_of_stuff='имя сотрудника')
        db.session.add(re)
        db.session.commit()
        assert re.date_of_received=='03.01.2021'
        assert re.name_of_editions=='название изданий'
        assert re.number_of_editions=='1 издание'
        assert re.index=='индекс'
        assert re.name_of_stuff=='имя сотрудника'
        
        
    def test_stuff(self):
        st = Stuff(name_of_stuff='имя сотрудника', adress_of_stuff='адрес сотрудника', numberphone='123 номер телефона')
        db.session.add(st)
        db.session.commit()
        assert st.name_of_stuff=='имя сотрудника'
        assert st.adress_of_stuff=='адрес сотрудника'
        assert st.numberphone=='123 номер телефона'     

if __name__ == '__main__':
    unittest.main()