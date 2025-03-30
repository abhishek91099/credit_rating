import unittest
import json
from app import app
from models import db, Mortgage

class MortgageAPITestCase(unittest.TestCase):
    def setUp(self):
        # Set up test client and configure app for testing
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        
        # Create database tables in memory
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        # Clear database after each test
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_create_mortgage(self):
        # Test creating a new mortgage
        test_mortgage = {
            'creditScore': 750,
            'loanAmount': 300000,
            'propertyValue': 400000,
            'annualIncome': 80000,
            'debtAmount': 20000,
            'loanType': 'fixed',
            'propertyType': 'single_family'
        }
        
        response = self.app.post(
            '/api/mortgages',
            data=json.dumps(test_mortgage),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('message', data)
        self.assertIn('mortgage', data)
        self.assertIn('creditRating', data)
        
        # Verify mortgage was added to database
        with app.app_context():
            mortgage_count = Mortgage.query.count()
            self.assertEqual(mortgage_count, 1)
    
    def test_create_mortgage_missing_field(self):
        # Test creating a mortgage with missing required field
        incomplete_mortgage = {
            'creditScore': 750,
            'loanAmount': 300000,
            # Missing propertyValue
            'annualIncome': 80000,
            'debtAmount': 20000,
            'loanType': 'fixed',
            'propertyType': 'single_family'
        }
        
        response = self.app.post(
            '/api/mortgages',
            data=json.dumps(incomplete_mortgage),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertIn('Missing required field', data['error'])
    
    def test_get_all_mortgages(self):
        # Add test mortgages to database
        test_mortgages = [
            Mortgage(credit_score=750, loan_amount=300000, property_value=400000, 
                     annual_income=80000, debt_amount=20000, loan_type='fixed', 
                     property_type='single_family'),
            Mortgage(credit_score=680, loan_amount=200000, property_value=250000, 
                     annual_income=65000, debt_amount=30000, loan_type='adjustable', 
                     property_type='condo')
        ]
        
        with app.app_context():
            for mortgage in test_mortgages:
                db.session.add(mortgage)
            db.session.commit()
        
        # Get all mortgages
        response = self.app.get('/api/mortgages')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
    
    def test_get_mortgage_by_id(self):
        # Add test mortgage
        test_mortgage = Mortgage(credit_score=750, loan_amount=300000, property_value=400000, 
                                 annual_income=80000, debt_amount=20000, loan_type='fixed', 
                                 property_type='single_family')
        
        with app.app_context():
            db.session.add(test_mortgage)
            db.session.commit()
            mortgage_id = test_mortgage.id
        
        # Get mortgage by ID
        response = self.app.get(f'/api/mortgages/{mortgage_id}')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['id'], mortgage_id)
        self.assertEqual(data['credit_score'], 750)
    
    def test_get_mortgage_not_found(self):
        # Test getting non-existent mortgage
        response = self.app.get('/api/mortgages/999')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Mortgage not found')
    
    def test_update_mortgage(self):
        # Add test mortgage
        test_mortgage = Mortgage(credit_score=750, loan_amount=300000, property_value=400000, 
                                 annual_income=80000, debt_amount=20000, loan_type='fixed', 
                                 property_type='single_family')
        
        with app.app_context():
            db.session.add(test_mortgage)
            db.session.commit()
            mortgage_id = test_mortgage.id
        
        # Update mortgage
        update_data = {
            'creditScore': 720,
            'loanAmount': 320000,
            'propertyValue': 400000,
            'annualIncome': 85000,
            'debtAmount': 25000,
            'loanType': 'adjustable',
            'propertyType': 'single_family'
        }
        
        response = self.app.put(
            f'/api/mortgages/{mortgage_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', data)
        self.assertIn('mortgage', data)
        self.assertIn('creditRating', data)
        
        # Verify mortgage was updated
        with app.app_context():
            updated_mortgage = Mortgage.query.get(mortgage_id)
            self.assertEqual(updated_mortgage.credit_score, 720)
            self.assertEqual(updated_mortgage.loan_amount, 320000)
            self.assertEqual(updated_mortgage.loan_type, 'adjustable')
    
    def test_update_mortgage_not_found(self):
        # Test updating non-existent mortgage
        update_data = {'creditScore': 720}
        
        response = self.app.put(
            '/api/mortgages/999',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Mortgage not found')
    
    def test_delete_mortgage(self):
        # Add test mortgage
        test_mortgage = Mortgage(credit_score=750, loan_amount=300000, property_value=400000, 
                                 annual_income=80000, debt_amount=20000, loan_type='fixed', 
                                 property_type='single_family')
        
        with app.app_context():
            db.session.add(test_mortgage)
            db.session.commit()
            mortgage_id = test_mortgage.id
        
        # Delete mortgage
        response = self.app.delete(f'/api/mortgages/{mortgage_id}')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', data)
        
        # Verify mortgage was deleted
        with app.app_context():
            deleted_mortgage = Mortgage.query.get(mortgage_id)
            self.assertIsNone(deleted_mortgage)
    
    def test_delete_mortgage_not_found(self):
        # Test deleting non-existent mortgage
        response = self.app.delete('/api/mortgages/999')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Mortgage not found')
    
    def test_calculate_rating(self):
        # Test calculate rating endpoint
        test_data = {
            'creditScore': 750,
            'loanAmount': 300000,
            'propertyValue': 400000,
            'annualIncome': 80000,
            'debtAmount': 20000,
            'loanType': 'fixed',
            'propertyType': 'single_family'
        }
        
        response = self.app.post(
            '/api/calculate-rating',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('creditRating', data)
        self.assertIn('riskScore', data)
        self.assertIn('components', data)
        
        # Check that all components are included
        components = data['components']
        expected_components = ['loanToValue', 'debtToIncome', 'creditScore', 
                              'loanType', 'propertyType', 'avgCreditScore']
        for component in expected_components:
            self.assertIn(component, components)

if __name__ == '__main__':
    unittest.main()