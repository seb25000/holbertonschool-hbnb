# Implement Testing and Validation of the Endpoints

## Objective

This task involves creating and running tests for the endpoints you have developed so far. You will implement validation logic, perform thorough testing using `cURL`, and document the results of those tests. The focus is on ensuring that each endpoint works as expected and adheres to the input/output formats, status codes, and validation rules you have defined in previous tasks.

## In this task, you will

1. Implement basic validation checks for each of the attributes in your endpoints.
2. Perform black-box testing using `cURL` and the Swagger documentation generated by Flask-RESTx.
3. Create a detailed testing report, highlighting both successful and failed cases.

## Instructions

### Implement Basic Validation in the Business Logic Layer

For this task, you should revisit each of the entity models (`User`, `Place`, `Review`, `Amenity`) and ensure that basic validation is performed at the model level. Here are a few key validations to implement:

- **User:**
  - Ensure that the `first_name`, `last_name`, and `email` attributes are not empty.
  - Ensure that the `email` is in a valid email format.

- **Place:**
  - Ensure that `title` is not empty.
  - Ensure that `price` is a positive number.
  - Ensure that `latitude` is between -90 and 90.
  - Ensure that `longitude` is between -180 and 180.

- **Review:**
  - Ensure that `text` is not empty.
  - Ensure that `user_id` and `place_id` reference valid entities.

### Testing the Endpoints Using cURL

Once you have implemented the necessary validation, you should perform tests using `cURL`. Below are some examples of how to test different scenarios:

#### Testing the Creation of a User

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
}'
```

**Expected Response:**

```jsonc
{
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
}

// 200 OK
```

#### Testing Invalid Data for a User

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{
    "first_name": "",
    "last_name": "",
    "email": "invalid-email"
}'
```

**Expected Response:**

```json
{
    "error": "Invalid input data"
}

// 400 Bad Request
```

You should repeat similar tests for other entities and endpoints, focusing on:

- **Boundary Testing** (e.g., out-of-range latitude/longitude).
- **Required Fields** (e.g., missing or empty values).
- **Error Handling** (e.g., retrieving a non-existent resource).

### **Generate Swagger Documentation**

Since Flask-RESTx automatically generates Swagger documentation based on your API models, you should review this documentation to ensure it accurately reflects your endpoints. To access the Swagger documentation, visit:

```text
http://127.0.0.1:5000/api/v1/
```

Use this documentation as a reference when performing manual tests or writing automated tests.

### **Write and Run Unit Tests**

In addition to manual tests, you should write automated unit tests using Python’s `unittest` or `pytest` frameworks. Here’s a basic example of how to structure your tests:

```python
import unittest
from app import create_app

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)
```

These tests should cover both positive and negative scenarios for all endpoints.

### Document the Testing Process

As you perform your tests, keep a log of:

- The endpoints tested.
- The input data used.
- The expected output vs. the actual output.
- Any issues encountered.

This documentation will be essential when you present your results and demonstrate that your implementation meets all the requirements.

## Expected Outcome

By the end of this task, you should have:

- Implemented basic validation for all entity models.
- Performed thorough testing using cURL and other tools.
- Generated Swagger documentation to confirm that your API is correctly described.
- Created and executed unit tests using `unittest` or `pytest`.
- Documented the testing process, highlighting both successful cases and edge cases that were handled correctly.
