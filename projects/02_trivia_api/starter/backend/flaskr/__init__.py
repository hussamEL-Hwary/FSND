import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random 

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  # enable CORS
  CORS(app, resources={r"/api/*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response 
  
  def paginate_questions(request):
    page = request.args.get('page', 1, type=int)
    start = (page-1)*QUESTIONS_PER_PAGE
    end = start+QUESTIONS_PER_PAGE
    questions = Question.query.all()
    return questions[start:end]

  def format_data(items):
    formatted_items = [item.format() for item in items]
    return formatted_items

  @app.route('/categories')
  def categories():
    categories = Category.query.all()
    formatted_categories = [(category.id, category.type) for category in categories]
    return jsonify({
      'success': True,
      'categories': formatted_categories
    })

  @app.route('/questions')
  def get_questions():
    questions = paginate_questions(request)
    if len(questions) == 0:
      abort(404)
    
    # format questions
    formatted_questions = format_data(questions)
    
    # get categories
    categories = Category.query.all()
    formatted_categories = [(category.id, category.type) for category in categories]

    total_question = len(Question.query.all())

    current_category = list(set([ques['category'] for ques in formatted_questions]))

    return jsonify({
      'success': True,
      'questions': formatted_questions,
      'total_questions': total_question,
      'categories': formatted_categories,
      'current_category': current_category
    })

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.filter_by(id=question_id).one_or_none()
    if not question:
      abort(404)

    question.delete()

    return jsonify({
      'suceess': True
    })

  @app.route('/questions', methods=['POST'])
  def create_question():
    try:
      body = request.get_json()
      new_question = Question(
        question=body.get('question'),
        answer=body.get('answer'),
        category=body.get('category'),
        difficulty=int(body.get('difficulty'))
      )

      new_question.insert()
      return jsonify({
        'sucess': True
      })
    except:
      abort(400)
    
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    