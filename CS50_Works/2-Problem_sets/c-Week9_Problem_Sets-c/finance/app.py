import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from pytz import timezone
from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
@login_required
def index():
    """Show portfolio of stocks"""

# Check if the user is new"
    rows = db.execute("SELECT * FROM stocks WHERE user_id = ?", session["user_id"])
    total_spent = 0
    if len(rows) == 0:
        return render_template("/index.html")

# Scanning database with lookup function
    for row in rows:
        Valid_data = lookup(row['symbol'])
        for key in Valid_data:
            row[key] = Valid_data[key]

        row['total'] = round(row['shares'] * row['price'], 2)
        total_spent += row['total']

# Variables handling
    Total_account_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    cash = int(Total_account_cash[0]['cash'])
    total_money = int(total_spent + Total_account_cash[0]['cash'])
    return render_template("/index.html", stocks=rows, total=total_money, cash=cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # GET WEBPAGE VIA GET"
    if request.method == "GET":
        return render_template("buy.html")

    # GET WEBPAGE VIA POST"
    if request.method == "POST":

        # Check symbol inputs if blank or number
        symbol = request.form.get("symbol")
        if symbol == None or symbol.isnumeric() == True:
            return apology("The symbol can't be blank or numbers !")

        # Aquire information about symbol & if it exists
        symbol = lookup(request.form.get("symbol"))
        if symbol == None:
            return apology("The symbol doesn't exist")

        # Check share if blank entry or negative or letters"
        shares = request.form.get("shares")
        if shares == None or shares.isnumeric() == False:
            return apology("The shares can't be blank or letters")

        shares = int(request.form.get("shares"))

        purshase = symbol['price'] * shares
        # User account cash check if he can buy or not"
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        user_cash = user_cash[0]['cash']
        user_cash_after_purshase = user_cash - purshase

        if user_cash_after_purshase < 0:
            return apology("There is not enough money")

        # Transaction making & saving"

        # Update user_account cash"
        db.execute("UPDATE users SET cash = ? WHERE id = ?", user_cash_after_purshase, session["user_id"])

        # Check putting data for the first time"
        rows = db.execute("SELECT * FROM stocks WHERE user_id = ? AND symbol = ?", session["user_id"], symbol['symbol'])

        # Generate transaction NO
        transaction_ID = db.execute("INSERT INTO user_transactions(user_id) VALUES(?)", session["user_id"])

        # Put data into transactions table
        db.execute("INSERT INTO transactions(user_id,symbol,name,shares,price,type,transaction_id) VALUES (?,?,?,?,?,?,?)",
                   session["user_id"], symbol['symbol'], symbol['name'], shares, usd(symbol['price']), "Buy", transaction_ID)

        if len(rows) != 1:
            db.execute("INSERT INTO stocks(user_id,symbol,shares) VALUES (?,?,?)", session["user_id"], symbol['symbol'], shares)

        # If not the first time put data normally keep update only shares"
        else:
            shares_old = db.execute("SELECT shares FROM stocks WHERE user_id = ? AND symbol = ?",
                                    session["user_id"], symbol['symbol'])
            shares_old = shares_old[0]['shares']
            new_shares = shares_old + shares
            db.execute("UPDATE stocks SET shares = ? WHERE user_id = ? AND symbol = ? ",
                       new_shares, session["user_id"], symbol['symbol'])
    return redirect("/")


@app.route("/history", methods=["GET"])
@login_required
def history():
    """Show history of transactions"""
    "Transactions Variables"
    stocks = db.execute("SELECT * FROM transactions WHERE user_id = ?", session["user_id"])

# Scanning database with function lookup
    for stock in stocks:
        Valid_data = lookup(stock["symbol"])
        for key in Valid_data:
            stock[key] = Valid_data[key]

# Check if user didn't bought anything yet
    if len(stocks) == 0:
        return apology("you haven't bought anything yet")

# Aquiring Data from database
    for stock in stocks:
        stock = db.execute("SELECT transaction_id FROM transactions WHERE user_id = ?", session["user_id"])[0]

    return render_template("/history.html", stocks=stocks)


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

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


@app.route("/resetpassword", methods=["GET", "POST"])
def resetpassword():

    # If user gets page by get
    if request.method == "GET":
        return render_template("resetpassword.html")

    # If user gets page by post
    else:

        # Checking the username in database for valid account
        username_check = request.form.get("username")
        username = db.execute("SELECT * from users WHERE username = ?", username_check)
        if len(username) != 1:
            return apology("Username you've entered doesn't exist")
        else:

            # Checking if the entry two passwords is not the same
            new_password = request.form.get("resetpassword")
            passwordconfirmation = request.form.get("passwordconfirmation")
            if new_password != passwordconfirmation:
                return apology("Passwords must be the same")

            # Checking if the old password is the same as the new one
            old_password = db.execute("SELECT hash FROM users WHERE username = ?", username_check)
            same_password = check_password_hash(old_password, new_password)
            if same_password != 0:
                return apology("Password can't be the same as the old one !")

            # Implementing the new password hash to database
            hash_pass = generate_password_hash(new_password)
            db.execute("UPDATE users SET hash = ? WHERE username = ?", hash_pass, request.form.get("username"))
            return redirect("/")


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

    # If user gets page by get
    if request.method == "GET":
        return render_template("quote.html")

    # If user gets page by post
    else:

        # Check If user enters blank
        if request.form.get("symbol") == None:
            return apology("The symbol can't be blank")

    # Check if symbol isn't exist
        symbol = lookup(request.form.get("symbol"))
        if symbol == None:
            return apology("The symbol you've entered is not available")

    # Rendering page
        return render_template("quoted.html", symbol=symbol)


@app.route("/register", methods=["GET", "POST"])
def register():

    # Forget any user_id
    session.clear()

    if request.method == "GET":
        render_template("/register.html")

    if request.method == "POST":

        # New username entry
        username = request.form.get("username")

        # Blank username
        if not request.form.get("username"):
            return apology("User name is requried")

        # Checking for indentical username
        userdata = db.execute("SELECT * from users WHERE username = ?", request.form.get("username"))
        if len(userdata) == 1:
            return apology("User name has already taken !")

        # Blank password
        if not request.form.get("password"):
            return apology("Password is not set !")

        # Password & it's confirmation not the same
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Password fields must me the same characters !")

        # Password hashing
        password = generate_password_hash(request.form.get("password"))

        # Account Data insertion
        db.execute("INSERT INTO users (username,hash) VALUES (?)", (username, password))

        # Aquiring session
        return redirect("/")

    # Rendering page
    return render_template("/register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # User getting page & stocks gathering
    if request.method == "GET":
        stocks = db.execute("SELECT * FROM stocks WHERE user_id = ?", session["user_id"])
        return render_template("sell.html", stocks=stocks)

    # User Posting
    if request.method == "POST":

        Sold_stock = request.form.get("symbol")

        # Stock searching & checking availability
        stock = db.execute("SELECT shares FROM stocks WHERE user_id = ? AND symbol = ?",
                           session["user_id"], Sold_stock)
        quantity_available = stock[0]['shares']
        if quantity_available <= 0:
            return apology("Please Select a valid stock on your account")

        # Stock checking quantity
        if request.form.get("shares").isnumeric() == False:
            return apology("Shares cannot be letters")
        quantity_sold = int(request.form.get("shares"))
        if quantity_sold > quantity_available:
            return apology("Cannot sell more than the stocks available")
        new_quantity_share = quantity_available - quantity_sold

        # Stock selling & cash back
        unit_sold_price = lookup(Sold_stock)
        unit_sold_price = unit_sold_price['price']

        # Stock name
        unit_name = lookup(Sold_stock)
        unit_name = unit_name['name']

        # Generate transaction NO"
        transaction_ID = db.execute("INSERT INTO user_transactions(user_id) VALUES(?)", session["user_id"])

        # New cash saving into account
        cash_back = unit_sold_price * quantity_sold
        cash_available = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash_available = cash_available[0]['cash']
        cash_after_selling = cash_available + cash_back
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash_after_selling, session["user_id"])

        # Update shares quantity into stocks
        db.execute("UPDATE stocks SET shares = ? WHERE user_id = ? AND symbol = ?",
                   new_quantity_share, session["user_id"], Sold_stock)

        # History of transactions
        db.execute("INSERT INTO transactions(user_id,symbol,name,shares,price,type,transaction_id) VALUES (?,?,?,?,?,?,?)",
                   session["user_id"], Sold_stock, unit_name, quantity_sold, unit_sold_price, "Sell", transaction_ID)

        # Rendering page
        return redirect("/")


@app.route("/charge", methods=["GET", "POST"])
@login_required
def charge():

    # User Getting Page
    if request.method == "GET":
        return render_template("/charge.html")

    # User Posting page
    if request.method == "POST":

        # User input money
        cash_charge = request.form.get("charge")

        # Check invalid input or blank
        if not cash_charge:
            return apology("Please Enter cash")
        if cash_charge.isnumeric() == False:
            return apology("Please Enter Valid Number")
        cash_charge = int(cash_charge)

        # User new cash in account
        cash_available = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash_available = cash_available[0]['cash']
        cash_balance = cash_available + cash_charge

        # deploy new cash
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash_balance, session["user_id"])

        # Rendering page
        return redirect("/")

@app.route("/query", methods =["GET","POST"])
@login_required
def query():

    #Only Admin enters
    if session['user_id'] != 3:
        return apology("Cannot access this page",403)

    #Query page by get
    if request.method == "GET":
        return render_template("/query.html")

    # User getting page by Post
    if request.method == "POST":

        # User input data query
        user_name_entered = request.form.get("username_entered")
        user_symbol_selected = request.form.get("symbol_entered")
        user_time_stamp_from = request.form.get("timestampfrom")
        user_time_stamp_to = request.form.get("timestampto")
        user_transaction_type = request.form.get("transaction_type")

        user_id = db.execute("SELECT id FROM users WHERE username = ?",user_name_entered)
        user_id = user_id[0]['id']
        if user_id == None:
            return apology("No username valid")

        transactions = db.execute("SELECT * FROM transactions WHERE user_id = ? AND symbol = ? AND type = ? AND Timestamp >= ? AND Timestamp <= ?",user_id,user_symbol_selected,user_transaction_type,user_time_stamp_from,user_time_stamp_to)

        return render_template("/query.html",transactions = transactions)

