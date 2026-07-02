# Flask Project Task Description Personal Blog Web Application

Build a complete Flask web application called Personal Blog.

## Project Goal

Create a blog website where users can view blog posts and manage them through the website.

## Main Requirements

### 1. Home Page

Create a home page that displays all blog posts.

Each post should show

 title
 short description or preview
 date of creation

Each post should also include a Read More link or button that opens the full post.

### 2. Single Post Page

Create a separate page for each blog post.

When the user clicks a post, the page should display

 full title
 full content
 date
 optional author name

### 3. Create Post Page

Create a page with a form that allows the user to add a new blog post.

The form should include

 title
 content
 author name

After submission, the new post should appear on the home page.

### 4. Edit Post Page

Allow the user to edit an existing post.

The edit form should already contain the old values.
After updating, the new values should be saved and shown on the website.

### 5. Delete Post Feature

Allow the user to delete an existing post.

After deletion, the post should no longer appear on the home page.

### 6. About Page

Create an About page that explains

 what the website is
 who created it

### 7. Navigation Bar

Add a navigation bar so the user can move between pages.

The navigation bar should include links to

 Home
 Create Post
 About

### 8. Styling

Use CSS to make the website clean, readable, and organized.

Style at least the following

 navigation bar
 forms
 buttons
 post cards
 single post page

### 9. Flask Requirements

The project must use

 Flask routes
 `render_template()`
 Jinja templating
 HTML templates
 static CSS file
 GET and POST methods

### 10. Data Handling

Use one of the following

 a Python listdictionary for beginner level, or
 SQLite database for a more complete project

### 11. Suggested Project Structure

Organize the project clearly.

Example structure

 `app.py`
 `templates`
 `static`

## Expected Learning Outcomes

By completing this project, you should understand

 how Flask routing works
 how templates work
 how to pass Python data into HTML
 how forms send data to Flask
 how CRUD works in Flask

## Optional Advanced Features

To make the project more complete, you may also add

 flash messages
 search for posts
 categories
 login system
 comments section
