"""Expense Tracker — a small Flask app to track expenses by category.

Uses Flask + sqlite3 only (no SQLAlchemy, no Flask-WTF).
"""
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash, abort

import database

app = Flask(__name__)
app.secret_key = "dev-secret-key"  # required for flash messages

database.init_db()


def validate_expense(title, amount_raw, category, date):
    """Validate form input. Returns (error_message, amount) — error is None if valid."""
    if not title:
        return "Title is required.", None
    # amount must be a positive number
    try:
        amount = float(amount_raw)
    except (TypeError, ValueError):
        return "Amount must be a number.", None
    if amount <= 0:
        return "Amount must be positive.", None
    if not category or category not in database.CATEGORIES:
        return "Please choose a valid category.", None
    if not date:
        return "Date is required.", None
    # date must be a real YYYY-MM-DD date
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return "Date must be in YYYY-MM-DD format.", None
    return None, amount


@app.route("/")
def index():
    category_filter = request.args.get("category", "all")
    if category_filter != "all" and category_filter not in database.CATEGORIES:
        category_filter = "all"

    expenses = database.get_expenses(category_filter)
    total = database.get_total(category_filter)
    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        categories=database.CATEGORIES,
        current_category=category_filter,
    )


@app.route("/add", methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        amount_raw = request.form.get("amount", "").strip()
        category = request.form.get("category", "")
        date = request.form.get("date", "").strip()
        note = request.form.get("note", "").strip()

        error, amount = validate_expense(title, amount_raw, category, date)
        if error:
            flash(error, "danger")
            return render_template(
                "add_expense.html",
                categories=database.CATEGORIES,
                title=title,
                amount=amount_raw,
                category=category,
                date=date,
                note=note,
            )

        database.add_expense(title, amount, category, date, note)
        flash("Expense added.", "success")
        return redirect(url_for("index"))

    # GET: show empty form with today's date pre-filled
    return render_template(
        "add_expense.html",
        categories=database.CATEGORIES,
        date=datetime.now().strftime("%Y-%m-%d"),
    )


@app.route("/edit/<int:expense_id>", methods=["GET", "POST"])
def edit_expense(expense_id):
    expense = database.get_expense(expense_id)
    if expense is None:
        abort(404)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        amount_raw = request.form.get("amount", "").strip()
        category = request.form.get("category", "")
        date = request.form.get("date", "").strip()
        note = request.form.get("note", "").strip()

        error, amount = validate_expense(title, amount_raw, category, date)
        if error:
            flash(error, "danger")
            return redirect(url_for("edit_expense", expense_id=expense_id))

        database.update_expense(expense_id, title, amount, category, date, note)
        flash("Expense updated.", "success")
        return redirect(url_for("index"))

    return render_template(
        "edit_expense.html", expense=expense, categories=database.CATEGORIES
    )


@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):
    expense = database.get_expense(expense_id)
    if expense is None:
        abort(404)
    database.delete_expense(expense_id)
    flash("Expense deleted.", "success")
    return redirect(url_for("index"))


@app.route("/summary")
def summary():
    totals = database.get_totals_by_category()
    grand_total = database.get_total("all")
    return render_template("summary.html", totals=totals, grand_total=grand_total)


@app.errorhandler(404)
def not_found(error):
    return render_template("base.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
