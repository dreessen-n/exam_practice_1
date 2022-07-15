# Import mysqlconnection config
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
from flask_app.models import user

"""
Change class construct, queries, and db for review
"""

class Review:
    # Use a alias for the database; call in classmethods as cls.db
    # For staticmethod need to call the database name not alias
    db = "exam_practice_1"

    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.rating = data['rating']
        self.date_watched = data['date_watched']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        # Needed to create this to capture the creator of the review
        self.creator = None
        self.user_ids_who_favorited = []
        self.users_who_favorited = []

    # CRUD CREATE METHODS
    @classmethod
    def create_review(cls,data):
        """Create a review"""
        query = "INSERT INTO reviews (title, rating, date_watched, content, user_id) VALUES (%(title)s, %(rating)s, %(date_watched)s, %(content)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    # CRUD READ METHODS -- Modified for many to many
    @classmethod
    def get_all_reviews(cls):
        """Get all the reviews in db"""
        query = '''SELECT * FROM reviews
                JOIN users AS creators ON reviews.user_id = creators.id
                LEFT JOIN favorited_reviews ON favorited_reviews.review_id = reviews.id
                LEFT JOIN users AS users_who_favorited ON favorited_reviews.user_id = users_who_favorited.id;'''
        # query = "SELECT * FROM reviews LEFT JOIN users ON reviews.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        all_reviews = []
        for r in results:
            new_review = True
            users_who_favorited_data = {
                'id': r['users_who_favorited.id'],
                'first_name': r['users_who_favorited.first_name'],
                'last_name': r['users_who_favorited.last_name'],
                'email': r['users_who_favorited.email'],
                'password': r['users_who_favorited.password'],
                'created_at': r['users_who_favorited.created_at'],
                'updated_at': r['users_who_favorited.updated_at']
            }
            # Check to see if previous processed review, exist as current row
            num_of_review = len(all_reviews)
            # Check to see if we have reviews in list
            if num_of_review > 0:
                # Check if last review equals current row
                last_review = all_reviews[num_of_review-1]
                if last_review.id == r['id']:
                    last_review.user_ids_who_favorited.append(r['users_who_favorited.id'])
                    last_review.users_who_favorited.append(user.User(users_who_favorited_data))
                    new_review = False
            # Create new review object if review has not been created
            # and added to the list
            if new_review:
                # Create the review object
                review = cls(r)
                # Create the associated User object; include all contructors
                user_data = {
                    'id': r['creators.id'],
                    'first_name': r['first_name'],
                    'last_name': r['last_name'],
                    'email': r['email'],
                    'password': r['password'],
                    'created_at': r['creators.created_at'],
                    'updated_at': r['creators.updated_at']
                }
                one_user = user.User(user_data)
                # Set user to creator in review
                review.creator = one_user
                # Check to see if any user liked this review
                if r['users_who_favorited.id']:
                    review.user_ids_who_favorited.append(r['users_who_favorited.id'])
                    review.users_who_favorited.append(user.User(users_who_favorited_data))
                # Append the review to the all_review list
                all_reviews.append(review)

        return all_reviews

    @classmethod
    def get_one_review(cls,data):
        """Get one review to display"""
        query = "SELECT * FROM reviews LEFT JOIN users ON reviews.user_id = users.id WHERE reviews.id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        review = cls(result[0])
        user_data = {
            'id': result[0]['users.id'],
            'first_name': result[0]['first_name'],
            'last_name': result[0]['last_name'],
            'email': result[0]['email'],
            'password': result[0]['password'],
            'created_at': result[0]['users.created_at'],
            'updated_at': result[0]['users.updated_at']
        }
        one_user = user.User(user_data)
        # Set user to creator in review
        review.creator = one_user
        return review

    # CRUD UPDATE METHODS
    @classmethod
    def update_review(cls,data):
        """Update the review"""
        query = "UPDATE reviews SET title=%(title)s, rating=%(rating)s, date_watched=%(date_watched)s, content=%(content)s, WHERE reviews.id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    # CRUD DELETE METHODS
    @classmethod
    def delete_review(cls,data):
        """Delete review"""
        query = "DELETE FROM reviews WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    # FORM VALIDATION
    @staticmethod
    def validate_form(review):
        """Validate the new review create form"""
        is_valid = True # We set True until False
        if len(review['title']) < 2:
            flash("The Title must be at least 2 characters.", "danger")
            is_valid = False
        if len(review['rating']) < 1:
            flash("The rating must be a number between 1 and 5; with 5 being the highest rating.", "danger")
            is_valid = False
        if review['date_watched'] == '':
            flash("Please enter a date.", "danger")
            is_valid = False
        if len(review['content']) < 3:
            flash("The content can not be blank.", "danger")
            is_valid = False
        return is_valid


