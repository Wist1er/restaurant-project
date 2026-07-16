from app import create_app, db
from app.models import StaticPage, Speciality, MenuItem, Event

app = create_app()

with app.app_context():
    db.create_all()

    db.session.add(StaticPage(section='about', title='About Us', text='Lorem ipsum dolor sit amet.'))
    db.session.add(StaticPage(section='team', title='Master Chef', text='Lorem ipsum dolor sit amet.'))
    db.session.add(Speciality(title='Beefsteak with truffle sauceh', subtitle='Marbled beef, black truffle sauce', image='img/food1.png'))
    db.session.add(Speciality(title='Duck breast with cherry glaze', subtitle='Cherry glaze, mashed potatoes', image='img/food2.png'))
    db.session.add(MenuItem(title='Tomato Soup', price=5.5, category='soupe', on_main=True))
    db.session.add(MenuItem(title='Margherita Pizza', price=8.9, category='pizza', on_main=True))
    db.session.add(MenuItem(title='Cream of Mushroom Soup', price=6.5, category='soupe', on_main=True))
    db.session.add(MenuItem(title='Caesar Salad', price=7, category='salad', on_main=True))
    db.session.add(MenuItem(title='Grilled Salmon', price=14.5, category='main', on_main=True))
    db.session.add(MenuItem(title='Beef Bourguignon', price=16, category='main', on_main=True))
    db.session.add(MenuItem(title='Pepperoni Pizza', price=9.9, category='pizza', on_main=True))
    db.session.add(MenuItem(title='Tiramisu', price=5.5, category='dessert', on_main=True))
    db.session.add(Event(title='Сorporate event', image='img/Rectangle (3).png'))
    db.session.add(Event(title='Weddings', image='img/Rectangle (2).png'))

    db.session.commit()
    print('Seed done')
