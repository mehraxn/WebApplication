# Flask HTTP Methods 

## Introduction

In Flask, when defining routes using the `@app.route()` decorator, you can specify which HTTP methods are allowed for a given URL.

Example

```python
@app.route('hello', methods=['GET', 'POST'])
def hello()
    return Hello World
```

In this example, the `hello` route accepts both GET and POST requests.

---

## What is an HTTP Method

An HTTP method (also called a verb) indicates the type of action that the client wants to perform on a resource.

 The URL specifies where
 The HTTP method specifies what action

Example

 `GET users` → Retrieve users
 `POST users` → Create a new user

---

## Why Methods Matter in Flask

Flask uses HTTP methods to

 Control how routes behave
 Separate logic for reading vs modifying data
 Build RESTful APIs
 Improve application security by restricting allowed actions

If a request is made using a method not listed in `methods=[...]`, Flask returns

```
405 Method Not Allowed
```

---

## Default Behavior

If you do not specify `methods`, Flask defaults to

```python
methods=['GET']
```

---

## Common HTTP Methods in Flask

### 1. GET

Purpose Retrieve or read data from the server.

Characteristics

 Safe (does not modify data)
 Can be cached
 Used when opening a webpage

Example

```python
@app.route('home', methods=['GET'])
def home()
    return Welcome Home
```

---

### 2. POST

Purpose Send data to the server, usually to create a resource.

Characteristics

 Modifies server state
 Data is sent in the request body
 Commonly used with forms

Example

```python
@app.route('submit', methods=['POST'])
def submit()
    return Form submitted
```

---

### 3. PUT

Purpose Replace or update an existing resource completely.

Characteristics

 Idempotent (same request gives same result)
 Replaces full resource

Example

```python
@app.route('userintid', methods=['PUT'])
def update_user(id)
    return fUser {id} updated
```

---

### 4. PATCH

Purpose Partially update an existing resource.

Characteristics

 Only updates specific fields
 More efficient than PUT for partial updates

Example

```python
@app.route('userintid', methods=['PATCH'])
def patch_user(id)
    return fUser {id} partially updated
```

---

### 5. DELETE

Purpose Remove a resource from the server.

Characteristics

 Idempotent
 Used in REST APIs

Example

```python
@app.route('userintid', methods=['DELETE'])
def delete_user(id)
    return fUser {id} deleted
```

---

### 6. HEAD

Purpose Same as GET, but returns only headers (no body).

Use cases

 Check if a resource exists
 Inspect metadata

---

### 7. OPTIONS

Purpose Returns the list of supported methods for a route.

Use cases

 API discovery
 CORS preflight requests

---

## Using Multiple Methods in One Route

You can handle multiple methods in a single function using `request.method`.

```python
from flask import request

@app.route('login', methods=['GET', 'POST'])
def login()
    if request.method == 'GET'
        return Show login form
    elif request.method == 'POST'
        return Process login
```

---

## Best Practices

 Use GET for retrieving data
 Use POST for creating data
 Use PUTPATCH for updates
 Use DELETE for removal
 Always restrict methods explicitly for better security

---

## Interview-Ready Summary

In Flask, the `methods` argument in the `@app.route()` decorator specifies which HTTP request methods are allowed for a particular route. HTTP methods define the type of action performed on a resource, such as retrieving data (GET), sending data (POST), updating data (PUTPATCH), or deleting data (DELETE). If a request uses a method not allowed by the route, Flask returns a 405 error.

---

## Conclusion

Understanding HTTP methods is essential for building web applications and APIs in Flask. They allow you to design clean, organized, and secure routes that follow standard web communication principles.
