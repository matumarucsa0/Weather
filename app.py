from flask import Flask, render_template, redirect, request
import sqlite3

from fuzzywuzzy import fuzz
import unidecode

#???
import smtplib
import ssl
from email.message import EmailMessage

email = EmailMessage()
sender = "maruscak2006@gmail.com"
email["From"] = sender
reciever = "maruscak.matus@gmail.com"
passowrd = "cqcrdtyepasvxwyt"
subject = "Password"

body = """
Hello, your password is: 0000
"""

email["To"] = reciever
email["Subject"] = subject
email.set_content(body)
context = ssl.create_default_context()
#???

app = Flask(__name__)
conn = sqlite3.connect("data.db", check_same_thread=False)

@app.route("/")
def df():
    return redirect("/log-in")

@app.route("/log-in", methods=["GET", "POST"])
def LogIn():
    if request.method == "POST":
        if request.form.get("button") != None:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(sender, passowrd)
                smtp.sendmail(sender, reciever, email.as_string())
            return redirect("/log-in")

        else:
            password = request.form.get("pass")

            if password == "0000":
                #add log !!!
                return redirect("/homepage")
            else:
                return render_template("log-in.html", forgot="Incorrect password")

    else:
        return render_template("log-in.html")


@app.route("/homepage", methods=["GET", "POST"])
def homepage():
    if request.method == "POST":
        v = request.form.get("remove")
        data = conn.execute(f"DELETE FROM tracked_locations WHERE id = {v}")
        return redirect("/homepage")
    else:
        data = conn.execute("SELECT * FROM locations_db WHERE ID in (SELECT * FROM tracked_locations);").fetchall()

        return render_template("homepage.html", items=data)

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        response_ = []

        res = conn.execute("SELECT * FROM locations_db").fetchall()
        val = request.form.get("search")
        val = unidecode.unidecode(val.lower())
        
        for x in res:
            
            f = fuzz.ratio(unidecode.unidecode(x[1].lower()), val)
            
            if f > 60:
                response_.append((x, f))

        response_.sort(key = lambda x: x[1], reverse=True)
        response_f = []
        for x in response_:
            response_f.append(x[0])


        return render_template("search.html", results = response_f)
    else:
        r = conn.execute("SELECT * FROM locations_db").fetchall()
        r.sort(key= lambda x: x[1])
        return render_template("search.html", results = r)


@app.route("/search-", methods=["GET", "POST"]) #handles adding of locations
def search_():
    v = request.form.get("add")
    conn.execute(f"INSERT INTO tracked_locations (id) VALUES({v})")
    return redirect("/homepage")
        