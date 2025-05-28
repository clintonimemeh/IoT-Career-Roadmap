import requests
import unittest
import sys
import json

# Use the public endpoint from frontend/.env
BACKEND_URL = "https://d369f806-187f-4f1d-afc8-a5a03877c618.preview.emergentagent.com"
API_URL = f"{BACKEND_URL}/api"

class IoTRoadmapAPITest(unittest.TestCase):
    """Test suite for IoT Career Roadmap API endpoints"""
    
    def test_01_root_endpoint(self):
        """Test the root API endpoint"""
        print("\n🔍 Testing root API endpoint...")
        response = requests.get(f"{API_URL}/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["message"], "IoT Career Roadmap API")
        print("✅ Root API endpoint test passed")
    
    def test_02_get_roadmap(self):
        """Test the roadmap endpoint"""
        print("\n🔍 Testing roadmap endpoint...")
        response = requests.get(f"{API_URL}/roadmap")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 4)  # Should have 4 roadmap levels
        
        # Verify roadmap level structure
        level = data[0]
        self.assertIn("id", level)
        self.assertIn("level_number", level)
        self.assertIn("title", level)
        self.assertIn("description", level)
        self.assertIn("difficulty_level", level)
        self.assertIn("estimated_duration_months", level)
        self.assertIn("skills_to_develop", level)
        self.assertIn("recommended_courses", level)
        self.assertIn("projects_to_complete", level)
        self.assertIn("roles_available", level)
        self.assertIn("specialization_paths", level)
        self.assertIn("milestone_achievements", level)
        
        # Verify level ordering
        self.assertEqual(data[0]["level_number"], 1)
        self.assertEqual(data[1]["level_number"], 2)
        self.assertEqual(data[2]["level_number"], 3)
        self.assertEqual(data[3]["level_number"], 4)
        
        # Store level ID for later tests
        self.level_id = data[0]["id"]
        print(f"✅ Roadmap endpoint test passed - Found {len(data)} levels")
    
    def test_03_get_level_details(self):
        """Test the level details endpoint"""
        print("\n🔍 Testing level details endpoint...")
        # Make sure we have a level ID from previous test
        if not hasattr(self, 'level_id'):
            self.test_02_get_roadmap()
        
        response = requests.get(f"{API_URL}/roadmap/level/{self.level_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verify level details structure
        self.assertIn("level", data)
        self.assertIn("skills", data)
        self.assertIn("courses", data)
        self.assertIn("projects", data)
        self.assertIn("roles", data)
        
        # Verify data relationships
        level = data["level"]
        skills = data["skills"]
        courses = data["courses"]
        projects = data["projects"]
        roles = data["roles"]
        
        # Check that skills in level match skills array
        skill_ids = [skill["id"] for skill in skills]
        for skill_id in level["skills_to_develop"]:
            self.assertIn(skill_id, skill_ids)
        
        # Check that courses in level match courses array
        course_ids = [course["id"] for course in courses]
        for course_id in level["recommended_courses"]:
            self.assertIn(course_id, course_ids)
        
        print(f"✅ Level details endpoint test passed - Found {len(skills)} skills, {len(courses)} courses, {len(projects)} projects, {len(roles)} roles")
    
    def test_04_get_skills(self):
        """Test the skills endpoint"""
        print("\n🔍 Testing skills endpoint...")
        response = requests.get(f"{API_URL}/skills")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 10)  # Should have at least 10 skills
        
        # Verify skill structure
        skill = data[0]
        self.assertIn("id", skill)
        self.assertIn("name", skill)
        self.assertIn("description", skill)
        self.assertIn("category", skill)
        self.assertIn("difficulty_level", skill)
        self.assertIn("estimated_time_hours", skill)
        
        # Test filtering by difficulty
        response = requests.get(f"{API_URL}/skills?difficulty=beginner")
        self.assertEqual(response.status_code, 200)
        beginner_skills = response.json()
        self.assertIsInstance(beginner_skills, list)
        for skill in beginner_skills:
            self.assertEqual(skill["difficulty_level"], "beginner")
        
        print(f"✅ Skills endpoint test passed - Found {len(data)} skills")
    
    def test_05_get_courses(self):
        """Test the courses endpoint"""
        print("\n🔍 Testing courses endpoint...")
        response = requests.get(f"{API_URL}/courses")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 8)  # Should have at least 8 courses
        
        # Verify course structure
        course = data[0]
        self.assertIn("id", course)
        self.assertIn("title", course)
        self.assertIn("description", course)
        self.assertIn("provider", course)
        self.assertIn("duration_weeks", course)
        self.assertIn("difficulty_level", course)
        self.assertIn("cost", course)
        self.assertIn("skills_covered", course)
        self.assertIn("prerequisites", course)
        
        # Test filtering by difficulty
        response = requests.get(f"{API_URL}/courses?difficulty=advanced")
        self.assertEqual(response.status_code, 200)
        advanced_courses = response.json()
        self.assertIsInstance(advanced_courses, list)
        for course in advanced_courses:
            self.assertEqual(course["difficulty_level"], "advanced")
        
        print(f"✅ Courses endpoint test passed - Found {len(data)} courses")
    
    def test_06_get_projects(self):
        """Test the projects endpoint"""
        print("\n🔍 Testing projects endpoint...")
        response = requests.get(f"{API_URL}/projects")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 4)  # Should have at least 4 projects
        
        # Verify project structure
        project = data[0]
        self.assertIn("id", project)
        self.assertIn("title", project)
        self.assertIn("description", project)
        self.assertIn("difficulty_level", project)
        self.assertIn("estimated_time_weeks", project)
        self.assertIn("technologies_used", project)
        self.assertIn("skills_practiced", project)
        self.assertIn("industry_relevance", project)
        self.assertIn("detailed_steps", project)
        self.assertIn("expected_outcomes", project)
        
        # Test filtering by difficulty
        response = requests.get(f"{API_URL}/projects?difficulty=expert")
        self.assertEqual(response.status_code, 200)
        expert_projects = response.json()
        self.assertIsInstance(expert_projects, list)
        for project in expert_projects:
            self.assertEqual(project["difficulty_level"], "expert")
        
        print(f"✅ Projects endpoint test passed - Found {len(data)} projects")
    
    def test_07_get_roles(self):
        """Test the roles endpoint"""
        print("\n🔍 Testing roles endpoint...")
        response = requests.get(f"{API_URL}/roles")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 4)  # Should have at least 4 roles
        
        # Verify role structure
        role = data[0]
        self.assertIn("id", role)
        self.assertIn("title", role)
        self.assertIn("description", role)
        self.assertIn("level", role)
        self.assertIn("salary_range", role)
        self.assertIn("responsibilities", role)
        self.assertIn("required_skills", role)
        self.assertIn("industry_demand", role)
        self.assertIn("growth_potential", role)
        
        # Test filtering by level
        response = requests.get(f"{API_URL}/roles?level=intermediate")
        self.assertEqual(response.status_code, 200)
        intermediate_roles = response.json()
        self.assertIsInstance(intermediate_roles, list)
        for role in intermediate_roles:
            self.assertEqual(role["level"], "intermediate")
        
        print(f"✅ Roles endpoint test passed - Found {len(data)} roles")
    
    def test_08_get_industry_insights(self):
        """Test the industry insights endpoint"""
        print("\n🔍 Testing industry insights endpoint...")
        response = requests.get(f"{API_URL}/industry-insights")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 3)  # Should have at least 3 industry insights
        
        # Verify industry insight structure
        insight = data[0]
        self.assertIn("id", insight)
        self.assertIn("specialization", insight)
        self.assertIn("market_size", insight)
        self.assertIn("growth_rate", insight)
        self.assertIn("key_trends", insight)
        self.assertIn("major_companies", insight)
        self.assertIn("future_outlook", insight)
        self.assertIn("entry_barriers", insight)
        self.assertIn("avg_salary", insight)
        
        # Test filtering by specialization
        response = requests.get(f"{API_URL}/industry-insights?specialization=industrial_iot")
        self.assertEqual(response.status_code, 200)
        industrial_insights = response.json()
        self.assertIsInstance(industrial_insights, list)
        for insight in industrial_insights:
            self.assertEqual(insight["specialization"], "industrial_iot")
        
        print(f"✅ Industry insights endpoint test passed - Found {len(data)} insights")

if __name__ == "__main__":
    print("🧪 Starting IoT Career Roadmap API Tests...")
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    print("\n🏁 All API tests completed!")
