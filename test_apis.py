import unittest
import json
from app import create_app, db
from app.models.student import Student


class StudentManagementAPITestCase(unittest.TestCase):
    """Test cases for Student Management API"""
    
    def setUp(self):
        """Set up test client and database before each test"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Create tables
        db.create_all()
        
        # Add sample data
        self.sample_student = Student(
            name='Alice Johnson',
            department='Computer Science',
            cgpa=3.9,
            email='alice@student.edu'
        )
        db.session.add(self.sample_student)
        db.session.commit()
    
    def tearDown(self):
        """Clean up after each test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    # ==================== Health Check Tests ====================
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['status'], 'healthy')
    
    # ==================== GET All Students Tests ====================
    
    def test_get_all_students_success(self):
        """Test getting all students successfully"""
        response = self.client.get('/api/students')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertTrue(data['success'])
        self.assertIn('data', data)
        self.assertIn('pagination', data)
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['pagination']['total'], 1)
    
    def test_get_all_students_with_pagination(self):
        """Test getting all students with pagination parameters"""
        # Add more students
        for i in range(15):
            student = Student(
                name=f'Student {i}',
                department='Computer Science',
                cgpa=3.5,
                email=f'student{i}@student.edu'
            )
            db.session.add(student)
        db.session.commit()
        
        # Test page 1
        response = self.client.get('/api/students?page=1&per_page=5')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertTrue(data['success'])
        self.assertEqual(len(data['data']), 5)
        self.assertEqual(data['pagination']['page'], 1)
        self.assertEqual(data['pagination']['per_page'], 5)
        self.assertEqual(data['pagination']['total'], 16)
        self.assertEqual(data['pagination']['pages'], 4)
    
    def test_get_all_students_invalid_page(self):
        """Test getting students with invalid page number"""
        response = self.client.get('/api/students?page=invalid')
        self.assertEqual(response.status_code, 500)
    
    def test_get_all_students_per_page_exceeds_max(self):
        """Test per_page exceeding maximum is capped"""
        response = self.client.get('/api/students?page=1&per_page=200')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertEqual(data['pagination']['per_page'], 100)
    
    # ==================== GET Single Student Tests ====================
    
    def test_get_student_by_id_success(self):
        """Test getting a specific student by ID"""
        response = self.client.get(f'/api/students/{self.sample_student.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['id'], self.sample_student.id)
        self.assertEqual(data['data']['name'], 'Alice Johnson')
        self.assertEqual(data['data']['email'], 'alice@student.edu')
    
    def test_get_student_not_found(self):
        """Test getting a non-existent student"""
        response = self.client.get('/api/students/999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 'Student not found')
    
    def test_get_student_invalid_id(self):
        """Test getting student with invalid ID format"""
        response = self.client.get('/api/students/invalid')
        self.assertEqual(response.status_code, 404)
    
    # ==================== CREATE Student Tests ====================
    
    def test_create_student_success(self):
        """Test creating a student successfully"""
        student_data = {
            'name': 'Bob Smith',
            'department': 'Data Science',
            'cgpa': 3.8,
            'email': 'bob@student.edu'
        }
        response = self.client.post(
            '/api/students',
            data=json.dumps(student_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        
        self.assertTrue(data['success'])
        self.assertIn('data', data)
        self.assertEqual(data['data']['name'], 'Bob Smith')
        self.assertEqual(data['data']['department'], 'Data Science')
        self.assertEqual(data['data']['cgpa'], 3.8)
        self.assertEqual(data['data']['email'], 'bob@student.edu')
    
    def test_create_student_missing_name(self):
        """Test creating student without name"""
        student_data = {
            'department': 'Data Science',
            'cgpa': 3.8,
            'email': 'bob@student.edu'
        }
        response = self.client.post(
            '/api/students',
            data=json.dumps(student_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('Missing required fields', data['error'])
    
    def test_create_student_missing_department(self):
        """Test creating student without department"""
        student_data = {
            'name': 'Bob Smith',
            'cgpa': 3.8,
            'email': 'bob@student.edu'
        }
        response = self.client.post(
            '/api/students',
            data=json.dumps(student_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_create_student_missing_cgpa(self):
        """Test creating student without CGPA"""
        student_data = {
            'name': 'Bob Smith',
            'department': 'Data Science',
            'email': 'bob@student.edu'
        }
        response = self.client.post(
            '/api/students',
            data=json.dumps(student_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_create_student_missing_email(self):
        """Test creating student without email"""
        student_data = {
            'name': 'Bob Smith',
            'department': 'Data Science',
            'cgpa': 3.8
        }
        response = self.client.post(
            '/api/students',
            data=json.dumps(student_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_create_student_invalid_email(self):
        """Test creating student with invalid email"""
        student_data = {
            'name': 'Bob Smith',
            'department': 'Data Science',
            'cgpa': 3.8,
            'email': 'invalid-email'
        }
        response = self.client.post(
            '/api/students',
            data=json.dumps(student_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_create_student_duplicate_email(self):
        """Test creating student with duplicate email"""
        student_data = {
            'name': 'Bob Smith',
            'department': 'Data Science',
            'cgpa': 3.8,
            'email': 'alice@student.edu'  # Already exists
        }
        response = self.client.post(
            '/api/students',
            data=json.dumps(student_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 409)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 'Email already exists')
    
    def test_create_student_cgpa_too_high(self):
        """Test creating student with CGPA > 4.0"""
        student_data = {
            'name': 'Bob Smith',
            'department': 'Data Science',
            'cgpa': 4.5,
            'email': 'bob@student.edu'
        }
        response = self.client.post(
            '/api/students',
            data=json.dumps(student_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('CGPA cannot exceed 4.0', data['error'])
    
    def test_create_student_cgpa_negative(self):
        """Test creating student with negative CGPA"""
        student_data = {
            'name': 'Bob Smith',
            'department': 'Data Science',
            'cgpa': -1.5,
            'email': 'bob@student.edu'
        }
        response = self.client.post(
            '/api/students',
            data=json.dumps(student_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_create_student_short_name(self):
        """Test creating student with name < 2 characters"""
        student_data = {
            'name': 'A',
            'department': 'Data Science',
            'cgpa': 3.8,
            'email': 'bob@student.edu'
        }
        response = self.client.post(
            '/api/students',
            data=json.dumps(student_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_create_student_long_name(self):
        """Test creating student with name > 100 characters"""
        long_name = 'A' * 101
        student_data = {
            'name': long_name,
            'department': 'Data Science',
            'cgpa': 3.8,
            'email': 'bob@student.edu'
        }
        response = self.client.post(
            '/api/students',
            data=json.dumps(student_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_create_student_invalid_cgpa_type(self):
        """Test creating student with invalid CGPA type"""
        student_data = {
            'name': 'Bob Smith',
            'department': 'Data Science',
            'cgpa': 'abc',
            'email': 'bob@student.edu'
        }
        response = self.client.post(
            '/api/students',
            data=json.dumps(student_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_create_student_empty_body(self):
        """Test creating student with empty body"""
        response = self.client.post(
            '/api/students',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_create_student_no_body(self):
        """Test creating student with no body"""
        response = self.client.post(
            '/api/students',
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    # ==================== UPDATE Student Tests ====================
    
    def test_update_student_success(self):
        """Test updating a student successfully"""
        update_data = {
            'cgpa': 3.95,
            'department': 'Data Science'
        }
        response = self.client.put(
            f'/api/students/{self.sample_student.id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['cgpa'], 3.95)
        self.assertEqual(data['data']['department'], 'Data Science')
        self.assertEqual(data['data']['name'], 'Alice Johnson')  # Unchanged
    
    def test_update_student_partial_update(self):
        """Test partial update of student"""
        update_data = {'cgpa': 3.92}
        response = self.client.put(
            f'/api/students/{self.sample_student.id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['cgpa'], 3.92)
        self.assertEqual(data['data']['name'], 'Alice Johnson')  # Unchanged
    
    def test_update_student_not_found(self):
        """Test updating a non-existent student"""
        update_data = {'cgpa': 3.95}
        response = self.client.put(
            '/api/students/999',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_update_student_invalid_cgpa(self):
        """Test updating student with invalid CGPA"""
        update_data = {'cgpa': 4.5}
        response = self.client.put(
            f'/api/students/{self.sample_student.id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_update_student_invalid_email(self):
        """Test updating student with invalid email"""
        update_data = {'email': 'invalid-email'}
        response = self.client.put(
            f'/api/students/{self.sample_student.id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_update_student_duplicate_email(self):
        """Test updating student with duplicate email"""
        # Add another student
        other_student = Student(
            name='Bob Smith',
            department='Data Science',
            cgpa=3.8,
            email='bob@student.edu'
        )
        db.session.add(other_student)
        db.session.commit()
        
        # Try to update first student with second student's email
        update_data = {'email': 'bob@student.edu'}
        response = self.client.put(
            f'/api/students/{self.sample_student.id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 409)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_update_student_empty_body(self):
        """Test updating student with empty body"""
        response = self.client.put(
            f'/api/students/{self.sample_student.id}',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_update_student_no_body(self):
        """Test updating student with no body"""
        response = self.client.put(
            f'/api/students/{self.sample_student.id}',
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    # ==================== DELETE Student Tests ====================
    
    def test_delete_student_success(self):
        """Test deleting a student successfully"""
        student_id = self.sample_student.id
        response = self.client.delete(f'/api/students/{student_id}')
        
        self.assertEqual(response.status_code, 204)
        
        # Verify student is deleted
        student = Student.query.get(student_id)
        self.assertIsNone(student)
    
    def test_delete_student_not_found(self):
        """Test deleting a non-existent student"""
        response = self.client.delete('/api/students/999')
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    # ==================== Database Tests ====================
    
    def test_student_creation_timestamps(self):
        """Test that created_at and updated_at timestamps are set"""
        student = Student(
            name='Charlie Brown',
            department='Engineering',
            cgpa=3.7,
            email='charlie@student.edu'
        )
        db.session.add(student)
        db.session.commit()
        
        self.assertIsNotNone(student.created_at)
        self.assertIsNotNone(student.updated_at)
        self.assertEqual(student.created_at, student.updated_at)
    
    def test_student_to_dict(self):
        """Test Student.to_dict() method"""
        result = self.sample_student.to_dict()
        
        self.assertEqual(result['id'], self.sample_student.id)
        self.assertEqual(result['name'], 'Alice Johnson')
        self.assertEqual(result['department'], 'Computer Science')
        self.assertEqual(result['cgpa'], 3.9)
        self.assertEqual(result['email'], 'alice@student.edu')


if __name__ == '__main__':
    unittest.main()
