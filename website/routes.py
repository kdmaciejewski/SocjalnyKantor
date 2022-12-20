from flask import render_template, url_for, flash, redirect, request, abort
from website import app, db, bcrypt
from website.forms import RegistrationForm, LoginForm, ExchangeForm, PostForm
from website.models import User, Klient, Post
from flask_login import login_user, current_user, logout_user, login_required
from website import prices
#forms pozwalają na sprawdzenie podawanych przez użytkownika danych

@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)  #dzięki temu będziemy mieć dostęp do postów w pliku html


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:   #sprawdzamy czy jest już zalogowany
        return redirect('home')

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Klient(imie=form.username.data, login=form.email.data, haslo=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Poprawnie utworzono użytkownika {form.username.data}! Można się zalogować', 'success')
        #jeżeli poprawnie się zarejestrował to
        return redirect(url_for('login'))
    return render_template('register.html', title='Rejestracja', form=form) #przekazujemy tę instancję RegistrationForm!!

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # sprawdzamy czy jest już zalogowany
        return redirect('home')

    form = LoginForm()
    if form.validate_on_submit():
        user = Klient.query.filter_by(login=form.email.data).first()  #sprawdzamy czy jest taki email w bazie
        if user and bcrypt.check_password_hash(user.haslo, form.password.data):
            login_user(user)                                        #, remember=form.remember.data
            #next_page to strona która wybraliśmy zanim przenieśliśmy się na strone logowania
            #(np nie mielismy dostępu do niej i nas przeniosło)
            next_page = request.args.get('next')
            #przenieś na next_page jeśli istnieje
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Nie udało się zalogować', 'danger')
    return render_template('login.html', title='Logowanie', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/exchange", methods=['GET', 'POST'])
@login_required
def exchange():
    form = ExchangeForm()
    if form.validate_on_submit():
        val1 = int(form.val1.data)
        cur1 = str(form.cur1.data)
        cur2 = str(form.cur2.data)

        res = prices.exchange(val1, cur1, cur2)

        if res[1] == True:
            flash(f'Wymieniono {res[0]}', 'success')
            return render_template('exchange.html', title='Wymiana', form=form)
        else:
            flash('Niepoprawnie podane dane', 'danger')


    return render_template('exchange.html', title='Wymiana', form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    # if form.validate_on_submit():
    if request.method == 'POST':
        post = Post(tytul=form.tytul.data, tresc=form.tresc.data, author=current_user) #autor=current_user
        db.session.add(post)
        db.session.commit()
        flash('Dodano post!', 'success')

        return redirect(url_for('home'))
    return render_template('create_post.html', title='Nowy Post', form=form, legend='Dodaj Post')

@app.route("/post/<int:post_id>")
def post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)

    user = Klient.query.filter_by(login=current_user.login).first() #sprawdzenie czy to klient czy administrator
    if user:
        print('1')
        return render_template('post_klient.html', tytul=post.tytul, post=post)
    else:
        return render_template('post.html', tytul=post.tytul, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):

    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)
    form = PostForm()

    if request.method == 'POST':
        post.tytul= form.tytul.data
        post.tresc = form.tresc.data
        db.session.commit()
        flash('Poprawnie edytowano post', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.tytul.data = post.tytul
        form.tresc.data = post.tresc

    return render_template('create_post.html', title='Edytuj Post',
                           form=form, legend='Edytuj Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()

    flash('Usunięto post', 'success')
    return redirect(url_for('home'))

@app.route("/plotbtc")
@login_required
def plotbtc():
    return render_template('plot-btc.html', title='Wykres BTC')

@app.route("/ploteth")
@login_required
def ploteth():
    return render_template('plot-eth.html', title='Wykres ETH')

@app.route("/plotdoge")
@login_required
def plotdoge():
    return render_template('plot-doge.html', title='Wykres DOGE')

@app.route("/plotbnb")
@login_required
def plotbnb():
    return render_template('plot-bnb.html', title='Wykres BNB')

@app.route("/account")
@login_required
def account():
    ima = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Konto', image_file=ima)

@app.route("/plots")
@login_required
def plots():
    return render_template('plots.html', title='Wymiana')
    