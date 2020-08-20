import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, questions):
    page = request.args.get('page', 1, type=int)
    start = (page-1) * QUESTIONS_PER_PAGE
    end = start+QUESTIONS_PER_PAGE
    formatted_questions = [question.format() for question in questions]
    current_questions = formatted_questions[start:end]
    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS,PATCH')
        return response

    @app.route('/categories')
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        formatted_categories = [category.format() for category in categories]
        if len(categories) == 0:
            abort(404)
            return
        return jsonify({
            'success': True,
            'categories': formatted_categories,
            'total_categories': len(categories)})

    @app.route('/questions', methods=['GET'])
    def retrieve_questions():
        categories = get_categories().get_json()['categories']
        categories = [category['type'] for category in categories]

        questions = Question.query.order_by(Question.id).all()

        current_questions = paginate_questions(request, questions)
        if len(current_questions) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions),
            'categories': categories,
            'current_category': None
        })

    @app.route('/questions', methods=['POST'])
    def search_and_add_questions():
        body = request.get_json()
        search_term = body.get('searchTerm', None)
        if request.method != 'POST':
            abort(405)
        if not search_term:
            question = body.get('question', None)
            answer = body.get('answer', None)
            difficulty = body.get('difficulty', None)
            category = body.get('category', None)

            if not question or not answer or not difficulty or not category:
                abort(422)

            new_question = Question(question, answer, category, difficulty)
            new_question.insert()
            new_question_id = new_question.format()['id']
            updated_questions = retrieve_questions().get_json()
            return jsonify({
                'success': True,
                'created': new_question_id,
                'questions': updated_questions['questions'],
                'categories': updated_questions['categories'],
                'total_questions': len(updated_questions['questions']),
                'current_category': None
            })

        else:
            wanted_questions = Question.query.filter(
                Question.question.ilike('%'+search_term.lower()+'%')).all()

            current_questions = paginate_questions(
                request, wanted_questions)
            if not current_questions:
                abort(404)
            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(wanted_questions),
                'current_category': None
            })

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():

        body = request.get_json()
        prev_questions = body.get('previous_questions', None)
        quiz_category = body.get('quiz_category', None)
        id = int(quiz_category['id'])

        if id == 0:
            quiz_questions = retrieve_questions().get_json()
        else:
            quiz_questions = get_questions_by_category(id-1).get_json()

        if len(prev_questions) == quiz_questions['total_questions']:
            return jsonify({
                'question': None,
            })

        random_question = quiz_questions['questions'][0]
        while random_question['id'] in prev_questions:
            random_question = random.choice(quiz_questions['questions'])
        return jsonify({
            'question': random_question
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            if not question:
                abort(422)
            question.delete()
            new_questions = retrieve_questions().get_json()
            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': new_questions['questions'],
                'categories': new_questions['categories'],
                'total_questions': len(new_questions['questions']),
                'current_category': None
            })
        except:
            abort(422)

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):

        try:
            all_questions = Question.query.order_by(
                Question.id).filter(Question.category == category_id+1).all()
            current_questions = paginate_questions(request, all_questions)
            categories = get_categories().get_json()
            if len(current_questions) == 0:
                abort(404)
            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(all_questions),
                'current_category': category_id,
                'categories': categories
            })
        except:
            abort(422)

    @app.route('/')
    def index():
        return jsonify({'message': 'Welcome to the trivia API'})

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unproccessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unproccessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405
    return app
