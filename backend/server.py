from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
from enum import Enum

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="IoT Career Roadmap API", description="API for IoT Professional Development Platform")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Enums
class DifficultyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class SpecializationArea(str, Enum):
    INDUSTRIAL_IOT = "industrial_iot"
    SMART_CITIES = "smart_cities"
    HEALTHCARE_IOT = "healthcare_iot"
    AUTOMOTIVE_IOT = "automotive_iot"
    CONSUMER_IOT = "consumer_iot"
    AGRICULTURE_IOT = "agriculture_iot"

# Data Models
class Skill(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    category: str  # technical, soft, business
    difficulty_level: DifficultyLevel
    estimated_time_hours: int

class Course(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    provider: str
    duration_weeks: int
    difficulty_level: DifficultyLevel
    cost: Optional[str] = None
    url: Optional[str] = None
    skills_covered: List[str] = []
    prerequisites: List[str] = []

class Project(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    difficulty_level: DifficultyLevel
    estimated_time_weeks: int
    technologies_used: List[str] = []
    skills_practiced: List[str] = []
    industry_relevance: List[SpecializationArea] = []
    detailed_steps: List[str] = []
    expected_outcomes: List[str] = []

class Role(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    level: DifficultyLevel
    salary_range: str
    responsibilities: List[str] = []
    required_skills: List[str] = []
    industry_demand: str  # high, medium, low
    growth_potential: str

class RoadmapLevel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    level_number: int
    title: str
    description: str
    difficulty_level: DifficultyLevel
    estimated_duration_months: int
    skills_to_develop: List[str] = []
    recommended_courses: List[str] = []
    projects_to_complete: List[str] = []
    roles_available: List[str] = []
    specialization_paths: List[SpecializationArea] = []
    milestone_achievements: List[str] = []

class IndustryInsight(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    specialization: SpecializationArea
    market_size: str
    growth_rate: str
    key_trends: List[str] = []
    major_companies: List[str] = []
    future_outlook: str
    entry_barriers: str
    avg_salary: str

# API Endpoints
@api_router.get("/")
async def root():
    return {"message": "IoT Career Roadmap API", "version": "1.0"}

@api_router.get("/roadmap", response_model=List[RoadmapLevel])
async def get_roadmap():
    """Get the complete IoT career roadmap"""
    roadmap_data = await db.roadmap_levels.find().sort("level_number", 1).to_list(100)
    if not roadmap_data:
        # Initialize with sample data if empty
        await initialize_roadmap_data()
        roadmap_data = await db.roadmap_levels.find().sort("level_number", 1).to_list(100)
    return [RoadmapLevel(**level) for level in roadmap_data]

@api_router.get("/skills", response_model=List[Skill])
async def get_skills(difficulty: Optional[DifficultyLevel] = None):
    """Get all skills, optionally filtered by difficulty level"""
    query = {"difficulty_level": difficulty} if difficulty else {}
    skills_data = await db.skills.find(query).to_list(1000)
    return [Skill(**skill) for skill in skills_data]

@api_router.get("/courses", response_model=List[Course])
async def get_courses(difficulty: Optional[DifficultyLevel] = None):
    """Get all courses, optionally filtered by difficulty level"""
    query = {"difficulty_level": difficulty} if difficulty else {}
    courses_data = await db.courses.find(query).to_list(1000)
    return [Course(**course) for course in courses_data]

@api_router.get("/projects", response_model=List[Project])
async def get_projects(difficulty: Optional[DifficultyLevel] = None):
    """Get all projects, optionally filtered by difficulty level"""
    query = {"difficulty_level": difficulty} if difficulty else {}
    projects_data = await db.projects.find(query).to_list(1000)
    return [Project(**project) for project in projects_data]

@api_router.get("/roles", response_model=List[Role])
async def get_roles(level: Optional[DifficultyLevel] = None):
    """Get all roles, optionally filtered by level"""
    query = {"level": level} if level else {}
    roles_data = await db.roles.find(query).to_list(1000)
    return [Role(**role) for role in roles_data]

@api_router.get("/industry-insights", response_model=List[IndustryInsight])
async def get_industry_insights(specialization: Optional[SpecializationArea] = None):
    """Get industry insights, optionally filtered by specialization"""
    query = {"specialization": specialization} if specialization else {}
    insights_data = await db.industry_insights.find(query).to_list(100)
    return [IndustryInsight(**insight) for insight in insights_data]

@api_router.get("/roadmap/level/{level_id}")
async def get_level_details(level_id: str):
    """Get detailed information for a specific roadmap level"""
    level_data = await db.roadmap_levels.find_one({"id": level_id})
    if not level_data:
        raise HTTPException(status_code=404, detail="Level not found")
    
    # Get associated skills, courses, projects, and roles
    skills = await db.skills.find({"id": {"$in": level_data.get("skills_to_develop", [])}}).to_list(100)
    courses = await db.courses.find({"id": {"$in": level_data.get("recommended_courses", [])}}).to_list(100)
    projects = await db.projects.find({"id": {"$in": level_data.get("projects_to_complete", [])}}).to_list(100)
    roles = await db.roles.find({"id": {"$in": level_data.get("roles_available", [])}}).to_list(100)
    
    return {
        "level": RoadmapLevel(**level_data),
        "skills": [Skill(**skill) for skill in skills],
        "courses": [Course(**course) for course in courses],
        "projects": [Project(**project) for project in projects],
        "roles": [Role(**role) for role in roles]
    }

async def initialize_roadmap_data():
    """Initialize the database with comprehensive IoT career roadmap data"""
    
    # Skills Data
    skills_data = [
        {
            "id": "skill_1", "name": "Electronics Fundamentals", "description": "Understanding of basic electronic components, circuits, and principles",
            "category": "technical", "difficulty_level": "beginner", "estimated_time_hours": 40
        },
        {
            "id": "skill_2", "name": "Programming (Python/C++)", "description": "Proficiency in programming languages commonly used in IoT",
            "category": "technical", "difficulty_level": "beginner", "estimated_time_hours": 80
        },
        {
            "id": "skill_3", "name": "Networking Protocols", "description": "Understanding of TCP/IP, HTTP, MQTT, CoAP and other IoT protocols",
            "category": "technical", "difficulty_level": "intermediate", "estimated_time_hours": 60
        },
        {
            "id": "skill_4", "name": "Cloud Platforms", "description": "Experience with AWS IoT, Azure IoT, Google Cloud IoT",
            "category": "technical", "difficulty_level": "intermediate", "estimated_time_hours": 70
        },
        {
            "id": "skill_5", "name": "Data Analytics", "description": "Ability to analyze and visualize IoT data using tools like Python, R, or Tableau",
            "category": "technical", "difficulty_level": "intermediate", "estimated_time_hours": 90
        },
        {
            "id": "skill_6", "name": "Security & Privacy", "description": "Understanding of IoT security challenges and implementation of security measures",
            "category": "technical", "difficulty_level": "advanced", "estimated_time_hours": 100
        },
        {
            "id": "skill_7", "name": "Machine Learning", "description": "Implementing ML algorithms for IoT data processing and edge computing",
            "category": "technical", "difficulty_level": "advanced", "estimated_time_hours": 120
        },
        {
            "id": "skill_8", "name": "System Architecture", "description": "Designing scalable and robust IoT system architectures",
            "category": "technical", "difficulty_level": "expert", "estimated_time_hours": 150
        },
        {
            "id": "skill_9", "name": "Project Management", "description": "Leading IoT projects from conception to deployment",
            "category": "business", "difficulty_level": "intermediate", "estimated_time_hours": 50
        },
        {
            "id": "skill_10", "name": "Communication Skills", "description": "Effectively communicating technical concepts to stakeholders",
            "category": "soft", "difficulty_level": "beginner", "estimated_time_hours": 30
        }
    ]
    
    # Courses Data
    courses_data = [
        {
            "id": "course_1", "title": "Introduction to IoT", "description": "Comprehensive introduction to Internet of Things concepts and applications",
            "provider": "Coursera", "duration_weeks": 4, "difficulty_level": "beginner", "cost": "Free",
            "skills_covered": ["skill_1", "skill_10"], "prerequisites": []
        },
        {
            "id": "course_2", "title": "IoT Programming with Python", "description": "Learn to program IoT devices using Python",
            "provider": "Udemy", "duration_weeks": 6, "difficulty_level": "beginner", "cost": "$49",
            "skills_covered": ["skill_2"], "prerequisites": ["course_1"]
        },
        {
            "id": "course_3", "title": "IoT Networking and Protocols", "description": "Deep dive into IoT communication protocols and networking",
            "provider": "edX", "duration_weeks": 8, "difficulty_level": "intermediate", "cost": "$99",
            "skills_covered": ["skill_3"], "prerequisites": ["course_1", "course_2"]
        },
        {
            "id": "course_4", "title": "Cloud Computing for IoT", "description": "Implementing IoT solutions using cloud platforms",
            "provider": "AWS Training", "duration_weeks": 6, "difficulty_level": "intermediate", "cost": "$199",
            "skills_covered": ["skill_4"], "prerequisites": ["course_3"]
        },
        {
            "id": "course_5", "title": "IoT Data Analytics", "description": "Analyzing and visualizing IoT data for insights",
            "provider": "Coursera", "duration_weeks": 8, "difficulty_level": "intermediate", "cost": "$79",
            "skills_covered": ["skill_5"], "prerequisites": ["course_2"]
        },
        {
            "id": "course_6", "title": "IoT Security", "description": "Comprehensive IoT security and privacy protection",
            "provider": "Cybrary", "duration_weeks": 10, "difficulty_level": "advanced", "cost": "$299",
            "skills_covered": ["skill_6"], "prerequisites": ["course_3", "course_4"]
        },
        {
            "id": "course_7", "title": "AI/ML for IoT", "description": "Implementing machine learning in IoT systems",
            "provider": "Stanford Online", "duration_weeks": 12, "difficulty_level": "advanced", "cost": "$499",
            "skills_covered": ["skill_7"], "prerequisites": ["course_5"]
        },
        {
            "id": "course_8", "title": "IoT System Architecture", "description": "Designing enterprise-grade IoT architectures",
            "provider": "MIT Professional Education", "duration_weeks": 8, "difficulty_level": "expert", "cost": "$799",
            "skills_covered": ["skill_8"], "prerequisites": ["course_6", "course_7"]
        }
    ]
    
    # Projects Data
    projects_data = [
        {
            "id": "project_1", "title": "Smart Home Temperature Monitor", "description": "Build a basic temperature monitoring system using Arduino",
            "difficulty_level": "beginner", "estimated_time_weeks": 2, "technologies_used": ["Arduino", "Temperature Sensor", "WiFi"],
            "skills_practiced": ["skill_1", "skill_2"], "industry_relevance": ["consumer_iot"],
            "detailed_steps": ["Set up Arduino", "Connect temperature sensor", "Program data reading", "Display on LCD"],
            "expected_outcomes": ["Working temperature monitor", "Basic IoT understanding", "Arduino programming experience"]
        },
        {
            "id": "project_2", "title": "IoT Weather Station", "description": "Create a comprehensive weather monitoring system with cloud connectivity",
            "difficulty_level": "intermediate", "estimated_time_weeks": 4, "technologies_used": ["Raspberry Pi", "Multiple Sensors", "MQTT", "Cloud"],
            "skills_practiced": ["skill_2", "skill_3", "skill_4"], "industry_relevance": ["smart_cities", "agriculture_iot"],
            "detailed_steps": ["Setup Raspberry Pi", "Connect multiple sensors", "Implement MQTT communication", "Store data in cloud"],
            "expected_outcomes": ["Complete weather station", "Cloud integration experience", "Protocol implementation"]
        },
        {
            "id": "project_3", "title": "Industrial Equipment Monitor", "description": "Develop a system to monitor industrial equipment health and performance",
            "difficulty_level": "advanced", "estimated_time_weeks": 8, "technologies_used": ["Industrial Sensors", "Edge Computing", "ML", "Dashboard"],
            "skills_practiced": ["skill_5", "skill_6", "skill_7"], "industry_relevance": ["industrial_iot"],
            "detailed_steps": ["Install industrial sensors", "Implement edge computing", "Develop ML algorithms", "Create monitoring dashboard"],
            "expected_outcomes": ["Predictive maintenance system", "ML implementation", "Industrial IoT experience"]
        },
        {
            "id": "project_4", "title": "Smart City Traffic Management", "description": "Design and implement a traffic optimization system using IoT",
            "difficulty_level": "expert", "estimated_time_weeks": 12, "technologies_used": ["Traffic Sensors", "AI", "Real-time Analytics", "Mobile App"],
            "skills_practiced": ["skill_7", "skill_8", "skill_9"], "industry_relevance": ["smart_cities"],
            "detailed_steps": ["Deploy traffic sensors", "Implement AI algorithms", "Build real-time analytics", "Develop mobile interface"],
            "expected_outcomes": ["Complete traffic system", "AI implementation", "System architecture design"]
        }
    ]
    
    # Roles Data
    roles_data = [
        {
            "id": "role_1", "title": "IoT Developer", "description": "Entry-level position developing IoT applications and prototypes",
            "level": "beginner", "salary_range": "$50,000 - $70,000", "industry_demand": "high", "growth_potential": "excellent",
            "responsibilities": ["Develop IoT prototypes", "Program embedded devices", "Basic testing and debugging"],
            "required_skills": ["skill_1", "skill_2", "skill_10"]
        },
        {
            "id": "role_2", "title": "IoT Solutions Engineer", "description": "Design and implement IoT solutions for specific business needs",
            "level": "intermediate", "salary_range": "$70,000 - $95,000", "industry_demand": "high", "growth_potential": "excellent",
            "responsibilities": ["Design IoT solutions", "Integrate cloud platforms", "Work with clients"],
            "required_skills": ["skill_2", "skill_3", "skill_4", "skill_9"]
        },
        {
            "id": "role_3", "title": "IoT Security Specialist", "description": "Focus on securing IoT systems and data protection",
            "level": "advanced", "salary_range": "$90,000 - $120,000", "industry_demand": "very high", "growth_potential": "outstanding",
            "responsibilities": ["Implement security measures", "Conduct security audits", "Develop security protocols"],
            "required_skills": ["skill_6", "skill_3", "skill_8"]
        },
        {
            "id": "role_4", "title": "IoT Architect", "description": "Senior role designing enterprise-scale IoT architectures",
            "level": "expert", "salary_range": "$120,000 - $180,000", "industry_demand": "very high", "growth_potential": "outstanding",
            "responsibilities": ["Design system architectures", "Lead technical teams", "Strategic planning"],
            "required_skills": ["skill_8", "skill_9", "skill_6", "skill_7"]
        }
    ]
    
    # Roadmap Levels Data
    roadmap_data = [
        {
            "id": "level_1", "level_number": 1, "title": "IoT Foundation", "description": "Build fundamental knowledge and skills in IoT",
            "difficulty_level": "beginner", "estimated_duration_months": 3,
            "skills_to_develop": ["skill_1", "skill_2", "skill_10"],
            "recommended_courses": ["course_1", "course_2"],
            "projects_to_complete": ["project_1"],
            "roles_available": ["role_1"],
            "specialization_paths": ["consumer_iot"],
            "milestone_achievements": ["Completed first IoT project", "Basic programming skills", "Understanding of IoT ecosystem"]
        },
        {
            "id": "level_2", "level_number": 2, "title": "IoT Development", "description": "Develop intermediate skills and start specializing",
            "difficulty_level": "intermediate", "estimated_duration_months": 6,
            "skills_to_develop": ["skill_3", "skill_4", "skill_5", "skill_9"],
            "recommended_courses": ["course_3", "course_4", "course_5"],
            "projects_to_complete": ["project_2"],
            "roles_available": ["role_2"],
            "specialization_paths": ["smart_cities", "agriculture_iot", "healthcare_iot"],
            "milestone_achievements": ["Cloud platform integration", "Data analytics capabilities", "Protocol implementation"]
        },
        {
            "id": "level_3", "level_number": 3, "title": "IoT Specialization", "description": "Advanced skills with focus on security and AI",
            "difficulty_level": "advanced", "estimated_duration_months": 9,
            "skills_to_develop": ["skill_6", "skill_7"],
            "recommended_courses": ["course_6", "course_7"],
            "projects_to_complete": ["project_3"],
            "roles_available": ["role_3"],
            "specialization_paths": ["industrial_iot", "automotive_iot"],
            "milestone_achievements": ["Security implementation", "ML integration", "Advanced project completion"]
        },
        {
            "id": "level_4", "level_number": 4, "title": "IoT Leadership", "description": "Expert-level skills and leadership capabilities",
            "difficulty_level": "expert", "estimated_duration_months": 12,
            "skills_to_develop": ["skill_8"],
            "recommended_courses": ["course_8"],
            "projects_to_complete": ["project_4"],
            "roles_available": ["role_4"],
            "specialization_paths": ["industrial_iot", "smart_cities", "healthcare_iot"],
            "milestone_achievements": ["System architecture design", "Team leadership", "Enterprise-scale deployment"]
        }
    ]
    
    # Industry Insights Data
    industry_data = [
        {
            "id": "insight_1", "specialization": "industrial_iot", "market_size": "$263.4 billion by 2027",
            "growth_rate": "16.7% CAGR", "avg_salary": "$95,000 - $140,000",
            "key_trends": ["Predictive maintenance", "Digital twins", "Edge computing", "5G integration"],
            "major_companies": ["GE", "Siemens", "Honeywell", "Schneider Electric"],
            "future_outlook": "Massive growth expected with Industry 4.0 adoption",
            "entry_barriers": "Requires understanding of industrial processes and safety standards"
        },
        {
            "id": "insight_2", "specialization": "smart_cities", "market_size": "$2.5 trillion by 2025",
            "growth_rate": "18.4% CAGR", "avg_salary": "$80,000 - $120,000",
            "key_trends": ["Smart traffic management", "Environmental monitoring", "Energy optimization", "Citizen services"],
            "major_companies": ["IBM", "Cisco", "Microsoft", "Oracle"],
            "future_outlook": "Huge opportunities as cities digitize infrastructure",
            "entry_barriers": "Understanding of urban planning and government processes helpful"
        },
        {
            "id": "insight_3", "specialization": "healthcare_iot", "market_size": "$659.8 billion by 2025",
            "growth_rate": "25.9% CAGR", "avg_salary": "$85,000 - $130,000",
            "key_trends": ["Remote patient monitoring", "Wearable devices", "Telemedicine", "AI diagnostics"],
            "major_companies": ["Philips", "GE Healthcare", "Medtronic", "Abbott"],
            "future_outlook": "Accelerated growth post-pandemic, regulatory support",
            "entry_barriers": "Requires knowledge of healthcare regulations and patient privacy"
        }
    ]
    
    # Insert all data
    await db.skills.delete_many({})
    await db.courses.delete_many({})
    await db.projects.delete_many({})
    await db.roles.delete_many({})
    await db.roadmap_levels.delete_many({})
    await db.industry_insights.delete_many({})
    
    await db.skills.insert_many(skills_data)
    await db.courses.insert_many(courses_data)
    await db.projects.insert_many(projects_data)
    await db.roles.insert_many(roles_data)
    await db.roadmap_levels.insert_many(roadmap_data)
    await db.industry_insights.insert_many(industry_data)

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
