import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from random import randint
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'ahmedghonem@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        self.complete_data_question = {
            'question': 'just for test',
            'answer': 'hehehe test too',
            'difficulty': '5',
            'category': '1'
        }
        self.incomplete_data_question = {
            'answer': 'hehehe test too',
            'difficulty': '5',
            'category': '1'
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_retrieve_categories(self):

        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['total_categories'], 6)
        self.assertTrue(data['categories'])

    def test_retrieve_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['categories']), 6)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_404_no_questions_on_invalid_pages(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_add_question(self):
        res = self.client().post('/questions', json=self.complete_data_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['created'])

    def test_422_failed_adding_question_for_missing_data(self):
        res = self.client().post('/questions', json=self.incomplete_data_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unproccessable')

    def test_405_add_question_not_allowed(self):
        res = self.client().post('/questions/45', json=self.complete_data_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_delete_question(self):
        id = randint(1, 4000)
        res = self.client().delete('/questions/'+str(id))
        data = json.loads(res.data)

        question = Question.query.get(id)
        if not question:
            self.assertEqual(res.status_code, 422)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'unproccessable')

        else:
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(data['deleted'], id)
            self.assertTrue(data['questions'])
            self.assertTrue(data['categories'])
            self.assertTrue(data['total_questions'])

    def test_get_questions_by_category_for_invalid_numbers(self):
        res = self.client().get('/categories/-2/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


        # Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
