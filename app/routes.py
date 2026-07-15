from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, current_app
from flask_mail import Message
from datetime import datetime

from app import db, mail
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
        try:
            reserve_date = datetime.strptime(request.form['reserve_date'], '%Y-%m-%d').date()
            reserve_time = datetime.strptime(request.form['reserve_time'], '%H:%M').time()
        except ValueError:
            return jsonify(ok=False, message='Проверьте формат даты и времени'), 400

        b = Booking(
            name=request.form['name'],
            email=request.form['email'],
            phone=request.form.get('phone'),
            guests=request.form.get('guests', 1),
            reserve_date=reserve_date,
            reserve_time=reserve_time,
        )
        db.session.add(b)
        db.session.commit()
        send_booking_email(b)
        return jsonify(ok=True, message='Столик забронирован, ждите подтверждения на email')
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
        return jsonify(ok=True, message='Сообщение отправлено')
    return render_template('contact.html')


@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if User.query.filter_by(email=request.form['email']).first():
            return jsonify(ok=False, message='Пользователь с таким email уже существует')
        user = User(email=request.form['email'])
        user.set_password(request.form['password'])
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        return jsonify(ok=True, message='Регистрация прошла успешно')
    return render_template('register.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and user.check_password(request.form['password']):
            session['user_id'] = user.id
            return jsonify(ok=True, message='Вход выполнен')
        return jsonify(ok=False, message='Неверный email или пароль')
    return render_template('login.html')


@main.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('main.home'))


def send_booking_email(booking):
    if not current_app.config.get('MAIL_USERNAME'):
        return

    admin_msg = Message(
        subject='Новая бронь столика — Hungry People',
        recipients=[current_app.config['MAIL_USERNAME']],
        body=(
            f'{booking.name} ({booking.email}, {booking.phone or "-"})\n'
            f'Гостей: {booking.guests}\n'
            f'Дата/время: {booking.reserve_date} {booking.reserve_time}'
        ),
    )

    customer_msg = Message(
        subject='Ваша бронь столика подтверждена — Hungry People',
        recipients=[booking.email],
        body=(
            f'Здравствуйте, {booking.name}!\n\n'
            f'Столик забронирован на {booking.reserve_date} в {booking.reserve_time}, '
            f'гостей: {booking.guests}.\n\n'
            f'Если это не вы — просто проигнорируйте это письмо.'
        ),
    )

    for msg in (admin_msg, customer_msg):
        try:
            mail.send(msg)
        except Exception as exc:
            print('ОШИБКА ОТПРАВКИ ПИСЬМА:', exc)
            current_app.logger.warning('Не удалось отправить письмо: %s', exc)
