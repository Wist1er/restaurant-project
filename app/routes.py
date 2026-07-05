from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from app import db
from app.models import User, StaticPage, Speciality, MenuItem, Event, Booking, ContactMessage

main = Blueprint('main', __name__)


@main.route('/')
def home():
    about = StaticPage.query.filter_by(section='about').all()
    team = StaticPage.query.filter_by(section='team').all()
    specialities = Speciality.query.all()
    events = Event.query.all()
    menu_items = MenuItem.query.filter_by(on_main=True).limit(21).all()

    return render_template(
        'index.html',
        about=about, team=team, specialities=specialities,
        events=events, menu_items=menu_items,
    )


@main.route('/menu')
def menu():
    items = MenuItem.query.all()
    return render_template('menu.html', items=items)


@main.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        b = Booking(
            name=request.form['name'],
            email=request.form['email'],
            phone=request.form.get('phone'),
            guests=request.form.get('guests', 1),
            reserve_date=request.form['reserve_date'],
            reserve_time=request.form['reserve_time'],
        )
        db.session.add(b)
        db.session.commit()
        flash('Столик забронирован')
        return redirect(url_for('main.home'))
    return render_template('booking.html')


@main.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        msg = ContactMessage(
            name=request.form['name'],
            email=request.form['email'],
            message=request.form['message'],
        )
        db.session.add(msg)
        db.session.commit()
        flash('Сообщение отправлено')
        return redirect(url_for('main.home'))
    return render_template('contact.html')


@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(email=request.form['email'])
        user.set_password(request.form['password'])
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        return redirect(url_for('main.home'))
    return render_template('register.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and user.check_password(request.form['password']):
            session['user_id'] = user.id
            return redirect(url_for('main.home'))
        flash('Неверный email или пароль')
    return render_template('login.html')


@main.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('main.home'))
