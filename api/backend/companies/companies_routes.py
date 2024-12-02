########################################################
# companies blueprint of endpoints
#######################################################
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from backend.ml_models.model01 import predict

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
companies = Blueprint('companies', __name__)


#------------------------------------------------------------
# Get all companies from the system
@companies.route('/companies', methods=['GET'])
def get_companies(): 
    query = 'SELECT * FROM company'
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Add a new company to the system
@companies.route('/companies', methods=['POST'])
def add_company(): 
    the_data = request.json
    current_app.logger.info(the_data)

    name = the_data['name']
    size = the_data['size']
    
    query = f'''
        INSERT INTO company (name, size)
        VALUES ('{name}', '{size}')
    '''
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully added company")
    response.status_code = 200
    return response

#------------------------------------------------------------
# Get company detail for company with particular companyID
@companies.route('/companies/<companyID>', methods=['GET'])
def get_company(companyID):
    query = f'''
        SELECT * FROM company WHERE companyID = {companyID}
    '''
    current_app.logger.info(f'GET /companies/{companyID} query={query}')
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    current_app.logger.info(f'GET /companies/{companyID} Result of the query={theData}')

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response


#------------------------------------------------------------
# Update company info for company with particular companyID
@companies.route('/companies/<companyID>', methods=['PUT'])
def update_company(companyID): 
    current_app.logger.info('PUT /companies/<companyID> route')
    company_info = request.json
    name = company_info['name']
    size = company_info['size']

    query = 'UPDATE company SET name = %s, size = %s where companyID = %s'
    data = (name, size, companyID)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'company updated!'


#------------------------------------------------------------
# Return all reviews associated with a particular company
@companies.route('/companies/<companyID>/reviews', methods=['GET'])
def get_company_reviews(companyID):
    current_app.logger.info('GET /companies/<companyID>/reviews route')
    query = f'''
        SELECT * FROM reviews WHERE companyID = {companyID}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    current_app.logger.info(f'GET /companies/{companyID}/reviews Result of the query={theData}')

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

#------------------------------------------------------------
# Return all questions from all reviews associated with a particular company
@companies.route('/companies/<companyID>/reviews/questions', methods=['GET'])
def get_company_reviews_questions(companyID):
    current_app.logger.info('GET /companies/<companyID>/reviews/questions route')
    query = f'''
        SELECT q.text, q.author, q.postId, q.questionId
        FROM company c 
            JOIN reviews r ON c.companyID = r.companyID
            JOIN questions q ON r.reviewID = q.postId
        WHERE c.companyID = {companyID}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    current_app.logger.info(f'GET /companies/{companyID}/reviews/questions Result of the query={theData}')

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

#------------------------------------------------------------
# Return all answers from all reviews associated with a particular company
@companies.route('/companies/<companyID>/reviews/answers', methods=['GET'])
def get_company_reviews_answers(companyID):
    current_app.logger.info('GET /companies/<companyID>/reviews/answers route')
    query = f'''
        SELECT a.text, a.author, a.postId, a.answerId
        FROM company c 
            JOIN reviews r ON c.companyID = r.companyID
            JOIN answers a ON r.reviewID = a.postId
        WHERE c.companyID = {companyID}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    current_app.logger.info(f'GET /companies/{companyID}/reviews/answers Result of the query={theData}')

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

#------------------------------------------------------------
# Return all questions associate with a particular position at a company
@companies.route('/companies/<companyID>/positions/<positionID>/reviews/questions', methods=['GET'])
def get_company_positions_reviews_questions(companyID, positionID):
    current_app.logger.info('GET /companies/<companyID>/positions/<positionID>/reviews/questions route')
    query = f'''
        SELECT q.text, q.author, q.postId, q.questionId, p.positionID
        FROM company c 
            JOIN position p ON c.companyID = p.companyID
            JOIN reviews r ON c.companyID = r.companyID
            JOIN questions q ON r.reviewID = q.postId
        WHERE c.companyID = {companyID} AND p.positionID = {positionID}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    current_app.logger.info(f'GET /companies/{companyID}/positions/{positionID}/reviews/questions Result of the query={theData}')

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

#------------------------------------------------------------
# Return all answers associate with a particular position at a company
@companies.route('/companies/<companyID>/positions/<positionID>/reviews/answers', methods=['GET'])
def get_company_positions_reviews_answers(companyID, positionID):
    current_app.logger.info('GET /companies/<companyID>/positions/<positionID>/reviews/answers route')
    query = f'''
        SELECT a.text, a.author, a.postId, a.answerId, p.positionID
        FROM company c 
            JOIN position p ON c.companyID = p.companyID
            JOIN reviews r ON c.companyID = r.companyID
            JOIN answers a ON r.reviewID = a.postId
        WHERE c.companyID = {companyID} AND p.positionID = {positionID}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    
    current_app.logger.info(f'GET /companies/{companyID}/positions/{positionID}/reviews/answers Result of the query={theData}')

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response
