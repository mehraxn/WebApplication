"""Flask Blog CRUD App — create, read, update, delete blog posts, with title search.

Uses Flask + sqlite3 only (no SQLAlchemy, no Flask-WTF).
"""
from flask import Flask, render_template, request, redirect, url_for, flash, abort

import database

app = Flask(__name__)
app.secret_key = "dev-secret-key"  # required for flash messages

database.init_db()

TITLE_MAX_LENGTH = 100


def validate_post(title, content, author):
    """Return an error message if invalid, otherwise None."""
    if not title:
        return "Title is required."
    if len(title) > TITLE_MAX_LENGTH:
        return f"Title must be {TITLE_MAX_LENGTH} characters or fewer."
    if not content:
        return "Content is required."
    if not author:
        return "Author is required."
    return None


@app.route("/")
def index():
    # ?q= is the title search term (empty = show all)
    search = request.args.get("q", "").strip()
    posts = database.get_posts(search)
    return render_template("index.html", posts=posts, search=search)


@app.route("/post/<int:post_id>")
def post_detail(post_id):
    post = database.get_post(post_id)
    if post is None:
        abort(404)
    return render_template("post_detail.html", post=post)


@app.route("/create", methods=["GET", "POST"])
def create_post():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        author = request.form.get("author", "").strip()

        error = validate_post(title, content, author)
        if error:
            flash(error, "danger")
            # Re-render the form keeping the user's input
            return render_template(
                "create_post.html", title=title, content=content, author=author
            )

        database.add_post(title, content, author)
        flash("Post created successfully.", "success")
        return redirect(url_for("index"))

    return render_template("create_post.html")


@app.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = database.get_post(post_id)
    if post is None:
        abort(404)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        author = request.form.get("author", "").strip()

        error = validate_post(title, content, author)
        if error:
            flash(error, "danger")
            return redirect(url_for("edit_post", post_id=post_id))

        database.update_post(post_id, title, content, author)
        flash("Post updated successfully.", "success")
        return redirect(url_for("post_detail", post_id=post_id))

    return render_template("edit_post.html", post=post)


@app.route("/delete/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    post = database.get_post(post_id)
    if post is None:
        abort(404)
    database.delete_post(post_id)
    flash("Post deleted.", "success")
    return redirect(url_for("index"))


@app.errorhandler(404)
def not_found(error):
    return render_template("base.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
