from app import create_app, db
from app.models import StaticPage, Speciality, MenuItem, Event

app = create_app()

with app.app_context():
    db.create_all()

    db.session.add(StaticPage(section='about', title='About Us', text='Lorem ipsum dolor sit amet.'))
    db.session.add(StaticPage(section='team', title='Master Chef', text='Lorem ipsum dolor sit amet.'))
    db.session.add(Speciality(title='Grilled Fish'))
    db.session.add(Speciality(title='Steak'))
    db.session.add(MenuItem(title='Tomato Soup', price=5.5, category='soupe', on_main=True))
    db.session.add(MenuItem(title='Margherita Pizza', price=8.9, category='pizza', on_main=True))
    db.session.add(Event(title='Private Events', text='Book your celebration.'))

    db.session.commit()
    print('Seed done')
