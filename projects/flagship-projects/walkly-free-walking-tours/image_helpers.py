import os

from PIL import Image
from flask import request

from database import get_db_connection


# One real default image used when a tour has no real photo of its own.
DEFAULT_TOUR_IMAGE = "images/places/default-tour-cover.jpg"

# Build an absolute upload folder path so uploads work no matter where the app is started from.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")


def process_uploaded_image(uploaded_file, save_path):
    try:
        image = Image.open(uploaded_file)
        image.load()
    
    except Exception:
        return False

    if image.mode != "RGB":
        image = image.convert("RGB")

    image.save(save_path)
    return True


def save_uploaded_file(uploaded_file, prefix, item_id):
    if uploaded_file is None:
        return ""

    if uploaded_file.filename == "":
        return ""

    filename_parts = uploaded_file.filename.rsplit(".", 1)

    if len(filename_parts) != 2:
        return ""

    extension = filename_parts[-1].lower()

    if extension not in ["jpg", "jpeg", "png", "webp"]:
        return ""

    filename = str(prefix) + "_" + str(item_id) + "." + extension

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    save_path = os.path.join(UPLOAD_FOLDER, filename)

    if not process_uploaded_image(uploaded_file, save_path):
        return ""

    # Templates build image URLs with url_for('static', ...), so keep the stored path relative.
    return "uploads/" + filename


def count_uploaded_photo_files(uploaded_files):
    count = 0

    for x in uploaded_files:
        if x is not None and x.filename != "":
            count = count + 1

    return count


def uploaded_photo_extensions_are_valid(uploaded_files):
    allowed_extensions = ["jpg", "jpeg", "png", "webp"]

    for x in uploaded_files:
        if x is not None and x.filename != "":
            filename_parts = x.filename.rsplit(".", 1)

            if len(filename_parts) != 2:
                return False

            extension = filename_parts[-1].lower()

            if extension not in allowed_extensions:
                return False

    return True


def read_tour_photo_files():
    files = []

    first_photo = request.files.get("tour_image")
    files.append(first_photo)

    for index in range(2, 6):
        files.append(request.files.get("photo_" + str(index)))

    return files


def save_tour_photos(connection, tour_id, uploaded_files, old_main_image=""):
    has_new_photo = False

    for x in uploaded_files:
        if x is not None and x.filename != "":
            has_new_photo = True

    old_photos = connection.execute(
        "SELECT photo_path FROM tour_photos WHERE tour_id = ? ORDER BY photo_order",
        (tour_id,)
    ).fetchall()

    if not has_new_photo and len(old_photos) >= 5:
        return True

    connection.execute("DELETE FROM tour_photos WHERE tour_id = ?", (tour_id,))

    photos = []

    index = 1

    for uploaded_file in uploaded_files:
        saved_path = save_uploaded_file(
            uploaded_file,
            "tour_" + str(tour_id) + "_photo_" + str(index),
            index
        )

        if saved_path != "":
            photos.append(saved_path)

        index = index + 1

    if has_new_photo and len(photos) < 5:
        return False

    if len(photos) == 0:
        for x in old_photos:
            photos.append(x["photo_path"])

    if len(photos) == 0 and old_main_image is not None and old_main_image != "":
        photos.append(old_main_image)

    if len(photos) == 0:
        photos.append(DEFAULT_TOUR_IMAGE)

    index = 1

    for photo_path in photos[:5]:
        connection.execute(
            """
            INSERT INTO tour_photos (tour_id, photo_path, photo_order)
            VALUES (?, ?, ?)
            """,
            (tour_id, photo_path, index)
        )

        index = index + 1

    connection.execute(
        "UPDATE tours SET image = ? WHERE id = ?",
        (photos[0], tour_id)
    )

    return True


def get_current_tour_photos(tour_id):
    connection = get_db_connection()

    photo_rows = connection.execute(
        """
        SELECT photo_path, photo_order
        FROM tour_photos
        WHERE tour_id = ?
        ORDER BY photo_order
        """,
        (tour_id,)
    ).fetchall()

    connection.close()

    current_photos = []

    for x in photo_rows:
        current_photos.append(dict(x))

    return current_photos
