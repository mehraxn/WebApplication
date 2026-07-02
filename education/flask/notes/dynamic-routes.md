# README: Dynamic Routes in Flask

## 1. Introduction

In Flask, a **route** connects a URL to a Python function.

A normal route usually looks like this:

```python
@app.route('/about')
def about():
    return 'About page'
```

When the user visits:

```text
/about
```

Flask runs the `about()` function.

This type of route is fixed. The URL does not change.

A **dynamic route** is different. A dynamic route allows part of the URL to change.

For example:

```python
@app.route('/user/<name>')
def user(name):
    return f'Hello {name}'
```

Now the same route can handle many URLs:

```text
/user/Ali
/user/Sara
/user/John
```

The route is dynamic because the `name` part changes.

---

## 2. Static Route vs Dynamic Route

## Static Route

A static route is always the same.

```python
@app.route('/contact')
def contact():
    return 'Contact page'
```

This route only works for:

```text
/contact
```

It does not receive changing data from the URL.

Other examples of static routes:

```python
@app.route('/')
@app.route('/about')
@app.route('/login')
@app.route('/dashboard')
```

These routes are useful when the page has one fixed address.

---

## Dynamic Route

A dynamic route has a changing part inside the URL.

```python
@app.route('/hello/<name>')
def hello(name):
    return f'Hello {name}'
```

This route can work with:

```text
/hello/Ali
/hello/Sara
/hello/Maria
```

The value from the URL is passed into the function as a variable.

So if the user visits:

```text
/hello/Ali
```

Flask does this:

```python
name = 'Ali'
```

Then it runs the function.

---

## 3. Why Do We Need Dynamic Routes?

Dynamic routes are important because websites usually have many pages with the same structure but different data.

For example:

```text
/user/ali
/user/sara
/user/john
```

All of these pages are user profile pages.

The structure is the same, but the user data is different.

Without dynamic routes, we would need to write many separate routes:

```python
@app.route('/user/ali')
def ali():
    return 'Ali profile'

@app.route('/user/sara')
def sara():
    return 'Sara profile'

@app.route('/user/john')
def john():
    return 'John profile'
```

This is not a good way.

With a dynamic route, we can write only one route:

```python
@app.route('/user/<username>')
def profile(username):
    return f'{username} profile'
```

Now one route can handle many users.

This is the main purpose of dynamic routes.

---

## 4. Basic Syntax of a Dynamic Route

The basic syntax is:

```python
@app.route('/some-path/<variable_name>')
def function_name(variable_name):
    return 'some response'
```

The dynamic part is written inside angle brackets:

```python
<variable_name>
```

Example:

```python
@app.route('/city/<city_name>')
def city(city_name):
    return f'City: {city_name}'
```

Here:

```python
<city_name>
```

is the dynamic part of the route.

And:

```python
def city(city_name):
```

receives that dynamic value.

---

## 5. The Most Important Rule

The name inside the route must match the function parameter name.

Correct:

```python
@app.route('/user/<username>')
def profile(username):
    return username
```

Here, the route uses:

```python
<username>
```

And the function receives:

```python
username
```

So this is correct.

Wrong:

```python
@app.route('/user/<username>')
def profile(name):
    return name
```

This is wrong because the route gives Flask a variable called `username`, but the function expects a variable called `name`.

If you want to call it `name`, you must write it in both places:

```python
@app.route('/user/<name>')
def profile(name):
    return name
```

---

## 6. How Flask Reads a Dynamic Route

Imagine this route:

```python
@app.route('/hello/<name>')
def hello(name):
    return f'Hello {name}'
```

If the user visits:

```text
/hello/Ali
```

Flask does these steps:

1. Flask receives the request.
2. Flask checks the URL.
3. Flask sees that `/hello/Ali` matches `/hello/<name>`.
4. Flask takes `Ali` from the URL.
5. Flask stores it in the variable `name`.
6. Flask runs the function `hello(name)`.
7. The function returns the response.

So this URL:

```text
/hello/Ali
```

becomes this Python value:

```python
name = 'Ali'
```

---

## 7. Dynamic Route with Text

By default, Flask dynamic route values are strings.

Example:

```python
@app.route('/language/<lang>')
def language(lang):
    return f'You selected {lang}'
```

Valid URLs:

```text
/language/python
/language/javascript
/language/html
```

If the user visits:

```text
/language/python
```

Flask passes this value:

```python
lang = 'python'
```

The response will be:

```text
You selected python
```

---

## 8. Dynamic Route with Integer

Sometimes we want the dynamic value to be a number.

For this, we use the `int` converter.

Example:

```python
@app.route('/product/<int:product_id>')
def product(product_id):
    return f'Product ID: {product_id}'
```

The dynamic part is:

```python
<int:product_id>
```

This means Flask accepts only integer numbers in that part of the URL.

Valid URLs:

```text
/product/1
/product/25
/product/100
```

Invalid URLs:

```text
/product/book
/product/abc
/product/hello
```

Those invalid URLs do not match the route because they are not integers.

---

## 9. What is a Converter?

A converter tells Flask what type of value the dynamic part should accept.

Example:

```python
<int:id>
```

This means:

The dynamic value must be an integer.

Another example:

```python
<float:price>
```

This means:

The dynamic value must be a decimal number.

Another example:

```python
<username>
```

This means:

The dynamic value is a string.

When no converter is written, Flask uses string by default.

So these two routes are similar:

```python
@app.route('/user/<username>')
```

and:

```python
@app.route('/user/<string:username>')
```

---

## 10. Common Flask Route Converters

Flask gives us several useful converters.

## String Converter

```python
@app.route('/user/<string:username>')
def user(username):
    return username
```

This accepts text without slashes.

Example:

```text
/user/ali
```

Usually we do not need to write `string` because it is the default.

So this is also fine:

```python
@app.route('/user/<username>')
def user(username):
    return username
```

---

## Integer Converter

```python
@app.route('/item/<int:item_id>')
def item(item_id):
    return str(item_id)
```

This accepts whole numbers.

Example:

```text
/item/10
```

It does not accept text.

---

## Float Converter

```python
@app.route('/price/<float:amount>')
def price(amount):
    return str(amount)
```

This accepts decimal numbers.

Example:

```text
/price/19.99
```

---

## Path Converter

```python
@app.route('/files/<path:file_path>')
def files(file_path):
    return file_path
```

This accepts text with slashes.

Example:

```text
/files/images/profile/photo.png
```

Here Flask stores this value:

```python
file_path = 'images/profile/photo.png'
```

The `path` converter is useful when the dynamic part may contain `/` characters.

---

## 11. One Dynamic Value Example

```python
@app.route('/student/<name>')
def student(name):
    return f'Student name: {name}'
```

Example URL:

```text
/student/Ali
```

Flask reads it like this:

```python
name = 'Ali'
```

The result is:

```text
Student name: Ali
```

This is a simple dynamic route with one changing value.

---

## 12. Two Dynamic Values Example

A route can have more than one dynamic part.

Example:

```python
@app.route('/student/<name>/grade/<int:grade>')
def student_grade(name, grade):
    return f'{name} is in grade {grade}'
```

Example URL:

```text
/student/Ali/grade/5
```

Flask reads it like this:

```python
name = 'Ali'
grade = 5
```

The result is:

```text
Ali is in grade 5
```

Important rule:

Both dynamic values must be received by the function.

Because the route has:

```python
<name>
<int:grade>
```

The function must have:

```python
def student_grade(name, grade):
```

---

## 13. Dynamic Route with IDs

Many websites use IDs in URLs.

Example:

```text
/products/1
/products/2
/products/3
```

A route for this can be:

```python
@app.route('/products/<int:id>')
def product_detail(id):
    return f'Product detail page for product {id}'
```

If the user visits:

```text
/products/3
```

Flask passes:

```python
id = 3
```

The result is:

```text
Product detail page for product 3
```

This is common in real web applications.

---

## 14. Dynamic Route with Slugs

A **slug** is a readable text value in a URL.

Example:

```text
/blog/learning-flask-routes
/blog/how-html-works
/blog/css-flexbox-guide
```

A slug is usually used for blog posts, articles, products, or pages.

Example route:

```python
@app.route('/blog/<slug>')
def blog_post(slug):
    return f'Blog post slug: {slug}'
```

If the user visits:

```text
/blog/learning-flask-routes
```

Flask passes:

```python
slug = 'learning-flask-routes'
```

Slugs are useful because they make URLs easier to read.

This URL is readable:

```text
/blog/learning-flask-routes
```

This URL is less readable:

```text
/blog/15
```

Both ways can be used, but they have different purposes.

---

## 15. Dynamic Route and HTML Templates

Dynamic routes are often used with HTML templates.

A Flask route can receive a dynamic value, find some data, and send that data to an HTML file.

Example:

```python
@app.route('/profile/<username>')
def profile(username):
    return render_template('profile.html', username=username)
```

This route receives a username from the URL.

Then it sends the username to `profile.html`.

Inside `profile.html`, we can use:

```html
<h1>{{ username }}</h1>
```

If the user visits:

```text
/profile/Ali
```

The page shows:

```text
Ali
```

So the URL changes the content shown on the page.

---

## 16. Dynamic Route and `render_template()`

`render_template()` is used to show an HTML file.

Example:

```python
return render_template('profile.html', username=username)
```

This means:

Open the file:

```text
profile.html
```

and send this variable to it:

```python
username=username
```

The left side is the variable name in the HTML file.

```python
username=
```

The right side is the Python variable.

```python
username
```

So the HTML file can use:

```html
{{ username }}
```

Dynamic routes become more useful when combined with templates.

---

## 17. Dynamic Route and `url_for()`

When creating links to dynamic routes, we should use `url_for()`.

Example route:

```python
@app.route('/profile/<username>')
def profile(username):
    return render_template('profile.html', username=username)
```

Correct link:

```html
<a href="{{ url_for('profile', username='Ali') }}">Ali Profile</a>
```

This creates:

```text
/profile/Ali
```

Important rule:

`url_for()` uses the function name, not the URL itself.

The function name is:

```python
profile
```

So we write:

```python
url_for('profile', username='Ali')
```

We do not write:

```python
url_for('/profile/<username>')
```

That is wrong.

---

## 18. Why Use `url_for()` Instead of Writing URLs Manually?

You could write a link manually like this:

```html
<a href="/profile/Ali">Ali Profile</a>
```

But using `url_for()` is better:

```html
<a href="{{ url_for('profile', username='Ali') }}">Ali Profile</a>
```

Why?

Because Flask builds the correct URL for you.

If you later change the route from:

```python
@app.route('/profile/<username>')
```

to:

```python
@app.route('/users/<username>')
```

then `url_for()` can still build the correct link based on the function name.

This makes your project easier to maintain.

---

## 19. Dynamic Links Inside a Loop

Dynamic routes are often used with loops in Jinja.

Example:

```python
users = ['Ali', 'Sara', 'John']
```

Route:

```python
@app.route('/users')
def users_page():
    return render_template('users.html', users=users)

@app.route('/profile/<username>')
def profile(username):
    return render_template('profile.html', username=username)
```

Template:

```html
{% for user in users %}
    <a href="{{ url_for('profile', username=user) }}">{{ user }}</a>
{% endfor %}
```

This creates links like:

```text
/profile/Ali
/profile/Sara
/profile/John
```

The links are dynamic because each link uses a different username.

---

## 20. Dynamic Route with Data Lookup

A dynamic route usually receives a value and uses it to find data.

Example:

```python
products = {
    1: 'Laptop',
    2: 'Phone',
    3: 'Keyboard'
}

@app.route('/products/<int:id>')
def product(id):
    product_name = products.get(id)
    return product_name
```

If the user visits:

```text
/products/2
```

Flask gets:

```python
id = 2
```

Then this line runs:

```python
product_name = products.get(id)
```

The result is:

```python
product_name = 'Phone'
```

So the page shows:

```text
Phone
```

This is the common idea:

The URL gives an ID, and the app uses that ID to find data.

---

## 21. Handling Missing Data

Sometimes the user may visit a dynamic URL that does not exist.

Example:

```text
/products/100
```

But maybe there is no product with ID `100`.

If the app does not handle this case, it may crash or show an incorrect page.

A better solution is to return a 404 error.

Example:

```python
from flask import abort

products = {
    1: 'Laptop',
    2: 'Phone',
    3: 'Keyboard'
}

@app.route('/products/<int:id>')
def product(id):
    product_name = products.get(id)

    if product_name is None:
        abort(404)

    return product_name
```

`abort(404)` means:

Stop the request and show a page not found error.

This is safer and more professional.

---

## 22. What is 404?

404 means:

```text
Page Not Found
```

A 404 response is used when the requested page or data does not exist.

For example:

```text
/products/999
```

If product `999` does not exist, the app should show 404.

This tells the user and the browser that the requested resource was not found.

---

## 23. Dynamic Routes Are Not the Same as Dynamic Websites

This is an important point.

A dynamic route means the URL can contain changing values.

Example:

```python
@app.route('/user/<username>')
```

A dynamic website means the page content can change depending on data, user input, database information, login state, or other logic.

A Flask app can have dynamic routes but still use simple static data inside Python.

Example:

```python
users = ['Ali', 'Sara', 'John']
```

This is simple data written inside the code.

A larger app may use a database instead.

So we can say:

Dynamic route = changing URL part.

Dynamic website = changing page content based on data or logic.

They are related, but they are not exactly the same thing.

---

## 24. Dynamic Route with Query String Compared

Sometimes beginners confuse dynamic routes with query strings.

A dynamic route looks like this:

```text
/products/5
```

A query string looks like this:

```text
/products?id=5
```

Both can send information to Flask, but they are written differently.

Dynamic route example:

```python
@app.route('/products/<int:id>')
def product(id):
    return str(id)
```

URL:

```text
/products/5
```

Query string example:

```python
from flask import request

@app.route('/products')
def product():
    id = request.args.get('id')
    return id
```

URL:

```text
/products?id=5
```

Dynamic routes are usually used for main resources.

Query strings are usually used for filters, searches, sorting, and optional values.

Examples of query strings:

```text
/products?category=phones
/search?q=flask
/users?page=2
```

---

## 25. When Should We Use Dynamic Routes?

Use dynamic routes when the value is an important part of the page identity.

Good examples:

```text
/users/ali
/products/10
/posts/learning-flask
/categories/python
```

These URLs identify a specific resource.

Use query strings when the value is more like an option or filter.

Good examples:

```text
/products?sort=price
/products?category=laptops
/search?q=flask
/blog?page=2
```

The simple rule is:

Use dynamic routes for pages.

Use query strings for options.

---

## 26. Multiple Dynamic Routes in One App

A Flask app can have many dynamic routes.

Example:

```python
@app.route('/users/<username>')
def user_profile(username):
    return f'User: {username}'

@app.route('/products/<int:product_id>')
def product_detail(product_id):
    return f'Product: {product_id}'

@app.route('/categories/<category_name>')
def category(category_name):
    return f'Category: {category_name}'
```

Each route handles a different type of page.

The dynamic variables are:

```python
username
product_id
category_name
```

Each variable comes from the URL.

---

## 27. Dynamic Route with a Database Idea

In real applications, dynamic routes usually work with a database.

Example idea:

```python
@app.route('/users/<int:user_id>')
def user_profile(user_id):
    user = database.get_user(user_id)
    return render_template('profile.html', user=user)
```

This is just a simple idea.

The route receives:

```python
user_id
```

Then the app uses that ID to find the user in the database.

Then Flask sends the user data to an HTML template.

The logic is:

```text
URL value -> Python variable -> find data -> show template
```

This is one of the most common patterns in Flask.

---

## 28. Common Mistake: Variable Name Does Not Match

Wrong:

```python
@app.route('/book/<int:id>')
def book(book_id):
    return str(book_id)
```

The route gives Flask a variable called:

```python
id
```

But the function expects:

```python
book_id
```

This causes an error.

Correct:

```python
@app.route('/book/<int:book_id>')
def book(book_id):
    return str(book_id)
```

Now both names match.

---

## 29. Common Mistake: Forgetting the Converter

This route accepts text by default:

```python
@app.route('/product/<id>')
def product(id):
    return id
```

Here, `id` is a string.

So if you want to use it as a number, you may need to convert it manually.

Better:

```python
@app.route('/product/<int:id>')
def product(id):
    return str(id)
```

Now Flask automatically converts it to an integer.

So this is better for numeric IDs.

---

## 30. Common Mistake: Writing `url_for()` Incorrectly

Wrong:

```html
<a href="{{ url_for('/profile/<username>', username='Ali') }}">Profile</a>
```

This is wrong because `url_for()` does not use the route URL.

Correct:

```html
<a href="{{ url_for('profile', username='Ali') }}">Profile</a>
```

Because the function name is:

```python
def profile(username):
```

So we use:

```python
profile
```

inside `url_for()`.

---

## 31. Common Mistake: Missing Required Dynamic Value in `url_for()`

Route:

```python
@app.route('/profile/<username>')
def profile(username):
    return username
```

Wrong link:

```html
<a href="{{ url_for('profile') }}">Profile</a>
```

This is wrong because the route needs a `username` value.

Correct link:

```html
<a href="{{ url_for('profile', username='Ali') }}">Profile</a>
```

Now Flask can build the URL:

```text
/profile/Ali
```

---

## 32. Common Mistake: Using Spaces in URLs

A URL should not normally contain spaces.

Bad example:

```text
/blog/my first post
```

Better example:

```text
/blog/my-first-post
```

That is why slugs often use hyphens.

Example:

```text
/blog/learning-flask-routes
```

This is cleaner and easier to use.

---

## 33. Dynamic Route Naming Style

Use clear variable names.

Good:

```python
@app.route('/products/<int:product_id>')
def product_detail(product_id):
    return str(product_id)
```

Less clear:

```python
@app.route('/products/<int:x>')
def product_detail(x):
    return str(x)
```

The first version is better because `product_id` explains what the value means.

---

## 34. Dynamic Route Full Beginner Example

Here is a small standalone app showing different dynamic routes.

```python
from flask import Flask, render_template, abort

app = Flask(__name__)

@app.route('/')
def home():
    return 'Home page'

@app.route('/hello/<name>')
def hello(name):
    return f'Hello {name}'

@app.route('/products/<int:product_id>')
def product(product_id):
    return f'Product ID: {product_id}'

@app.route('/price/<float:amount>')
def price(amount):
    return f'Price: {amount}'

@app.route('/files/<path:file_path>')
def files(file_path):
    return f'File path: {file_path}'

if __name__ == '__main__':
    app.run(debug=True)
```

This app has:

A static route:

```python
@app.route('/')
```

A dynamic string route:

```python
@app.route('/hello/<name>')
```

A dynamic integer route:

```python
@app.route('/products/<int:product_id>')
```

A dynamic float route:

```python
@app.route('/price/<float:amount>')
```

A dynamic path route:

```python
@app.route('/files/<path:file_path>')
```

---

## 35. How to Make a Dynamic Route Step by Step

## Step 1: Choose the fixed part of the URL

Example:

```text
/users/
```

## Step 2: Choose the changing part

Example:

```text
username
```

## Step 3: Put the changing part inside angle brackets

```python
<username>
```

## Step 4: Put it in the route

```python
@app.route('/users/<username>')
```

## Step 5: Add the same name to the function parameter

```python
def user_profile(username):
```

## Step 6: Use the value inside the function

```python
return f'User: {username}'
```

Complete route:

```python
@app.route('/users/<username>')
def user_profile(username):
    return f'User: {username}'
```

Now this route works with:

```text
/users/Ali
/users/Sara
/users/John
```

---

## 36. Step-by-Step Example with Integer

## Step 1: Choose the fixed part

```text
/products/
```

## Step 2: Choose the dynamic value name

```text
product_id
```

## Step 3: Choose the type

Because product IDs are numbers, use:

```python
int
```

## Step 4: Create the route

```python
@app.route('/products/<int:product_id>')
```

## Step 5: Receive it in the function

```python
def product_detail(product_id):
```

## Step 6: Use it

```python
return f'Product ID: {product_id}'
```

Complete route:

```python
@app.route('/products/<int:product_id>')
def product_detail(product_id):
    return f'Product ID: {product_id}'
```

Now this URL:

```text
/products/7
```

creates this Python value:

```python
product_id = 7
```

---

## 37. How Dynamic Routes Connect to Templates

A common pattern is:

```python
@app.route('/users/<username>')
def user_profile(username):
    return render_template('profile.html', username=username)
```

Then in `profile.html`:

```html
<h1>{{ username }}</h1>
```

If the user visits:

```text
/users/Ali
```

Flask sends:

```python
username = 'Ali'
```

to the template.

Then the page shows:

```text
Ali
```

This means one HTML template can show different content depending on the URL.

---

## 38. The Main Pattern of Dynamic Routes

Most dynamic routes follow this pattern:

```text
Receive value from URL
Use value inside Python function
Find or prepare data
Send response or render template
```

Example:

```python
@app.route('/something/<value>')
def page(value):
    return render_template('page.html', value=value)
```

The route receives:

```python
value
```

Then it sends it to the HTML file.

---

## 39. Simple Mental Model

Think of a dynamic route like a blank space in the URL.

Example:

```python
@app.route('/hello/<name>')
```

The route is like this:

```text
/hello/____
```

Whatever the user writes in the blank space becomes the value of `name`.

So:

```text
/hello/Ali
```

means:

```python
name = 'Ali'
```

And:

```text
/hello/Sara
```

means:

```python
name = 'Sara'
```

Same route, different value.

---

## 40. Final Summary

A dynamic route lets part of the URL become a Python variable.

The dynamic part is written inside angle brackets:

```python
<name>
```

or with a converter:

```python
<int:id>
```

The function must receive the same variable name:

```python
@app.route('/user/<username>')
def user(username):
    return username
```

Dynamic routes help us avoid writing many repeated routes.

Instead of writing separate routes for many users, products, posts, or pages, we write one flexible route.

The most important idea is:

```text
Part of the URL becomes a Python variable.
```

That is the core meaning of a dynamic route in Flask.
