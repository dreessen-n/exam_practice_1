# Import app
from flask_app import app
# Import modules from flask
from flask_app import Flask, render_template, request, redirect, session, url_for, flash, bcrypt

# Import models class
from flask_app.models import user, review

# CRUD CREATE ROUTES
@app.route('/review/create', methods=['POST'])
def create_new_review():
    # Check that user is logged in
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    # Call staticmethod to validate form
    if not review.Review.validate_form(request.form):
        # Redirect back to new review page
        return redirect('/review/new')
    # Create data dict based on request form
    # the keys must match exactly to the var in the query set
    data = {
        'title': request.form['title'],
        'rating': int(request.form['rating']),
        'date_watched': request.form['date_watched'],
        'content': request.form['content'],
        'user_id': session['id']
    }
    review.Review.create_review(data)
    return redirect('/dashboard')

@app.route('/review/favorite', methods=['POST'])
def add_favorite_review():
    review.Review.favorite(request.form)
    return redirect('/dashboard')

@app.route('/review/new')
def review_new():
    """Display the form to create a new review"""
    # Check that user is logged in
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    # Create data dict based on user in session
    # the keys must match exactly to the var in the query set
    data = { 'id': session['id'] }
    # Call classmethod in models
    return render_template('new.html', user=user.User.get_user_by_id(data))

# CRUD READ ROUTES
@app.route('/review/show/<int:review_id>')
def review_show_one(review_id):
    """Show the review on a page"""
    # Check that user is logged in
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    # Create data dict based on review_id
    # The keys must match exactly to the var in the query set
    data = { 'id': review_id }
    # Create additonal data dict for user
    data_user = { 'id': session['id'] }
    # Call classmethods and render_template edit template with data filled in
    return render_template('show.html', one_review=review.Review.get_one_review(data), user=user.User.get_user_by_id(data_user))


# CRUD UPDATE ROUTES
@app.route('/review/edit/<int:review_id>')
def edit_review(review_id):
    """Edit the review"""
    # Check that user is logged in
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    # Create data dict based on review_id
    # The keys must match exactly to the var in the query set
    data = { 'id': review_id }
    # Create additonal data dict for user
    data_user = { 'id': session['id'] }
    # Call classmethods and render_template edit template with data filled in
    return render_template('edit.html', one_review=review.Review.get_one_review(data), user=user.User.get_user_by_id(data_user)) 

@app.route('/review/update', methods=['POST'])
def update_review():
    """Update review after editing"""
    # Check that user is logged in
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    # Call staticmethod to validate form
    if not review.Review.validate_form(request.form):
        # Redirect back to new review page
        id = int(request.form['id'])
        return redirect(f'/review/edit/{id}')
    # Create data dict based on review_id
    # The keys must match exactly to the var in the query set
    data = {
        'id': int(request.form['id']),
        'title': request.form['title'],
        'rating': int(request.form['rating']),
        'date_watched': request.form['date_watched'],
        'content': request.form['content'],
    }
    # Call classmethod in models
    review.Review.update_review(data)
    # Redirect to dashboard after update
    return redirect('/dashboard')

# CRUD DELETE ROUTES
@app.route('/review/delete/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    """Delete review if session user created"""
    # Check that user is logged in
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    # Create data dict based on review_id
    # The keys must match exactly to the var in the query set
    data = { 'id': review_id }
    # Call classmethod in models
    review.Review.delete_review(data)
    # Redirect back to dashboard after deletion
    return redirect('/dashboard')

@app.route('/review/unfavorite', methods=['POST'])
def un_favorite_review():
    review.Review.unfavorite(request.form)
    return redirect('/dashboard')

