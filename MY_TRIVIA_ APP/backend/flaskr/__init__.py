import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
def paginate_questions(request, selection):
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
       
        questions = [question.format() for question in selection]
        current_questions = questions[start:end]
        return current_questions

CATEGORY_PER_PAGE = 10
def paginate_category(request, selection):
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * CATEGORY_PER_PAGE
        end = start + CATEGORY_PER_PAGE
       
        questions = [question.format() for question in selection]
        current_questions = questions[start:end]
        return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """ 
    CORS(app, resources=r'/api/*')    
    #CORS(app, resources={r"*/api/*" : {origins: '*'}})
    

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Headers", "GET, POST, PATCH, DELETE, OPTION"
        )
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests for all available categories.
    """
    @app.route("/categories")
    def get_all_categories():
        # get all categories
        categories = Category.query.all()
        #current_categories= paginate_category(request, selection)
        categoriesDic = {}

        # adding all categories to the dict
        for category in categories:
            categoriesDic[category.id] = category.type              
        
        return jsonify(
            {
                "success": True,
                "categories": categoriesDic,
                "total_Categories": len(Category.query.all()),
            }
        )

    """
    @TODO:    Create an endpoint to handle GET requests for questions,including pagination (every 10 questions).  
    This endpoint should return a list of questions, number of total questions, current category, categories.
    TEST: At this point, when you start the application   you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
   Clicking on the page numbers should update the questions.
    """
    @app.route("/questions")
    def get_all_questions():
    # get all questions
        selection = Question.query.order_by(Question.id).all()
        current_questions= paginate_questions(request, selection)
    # get all categories
        catselec = Category.query.all()         
        categoriesDic = {}
        for category in catselec:
                categoriesDic[category.id] = category.type

        if len(current_questions) == 0  :
            abort(404)
        
        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_questions": len(Question.query.all()),
                "categories": categoriesDic ,

            }
        )

    
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=['DELETE'])
    def delete_questions(question_id):
        
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions= paginate_questions(request, selection)   

            return jsonify(
            {
                "success": True,
                "deleted": question_id,
                "questions": current_questions,
                "total_questions": len(Question.query.all()),
            })        

        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=['POST'])
    def add_question():
        # get the body from requist
        body = request.get_json()

        # get new data, none if not enterd
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)

        try:
            # add ..
            question = Question(question=new_question, answer=new_answer,
                                category=new_category, difficulty=new_difficulty)
            question.insert()

            # send back the current questions, to update front end
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'question created': question.id,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
            })

        except :            
            abort(422)


    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route("/search", methods=['POST'])
    def search_questions():
        body = request.get_json()
        search = body.get('searchTerm')
        questions = Question.query.filter(Question.question.ilike('%'+search+'%')).all()

        if questions:
            current_questions = paginate_questions(request, questions)
            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(questions)
            })
        else:
            abort(404)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:category_id>/questions")
    def questions_in_category(category_id):
        # retrive the category by given id
        category = Category.query.filter_by(id=category_id).one_or_none()
        if category:
            # retrive all questions in a category
            selection = Question.query.filter_by(category=str(category_id)).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                "success": True,
                "questions": current_questions,
                "total_questions": len(selection),
                "current_category": category.type,
                "current_category_id": category_id,
            })
        # if category not founs
        else:
            abort(404)
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def quiz():
        # get the qestion category an the previous question
        body = request.get_json()
        quiz_category = body.get('quiz_category')
        previous_question = body.get('previous_questions')

        try:
            if (quiz_category['id'] == 0):
                questions_query = Question.query.all()
            else:
                questions_query = Question.query.filter_by(
                    category=quiz_category['id']).all()

            randomIndex = random.randint(0, len(questions_query)-1)
            next_question = questions_query[randomIndex]

            #Questions_st = True
            while next_question.id not in previous_question:
                next_question = questions_query[randomIndex]
                return jsonify({
                    'success': True,
                    'question': {
                        "answer": next_question.answer,
                        "category": next_question.category,
                        "difficulty": next_question.difficulty,
                        "id": next_question.id,
                        "question": next_question.question
                    },
                    'previousQuestion': previous_question
                })

        except:            
            abort(404)

    """
    @TODO:
    Create error handlers for all expected errors including 404 and 422.
    """
    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
        "success": False, 
        "error": 404,
        "message": "Resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
        "success": False, 
        "error": 422,
        "message": "Unprocessable"
        }), 422

    @app.errorhandler(400)
    def Bad_request(error):
        return jsonify({
        "success": False, 
        "error": 400,
        "message": "Bad request"
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
        "success": False, 
        "error": 405,
        "message": "Method not allowed"
        }), 405
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
        "success": False, 
        "error": 500,
        "message": "Internal server error"
        }), 500

    return app

