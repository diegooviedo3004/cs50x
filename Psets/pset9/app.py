 from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
 
# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # selecciona el simbolo que posee el usuario con sus acciones
    stocks = db.execute(
        "SELECT symbol, name, price, SUM(shares) AS total_shares FROM transactions WHERE user_id = :id GROUP BY symbol HAVING total_shares > 0", id=session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])[0]["cash"]

    # guarda el dinero mas las acciones
    total = cash
    # actualiza cada simbolo del portafolio, precio y total
    # stock in stocks:
    #   for total += stock["price"] * stock["total_shares"]
    return render_template("index.html", stocks=stocks, cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        # busqueda del simbolo
        symbol = lookup(request.form.get("symbol"))
        if not symbol:
            return apology("simbolo invalido", 400)

        # verifica la cantidad apropiada de acciones
        try:
            shares = int(request.form.get("shares"))
            if shares < 0:
                return apology("por favor ingrese un numero positivo")
        except:
            return apology("por favor ingrese un numero positivo")

        # selecciona el dinero del usuario
        cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])

        nom_sim = symbol["name"]
        precio_sim = symbol["price"]
        sym = symbol["symbol"]
        total_precio = precio_sim * shares
        print(usd(total_precio))
        print(cash[0]["cash"])
        # verifica la cantidad de dinero disponible
        if float(cash[0]["cash"]) < total_precio:
            return apology("no tienes suficiente dinero")
        else:
            # actualiza el cash y transacciones realizadas
            db.execute("UPDATE users SET cash = cash - :total_precio WHERE id = :id",
                       id=session["user_id"], total_precio=total_precio)

            db.execute("INSERT INTO transactions (name, shares, price, symbol, user_id) VALUES(:name, :shares, :price, :symbol, :id)",
                       name=nom_sim, shares=shares, price=precio_sim, symbol=sym, id=session["user_id"])

        return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT symbol, price, shares FROM transactions WHERE id = :id", id=session["user_id"])
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        # busca simbolo
        symbol = lookup(request.form.get("symbol"))

        # si el simbolo no existe
        if not symbol:
            return apology("símbolo inválido")

        return render_template("quoted.html", stock=symbol, usdfunc=usd)
    # si exista regresa a quote
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        usuario = request.form.get("username")
        contra = request.form.get("password")
        confirm = request.form.get("confirmation")
        # asegura que el username sea ingresada
        if not usuario:
            return apology("por favor ingrese su usuario", 400)
        # asegura que la contraseña sea ingresada
        elif not contra:
            return apology("por favor ingrese su contraseña", 400)

        elif contra != confirm:
            return apology("las contraseñas no coinciden")

        val = db.execute("SELECT username FROM users WHERE username = :username", username=usuario)

        if len(val) >= 1:
            return apology("el usuario ya existe")
        else:
            # agrega un nuevo usuario a la tabla
            query = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                               username=usuario, hash=generate_password_hash(request.form.get("password")))

        if not query:
            return apology("el usuario ya existe")

        session["user_id"] = query
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = lookup(request.form.get("symbol"))
        if not symbol:
            return apology("Símbolo inválido")
        try:
            shares = int(request.form.get("shares"))
            if shares <= 0:
                return apology("por favor ingrese un numero positivo")

        except:
            return apology("por favor ingrese un numero positivo")

        price_simb = symbol["price"]
        nom_simb = symbol["name"]
        price = shares * price_simb
        sym = symbol["symbol"]

        acciones_usuario = db.execute(
            "SELECT shares FROM transactions WHERE user_id = :id AND symbol = :symbol GROUP BY symbol", id=session["user_id"], symbol=sym)

        if acciones_usuario[0]["shares"] < shares:
            return apology("no tienes suficientes acciones")

        cash_actual = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])[0]["cash"]
        db.execute("UPDATE users SET cash = ? WHERE id = ?", (cash_actual + price), session["user_id"])
        db.execute("INSERT INTO transactions (user_id, name, shares, price, symbol) VALUES(:id, :name, :shares, :price, :symbol)",
                   id=session["user_id"], name=nom_simb, shares=-shares, price=price_simb, symbol=sym)
        return redirect("/")
    else:
        tabla = db.execute(
            "SELECT symbol, SUM(shares) AS acciones FROM transactions WHERE user_id = :id GROUP BY symbol having acciones > 0", id=session["user_id"])
        return render_template("sell.html", symbols=tabla)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
