from flask import Flask, redirect, url_for, render_template, request, session, flash
from dbconnector import useractions
import json

app = Flask(__name__)
app.secret_key = "doinkboinkwithmammajoink"


@app.route("/home/", methods=["POST", "GET"])
@app.route("/", methods=["POST", "GET"])
def home():
    return render_template("home.html", page="home")


@app.route("/login/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        usermail = request.form["umail"]
        userpwd = request.form["upwd"]
        login = useractions.login(useractions, usermail, userpwd)
        if login:
            flash("Sucessful Login!", "info")
            if session["role"] == "ADMIN":
                return redirect(url_for("admin", page="admin"))
            else:
                return redirect(url_for("usersession", page="session"))
        else:
            flash("Login Failed", "danger")
    status = request.args.get("status")
    if status:
        if status == "register_success":
            flash("Register Sucessful, Please Log-In", "success")
    return render_template("login.html", page="login")
@app.route("/register/", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        uname = request.form["uname"]
        upwd = request.form["upwd"]
        umail = request.form["umail"]
        useractions.adduser(useractions, uname, upwd, umail)
    return render_template("register.html", page="register")


@app.route("/u/<name>/", methods=["POST", "GET"])
def user(name):
    return render_template("user.html", uname=name, page="user")


@app.route("/admin/", methods=["POST", "GET"])
def admin():
    if not session:
        return redirect(url_for("login", page="login"))
    else:
        if not session["uid"]:
            return redirect(url_for("login", page="login"))
        else:
            if request.method == "POST":
                req = json.loads(request.data)
                useractions.approveOrDenyLoan(
                    useractions, req["loanId"], req["approved"]
                )
                return redirect(url_for("admin", page="admin"))
            else:
                acc = useractions.getAccDetail(
                    useractions, session["apiKey"], session["uid"]
                )
                data = useractions.getLoanRequests(
                    useractions, session["accno"], session["apiKey"]
                )
                if acc:
                    return render_template("admin.html", page="admin", loans=data)
                else:
                    return redirect(url_for("login", page="login"))


@app.route("/session/", methods=["POST", "GET"])
def usersession():
    if not session:
        return redirect(url_for("login", page="login"))
    else:
        if not session["uid"]:
            return redirect(url_for("login", page="login"))
        else:
            acc = useractions.getAccDetail(
                useractions, session["apiKey"], session["uid"]
            )
            if acc:
                return render_template("session.html", page="session")
            else:
                return redirect(url_for("login", page="login"))


@app.route("/session/b2btransfer/", methods=["POST", "GET"])
def b2btransfer():
    if not session:
        return redirect(url_for("login", page="login"))
    else:
        if not session["uid"]:
            return redirect(url_for("login", page="login"))
        else:
            if request.method == "POST":
                accno = request.form["accno"]
                amount = request.form["amount"]
                transfer = useractions.transfer(
                    useractions, accno, session["accno"], amount, False
                )
                if transfer:
                    flash("Sucessful Transfer!", "info")
                else:
                    flash("Transfer failed", "danger")
            acc = useractions.getAccDetail(
                useractions, session["apiKey"], session["uid"]
            )
            if acc:
                return render_template("b2btransfer.html", page="b2btransfer")
            else:
                return redirect(url_for("login", page="login"))


@app.route("/session/localtransfer/", methods=["POST", "GET"])
def localtransfer():
    if not session:
        return redirect(url_for("login", page="login"))
    else:
        if not session["uid"]:
            return redirect(url_for("login", page="login"))
        else:
            if request.method == "POST":
                accno = request.form["accno"]
                amount = request.form["amount"]
                transfer = useractions.transfer(
                    useractions, accno, session["accno"], amount, True
                )
                if transfer:
                    flash("Sucessful Transfer!", "info")
                else:
                    flash("Transfer failed", "danger")
            acc = useractions.getAccDetail(
                useractions, session["apiKey"], session["uid"]
            )
            if acc:
                return render_template("localtransfer.html", page="localtransfer")
            else:
                return redirect(url_for("login", page="login"))


@app.route("/session/internationaltransfer/", methods=["POST", "GET"])
def interantionaltransfer():
    if not session:
        return redirect(url_for("login", page="login"))
    else:
        if not session["uid"]:
            return redirect(url_for("login", page="login"))
        else:
            if request.method == "POST":
                accno = request.form["accno"]
                amount = request.form["amount"]
                transfer = useractions.transfer(
                    useractions, accno, session["accno"], amount, True
                )
                if transfer:
                    flash("Sucessful Transfer!", "info")
                else:
                    flash("Transfer failed", "danger")
            acc = useractions.getAccDetail(
                useractions, session["apiKey"], session["uid"]
            )
            if acc:
                return render_template("localtransfer.html", page="localtransfer")
            else:
                return redirect(url_for("login", page="login"))


@app.route("/session/history/", methods=["POST", "GET"])
def userhistory():
    if not session:
        return redirect(url_for("login", page="login"))
    else:
        if not session["uid"]:
            return redirect(url_for("login", page="login"))
        else:
            acc = useractions.getAccDetail(
                useractions, session["apiKey"], session["uid"]
            )
            if acc:
                history = useractions.getTransferHistory(
                    useractions, session["accno"], session["apiKey"]
                )
                return render_template(
                    "transferstatement.html", page="transferstatement", history=history
                )
            else:
                return redirect(url_for("login", page="login"))


@app.route("/session/nriterms", methods=["POST", "GET"])
def nriterms():
    if not session:
        return redirect(url_for("login", page="login"))
    else:
        if not session["uid"]:
            return redirect(url_for("login", page="login"))
        else:
            return render_template("tandc.html", page="nriterms")


@app.route("/session/delete", methods=["POST", "GET"])
def delete():
    if not session:
        return redirect(url_for("login", page="login"))
    else:
        if not session["uid"]:
            return redirect(url_for("login", page="login"))
        else:
            if request.method == "POST":
                useractions.deleteUser(useractions, session["uid"])
                return redirect(url_for("logout", page="logout"))
            else:
                return render_template("delete.html", page="delete")


@app.route("/session/loan/", methods=["POST", "GET"])
def loan():
    if not session:
        return redirect(url_for("login", page="login"))
    else:
        if not session["uid"]:
            return redirect(url_for("login", page="login"))
        else:
            if request.method == "POST":
                submit = useractions.addEntry(useractions, list(request.form.lists()))
                if submit:
                    flash("Sucessfuly submitted application!", "info")
                else:
                    flash("Submition failed", "danger")
            acc = useractions.getAccDetail(
                useractions, session["apiKey"], session["uid"]
            )
            if acc:
                return render_template("loan.html", page="loan")
            else:
                return redirect(url_for("login", page="login"))


@app.route("/session/insurance/", methods=["POST", "GET"])
def insurance():
    if not session:
        return redirect(url_for("login", page="login"))
    else:
        if not session["uid"]:
            return redirect(url_for("login", page="login"))
        else:
            if request.method == "POST":
                submit = useractions.addEntry(useractions, request.form)
                if submit:
                    flash("Sucessfuly submitted application!", "info")
                else:
                    flash("Submition failed", "danger")
            acc = useractions.getAccDetail(
                useractions, session["apiKey"], session["uid"]
            )
            if acc:
                return render_template("insurance.html", page="insurance")
            else:
                return redirect(url_for("login", page="login"))


@app.route("/session/nri", methods=["GET"])
def nri():
    flash("Submitted Application!", "info")
    return redirect(url_for("usersession", page="session"))


@app.route("/logout/", methods=["POST", "GET"])
def logout():
    if "uid" in session:
        session.clear()
        flash("Sucessful Logout!", "info")
        return redirect(url_for("home", page="home"))
    else:
        return redirect(url_for("home", page="home"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", page="404"), 404


if __name__ == "__main__":
    app.run(debug=True, port=42069)
