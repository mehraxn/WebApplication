from flask import render_template


def admin_dashboard():
    """Display the placeholder Guild Council Admin dashboard."""
    return render_template("admin_dashboard.html")
