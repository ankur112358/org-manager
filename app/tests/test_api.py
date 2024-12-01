import os
import unittest
import tempfile
from fastapi.testclient import TestClient

os.environ["LOGLEVEL"] = "ERROR"

from app.main import app
from app.services.db_handler import reset_db

client = TestClient(app)

class TestFastAPIApp(unittest.TestCase):
    def setUp(self):
        self.db_dir = tempfile.TemporaryDirectory()
        os.environ["DATABASE_DIR"] = self.db_dir.name
        reset_db()

        self.create_org_url = "/org/create"
        self.get_org_url = "/org/get"
        self.login_url = "/admin/login"

        # Sample test data
        self.org_data = {
            "email": "admin@example.com",
            "password": "strongpassword123",
            "organization_name": "TestOrganization"
        }

    def tearDown(self):
        self.db_dir.cleanup()
        del os.environ["DATABASE_DIR"]

    def test_create_organization(self):
        """Test creating a new organization."""
        response = client.post(self.create_org_url, json=self.org_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())
        self.assertGreaterEqual(len(os.listdir(self.db_dir.name)), 2)
        self.assertIn('master.db', os.listdir(self.db_dir.name))
        self.assertIn('TestOrganization.db', os.listdir(self.db_dir.name))

    def test_get_organization(self):
        """Test retrieving an organization by name."""
        # Ensure the organization exists by creating it first
        client.post(self.create_org_url, json=self.org_data)
        # Attempt to retrieve the organization
        response = client.get(self.get_org_url, params={"organization_name": "TestOrganization"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["organization_name"], "TestOrganization")
        self.assertEqual(response.json()["admin_email"], "admin@example.com")

    def test_get_organization_not_found(self):
        """Test retrieving a non-existent organization."""
        response = client.get(self.get_org_url, params={"organization_name": "NonExistentOrg"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Organization not found")

    def test_admin_login(self):
        """Test logging in with correct credentials."""
        # Ensure the organization exists
        client.post(self.create_org_url, json=self.org_data)

        # Test login
        login_data = {
            "email": "admin@example.com",
            "password": "strongpassword123"
        }
        response = client.post(self.login_url, json=login_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())

    def test_admin_login_incorrect_credentials(self):
        """Test logging in with incorrect credentials."""
        # Ensure the organization exists
        client.post(self.create_org_url, json=self.org_data)

        # Test login with wrong password
        login_data = {
            "email": "admin@example.com",
            "password": "wrongpassword"
        }
        response = client.post(self.login_url, json=login_data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["detail"], "Invalid credentials")

    def test_create_organization_duplicate(self):
        """Test creating an organization that already exists."""
        # Create the organization for the first time
        client.post(self.create_org_url, json=self.org_data)

        # Attempt to create the same organization again
        response = client.post(self.create_org_url, json=self.org_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Organization creation failed")

if __name__ == "__main__":
    unittest.main()
