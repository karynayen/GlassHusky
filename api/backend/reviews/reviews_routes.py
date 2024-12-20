#################################################
# reviews blueprint of endpoints
#################################################
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

#-------------------------------------------------
# Create a new blueprint object which is a collection
# of routes.
reviews = Blueprint('reviews', __name__)

#-------------------------------------------------
# Get all reviews from the system
@reviews.route('/reviews', methods=['GET'])
def get_reviews():
    authorID = request.args.get('authorID')
    query = '''
        SELECT reviewID,
               positionID,
               companyID,
               authorID,
               title,
               rating,
               recommend,
               pay_type,
               pay,
               job_type,
               date_time,
               verified,
               text
        FROM reviews
    '''
    if authorID:
        query += ' WHERE authorID = %s'
        cursor = db.get_db().cursor()
        cursor.execute(query, (authorID,))
    else:
        cursor = db.get_db().cursor()
        cursor.execute(query)
    
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

#-------------------------------------------------
# Get all reviews associated with a company
@reviews.route('/reviews/<int:companyID>', methods=['GET'])
def get_reviews_company(companyID):
    query = '''
        SELECT reviewID,
               positionID,
               companyID,
               authorID,
               title,
               rating,
               recommend,
               pay_type,
               pay,
               job_type,
               date_time,
               verified,
               text,
               r.name
        FROM reviews
            NATURAL JOIN reviewer r
        WHERE companyID = %s
    '''

    cursor = db.get_db().cursor()

    cursor.execute(query, companyID)

    theData = cursor.fetchall()

    response = make_response(jsonify(theData))

    response.status_code = 200

    return response
#---------------------------------------------------
# Add a new review to the system
@reviews.route('/reviews', methods=['POST'])
def add_new_review():

    the_data = request.json
    current_app.logger.info(the_data)

    positionID = the_data['positionID']
    companyID = the_data['companyID']
    authorID = the_data['authorID']
    title = the_data['title']
    rating = the_data['rating']
    recommend = the_data['recommend']
    pay_type = the_data['pay_type']
    pay = the_data['pay']
    job_type = the_data['job_type']
    verified = the_data['verified']
    text = the_data['text']

    query = f'''
        INSERT INTO reviews (positionID,
                             companyID,
                             authorID,
                             title,
                             rating,
                             recommend,
                             pay_type,
                             pay,
                             job_type,
                             verified,
                             text)
        VALUES ('{str(positionID)}', '{str(companyID)}', '{str(authorID)}',
                '{title}', '{str(rating)}', '{recommend}',
                '{pay_type}', '{str(pay)}', '{job_type}',
                '{verified}', '{text}')
    '''
    
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully added review")
    response.status_code = 200
    return response

#-----------------------------------------------------------------
# Update a review in the system
@reviews.route('/reviews', methods=['PUT'])
def update_review():
    current_app.logger.info('PUT /reviews route')
    rev_info = request.json
    rev_id = rev_info['reviewID']
    rating = rev_info['rating']
    verified = rev_info['verified']
    text = rev_info['text']

    query = 'UPDATE reviews SET rating = %s, verified = %s, text = %s where reviewID = %s'
    data = (rating, verified, text, rev_id)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'review updated!'

#-------------------------------------------------------------------
@reviews.route('/reviews/<reviewID>', methods=['DELETE'])
def delete_review(reviewID):
    current_app.logger.info(f'DELETE /reviews/{reviewID} route')
    query = 'DELETE FROM reviews WHERE reviewID = %s'
    cursor = db.get_db().cursor()
    cursor.execute(query, (reviewID,))
    db.get_db().commit()
    return jsonify({'message': 'Review deleted successfully'}), 200

#--------------------------------------------------------------------
# Get a specific review based on reviewID from the system
@reviews.route('/reviews/<reviewID>', methods=['GET'])
def get_review(reviewID):
    query = f'''
        SELECT * FROM reviews WHERE reviewID = {reviewID}
    '''

    current_app.logger.info(f'GET /reviews/{reviewID} query={query}')
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    current_app.logger.info(f'GET /reviews/{reviewID} Result of the query={theData}')

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

#--------------------------------------------------------------------
# Update a specific review based on reviewID from the system
@reviews.route('/reviews/<reviewID>', methods=['PUT'])
def update_specific_review(reviewID):
    current_app.logger.info('PUT /reviews/<reviewID> route')
    rev_info = request.json
    title = rev_info['title']
    rating = rev_info['rating']
    recommend = rev_info['recommend']
    pay_type = rev_info['pay_type']
    pay = rev_info['pay']
    job_type = rev_info['job_type']
    text = rev_info['text']
    verified = rev_info['verified']

    query = '''
        UPDATE reviews
        SET title = %s, rating = %s, recommend = %s, pay_type = %s, pay = %s, job_type = %s, text = %s, verified = %s
        WHERE reviewID = %s
    '''
    data = (title, rating, recommend, pay_type, pay, job_type, text, verified, reviewID)
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    response = make_response(jsonify({"message": "Review updated successfully"}))
    response.status_code = 200
    return response

#----------------------------------------------------------------------

# Get all questions associated with a specific review
@reviews.route('/reviews/<reviewID>/questions', methods=['GET'])
def get_review_questions(reviewID):
    current_app.logger.info('GET /reviews/<reviewID>/questions route')
    query = f'''
        SELECT * FROM questions WHERE postID = {reviewID}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    current_app.logger.info(f'GET /reviews/{reviewID}/questions Result of the query={theData}')

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

#----------------------------------------------------------------------

# Add a new question to a specific review
@reviews.route('/reviews/<reviewID>/questions', methods=['POST'])
def add_review_question(reviewID):
    the_data = request.json
    current_app.logger.info(the_data)

    postId = reviewID
    author = the_data['author']
    text = the_data['text']

    query = f'''
        INSERT INTO questions (postId,
                               author,
                               text)
        VALUES ('{postId}', '{author}', '{text}')
    '''

    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response('Successfully added question')
    response.status_code = 200
    return response

#-----------------------------------------------------------------
# Get all answers associated with a specific review
@reviews.route('/reviews/<reviewID>/answers', methods=['GET'])
def get_review_answers(reviewID):
    current_app.logger.info('GET /reviews/<reviewID>/answers route')
    query = f'''
        SELECT * FROM answers WHERE postID = {reviewID}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    current_app.logger.info(f'GET /reviews/{reviewID}/answers Result of the query={theData}')

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

#-------------------------------------------------------------------

# Add a new answer to a specific review
@reviews.route('/reviews/<reviewID>/answers', methods=['POST'])
def add_review_answer(reviewID):
    the_data = request.json
    current_app.logger.info(the_data)

    postId = reviewID
    questionId = the_data['questionId']
    author = the_data['author']
    text = the_data['text']

    query = f'''
        INSERT INTO questions (postId,
                               questionId,
                               author,
                               text)
        VALUES ('{postId}', '{questionId}', '{author}', '{text}')
    '''

    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response('Successfully added answer')
    response.status_code = 200
    return response

#----------------------------------------------------------------------

# Get all reviews by a given authorID
@reviews.route('/reviews/<authorID>', methods=['GET'])
def get_reviews_by_author(authorID):
    query = f'''
        SELECT * FROM reviews WHERE authorID = {authorID}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (authorID,))
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

#----------------------------------------------------------------------
