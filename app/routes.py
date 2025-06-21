import os
from flask import render_template, request, redirect, url_for, jsonify, flash, send_file, make_response
from . import db
from .models import Menenger, Klient, Event
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import requests

def init_routes(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.route('/')
    def index():
        return render_template('index.html', current="index")
    
    @app.route('/menengers')
    @login_required
    def menengers():
        menengers = Menenger.query.all()
        return render_template('menenger.html', current="menengers", menengers=menengers)

    @app.route('/menenger/add', methods=["GET", "POST"])
    @login_required
    def menenger_add():
        if request.method == "GET":
            return render_template('menenger/add.html', current="menengers")
        if request.method == "POST":
            user = Menenger()
            user.menengername = request.form["menengername"]
            user.number_phone = request.form["number_phone"]
            user.password = request.form["password"]
            db.session.add(user)
            db.session.commit()
            return redirect("/menengers")

    @app.route('/menenger/edit/<id>', methods=["GET", "POST"])
    @login_required
    def menenger_edit(id):
        if request.method == "GET":
            menenger = db.get_or_404(Menenger, id)
            return render_template('menenger/edit.html', current="menengers", menenger=menenger)
        if request.method == "POST":
            user = db.get_or_404(Menenger, request.form["id"])
            user.menengername = request.form["menengername"]
            user.number_phone = request.form["number_phone"]
            user.password = request.form["password"]
            db.session.commit()
            return redirect("/menengers")

    @app.route('/menenger/del/<id>', methods=["GET", "POST"])
    @login_required
    def menenger_del(id):
        if request.method == "GET":
            menenger = db.get_or_404(Menenger, id)
            return render_template('menenger/del.html', current="menengers", menenger=menenger)
        if request.method == "POST":
            user = db.get_or_404(Menenger, request.form["id"])
            db.session.delete(user)
            db.session.commit()
            return redirect("/menengers")

    @app.route('/klients')
    @login_required
    def klients():
        klients = Klient.query.all()
        return render_template('klient.html', current="klients", klients=klients)

    @app.route('/klient/add', methods=["GET", "POST"])
    @login_required
    def klient_add():
        if request.method == "GET":
            return render_template('klient/add.html', current="klients")
        if request.method == "POST":
            klient = Klient()
            klient.klientname = request.form["klientname"]
            klient.number_phone = request.form["number_phone"]
            klient.VIP_status = request.form["VIP_status"]
            klient.telegram_id = request.form["telegram_id"]
            db.session.add(klient)
            db.session.commit()
            return redirect("/klients")

    @app.route('/klient/edit/<id>', methods=["GET", "POST"])
    @login_required
    def klient_edit(id):
        if request.method == "GET":
            klient = db.get_or_404(Klient, id)
            return render_template('klient/edit.html', current="klients", klient=klient)
        if request.method == "POST":
            klient = db.get_or_404(Klient, request.form["id"])
            klient.klientname = request.form["klientname"]
            klient.number_phone = request.form["number_phone"]
            klient.VIP_status = request.form["VIP_status"]
            klient.telegram_id = request.form["telegram_id"]
            db.session.commit()
            return redirect("/klients")

    @app.route('/klient/del/<id>', methods=["GET", "POST"])
    @login_required
    def klient_del(id):
        klient = db.get_or_404(Klient, id)
        if request.method == "GET":
            return render_template('klient/del.html', current="klients", klient=klient)
        elif request.method == "POST":
            db.session.delete(klient)
            db.session.commit()
            return redirect("/klients")
    
    @app.route('/klient/photo-edit/<id>', methods=["GET", "POST"])
    def klient_photo_edit(id):
        if request.method == "GET":
            klient = db.get_or_404(Klient, id)
            return render_template('klient/add_photo.html', current="klients", klient=klient)
        if request.method == "POST":
            # Проверяем, есть ли файл в запросе
            if 'photo' not in request.files:
                flash('No file part')
                return redirect("/klients")
        
            file = request.files['photo']
        
            # Если пользователь не выбрал файл
            if file.filename == '':
                flash('No selected file')
                return redirect("/klients")
            
            def allowed_file(filename):
                return '.' in filename and filename.rsplit('.', 1)[1].lower() in {"jpg"}
            
            # Если файл разрешен и корректен
            if file and allowed_file(file.filename):
                if not os.path.exists(app.config['IMGS']):
                    os.makedirs(app.config['IMGS'])
                file.save(os.path.abspath(os.path.join(app.config['IMGS'], f"{id}.jpg")))
                return redirect("/klients")
    
        return redirect("/klients")

    @app.route('/klient/photo/<id>', methods=["GET", "POST"])
    def klient_photo(id):
        if request.method == "GET":
            klient = db.get_or_404(Klient, id)
            if os.path.isfile(os.path.join(app.config['IMGS'], f"{id}.jpg")):
                return send_file(os.path.abspath(os.path.join(app.config['IMGS'], f"{id}.jpg")), as_attachment=True)
            else:
                return make_response(f"File '{id}' not found.", 404)
    
    @app.route('/klients/json')
    def klients_all():
        klients = Klient.query.all()
        result = []
        for klient in klients:
            klient_dict = klient.__dict__
            klient_dict.pop('_sa_instance_state', None)  # Удаляем служебное поле SQLAlchemy
            result.append(klient_dict)
        return jsonify(result)

    @app.route('/events')
    @login_required
    def events():
        events = Event.query.all()
        return render_template('events.html', current="events", events=events)

    def send_event_telegram(event):
        klients = Klient.query.all()
        msg = f"{event.type}\n{event.data}\n{event.datetime}"
        url = f"http://{app.config['TELEGRAM_URL']}/send_notification"
        headers = {"X-API-KEY": app.config['TELEGRAM_API_KEY']}
        for klient in klients:
            if klient.telegram_id == None : continue
            data = {
                "user_id": klient.telegram_id,  # ID пользователя из Telegram
                "message": msg
            }
            try:
                response = requests.post(url, json=data, headers=headers)
                if response.status_code != 200:
                    print(f"Ошибка отправки сообщения {data}")
            except requests.exceptions.ConnectionError as e:
                print(f"Ошибка подключения к Telegram Bot")

    @app.route('/event/add', methods=["POST"])
    def event_add():
        if request.method == "POST":
            event = Event()
            event.type = request.json["type"]
            event.data = request.json["data"]
            event.datetime = request.json["datetime"]
            db.session.add(event)
            db.session.commit()
            send_event_telegram(event)
            return make_response("", 200)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
    
        if request.method == 'POST':
            menengername = request.form.get('menengername')
            password = request.form.get('password')
        
            user = Menenger.query.filter_by(menengername=menengername, password=password).first()
            
            if user:
                login_user(user, remember=True)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect("/")
            else:
                flash('Неверное имя пользователя или пароль', 'danger')
    
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect("/")