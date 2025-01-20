from flask import render_template, redirect, request, flash, url_for, abort, jsonify
from flask_login import login_user, current_user, LoginManager, logout_user, login_required

from decorators import admin_required
from ext import app
from forms import RegisterForm, LoginForm
from models import Tea, User, Like, db

login_manager = LoginManager(app)
login_manager.login_view = "login"


@app.route('/')
def index():
    teas = Tea.query.all()
    return render_template('index.html', teas=teas)


@app.route('/shop')
def shop():
    teas = Tea.query.all()
    return render_template('shop.html', teas=teas)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        flash('Thank you for your message!', 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html')


@app.route('/register.html', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect("/")

    form = RegisterForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect('/register.html')

        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect('/login.html')

    return render_template('register.html', form=form)


@app.route("/login.html", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/")
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/")
    return render_template("login.html", form=form)


@app.route('/add_tea', methods=["GET", "POST"])
@admin_required
def add_tea():
    if not current_user.is_authenticated or current_user.role != 'admin':
        abort(403)
    if request.method == "POST":
        tea_name = request.form.get('name')
        tea_description = request.form.get('description')
        tea_price = float(request.form.get('price'))
        tea_category = request.form.get('category')

        existing_tea = Tea.query.filter_by(name=tea_name).first()
        if existing_tea:
            flash("Tea already exists!", "danger")
            return redirect('/add_tea')

        new_tea = Tea(name=tea_name, description=tea_description, price=tea_price, category=tea_category)

        db.session.add(new_tea)
        db.session.commit()
        flash("Tea added successfully!", "success")
        return redirect('/')

    return render_template('add_tea.html')


@app.route('/tea/<int:tea_id>', endpoint='tea_details_page')
def tea_details(tea_id):
    tea = Tea.query.get_or_404(tea_id)
    return render_template('tea_details.html', tea=tea)


@app.route('/delete_tea/<int:tea_id>', methods=['POST'])
@admin_required
def delete_tea(tea_id):
    tea = Tea.query.get(tea_id)

    if tea:
        db.session.delete(tea)
        db.session.commit()

    return redirect(url_for('shop'))


@app.route("/admin_dashboard")
def admin_dashboard():
    return render_template("admin_dashboard")


@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@app.route('/like_tea', methods=['POST'])
@login_required
def like_tea():
    try:
        data = request.get_json()
        tea_id = data.get('tea_id')
        if not tea_id:
            return jsonify({'error': 'Missing tea_id'}), 400

        tea = Tea.query.get(tea_id)
        if not tea:
            return jsonify({'error': 'Tea not found'}), 404

        existing_like = Like.query.filter_by(user_id=current_user.id, tea_id=tea_id).first()
        if existing_like:
            return jsonify({'error': 'You have already liked this tea'}), 400

        new_like = Like(user_id=current_user.id, tea_id=tea_id)
        db.session.add(new_like)
        tea.likes += 1
        db.session.commit()

        return jsonify({'message': 'Tea liked successfully', 'likes': tea.likes}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
