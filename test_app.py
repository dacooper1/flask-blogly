from app import app
from unittest import TestCase

class TestCases(TestCase):
    
    def test_homepage_redirect(self):
        with app.test_client() as client:
            # import pdb
            # pdb.set_trace()
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location,"/users")

    def test_show_user_list(self):
        with app.test_client() as client:
            res = client.get('/users')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)

    def test_add_user_form(self):
        with app.test_client() as client:
           res = client.get('/users/new') 
           html = res.get_data(as_text=True)

           self.assertEqual(res.status_code, 200)
           self.assertIn('<div class="form-container">', html)

    def test_cancel_adding_new_user(self):
        with app.test_client() as client:
            res = client.get('/cancel')

            self.assertEqual(res.status_code, 302)
            self.assertIn(res.location, "/users")

    # add new post request 
    def test_add_user(self):
        with app.test_client() as client:
            res = client.post('/users/new', data={'fname': 'Melo', 'lname' : 'Ball'})
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 302)
            self.assertIn(res.location, "/users")
            self.assertIn('Melo Ball', html)

    def test_user_details(self):
        with app.test_client() as client:
            res = client.get('/users/1')
            # ask Mike about variable in testing
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="fullname">', html)

    # add edit post request
    
    # add delete post request





