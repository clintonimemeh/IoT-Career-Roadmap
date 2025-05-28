import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const App = () => {
  const [roadmapData, setRoadmapData] = useState([]);
  const [selectedLevel, setSelectedLevel] = useState(null);
  const [levelDetails, setLevelDetails] = useState(null);
  const [industryInsights, setIndustryInsights] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('roadmap');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [roadmapRes, insightsRes] = await Promise.all([
        axios.get(`${API}/roadmap`),
        axios.get(`${API}/industry-insights`)
      ]);
      setRoadmapData(roadmapRes.data);
      setIndustryInsights(insightsRes.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  };

  const fetchLevelDetails = async (levelId) => {
    try {
      const response = await axios.get(`${API}/roadmap/level/${levelId}`);
      setLevelDetails(response.data);
      setSelectedLevel(levelId);
    } catch (error) {
      console.error('Error fetching level details:', error);
    }
  };

  const getLevelColor = (difficulty) => {
    switch (difficulty) {
      case 'beginner': return 'from-green-400 to-green-600';
      case 'intermediate': return 'from-blue-400 to-blue-600';
      case 'advanced': return 'from-purple-400 to-purple-600';
      case 'expert': return 'from-red-400 to-red-600';
      default: return 'from-gray-400 to-gray-600';
    }
  };

  const getDifficultyIcon = (difficulty) => {
    switch (difficulty) {
      case 'beginner': return '🌱';
      case 'intermediate': return '🚀';
      case 'advanced': return '⚡';
      case 'expert': return '👑';
      default: return '📚';
    }
  };

  const VisualRoadmap = () => (
    <div className="relative">
      {/* Header */}
      <div className="text-center mb-12">
        <h1 className="text-4xl md:text-6xl font-bold text-white mb-4">
          IoT Professional Roadmap
        </h1>
        <p className="text-xl text-gray-300 max-w-3xl mx-auto">
          Your comprehensive guide to becoming an IoT expert - from foundation to leadership
        </p>
      </div>

      {/* Roadmap Path */}
      <div className="relative max-w-6xl mx-auto">
        {/* Connection Line */}
        <div className="absolute left-1/2 transform -translate-x-1/2 w-1 h-full bg-gradient-to-b from-green-400 via-blue-400 via-purple-400 to-red-400 rounded-full"></div>
        
        {roadmapData.map((level, index) => (
          <div
            key={level.id}
            className={`relative flex items-center mb-16 ${
              index % 2 === 0 ? 'justify-start' : 'justify-end'
            }`}
          >
            {/* Level Card */}
            <div
              className={`relative w-80 md:w-96 cursor-pointer transform hover:scale-105 transition-all duration-300 ${
                index % 2 === 0 ? 'mr-auto' : 'ml-auto'
              }`}
              onClick={() => fetchLevelDetails(level.id)}
            >
              <div className={`bg-gradient-to-r ${getLevelColor(level.difficulty_level)} p-6 rounded-2xl shadow-2xl border border-white/20`}>
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center space-x-3">
                    <span className="text-3xl">{getDifficultyIcon(level.difficulty_level)}</span>
                    <div>
                      <h3 className="text-2xl font-bold text-white">Level {level.level_number}</h3>
                      <p className="text-white/80 capitalize">{level.difficulty_level}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-white/80 text-sm">Duration</p>
                    <p className="text-white font-semibold">{level.estimated_duration_months} months</p>
                  </div>
                </div>
                
                <h4 className="text-xl font-bold text-white mb-2">{level.title}</h4>
                <p className="text-white/90 mb-4">{level.description}</p>
                
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="text-white/70">Skills to Develop</p>
                    <p className="text-white font-semibold">{level.skills_to_develop.length} skills</p>
                  </div>
                  <div>
                    <p className="text-white/70">Projects</p>
                    <p className="text-white font-semibold">{level.projects_to_complete.length} projects</p>
                  </div>
                </div>
                
                <div className="mt-4 flex flex-wrap gap-2">
                  {level.specialization_paths.map((path, idx) => (
                    <span key={idx} className="px-2 py-1 bg-white/20 rounded-full text-xs text-white">
                      {path.replace('_', ' ').toUpperCase()}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            {/* Level Number Circle */}
            <div className={`absolute left-1/2 transform -translate-x-1/2 w-12 h-12 bg-white rounded-full flex items-center justify-center shadow-lg z-10 border-4 ${
              selectedLevel === level.id ? 'border-yellow-400' : 'border-gray-300'
            }`}>
              <span className="text-lg font-bold text-gray-800">{level.level_number}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const LevelDetails = () => {
    if (!levelDetails) return null;

    return (
      <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
          <div className="sticky top-0 bg-white border-b border-gray-200 p-6 flex justify-between items-center">
            <h2 className="text-3xl font-bold text-gray-800">
              {levelDetails.level.title} - Level {levelDetails.level.level_number}
            </h2>
            <button
              onClick={() => {setSelectedLevel(null); setLevelDetails(null);}}
              className="text-gray-500 hover:text-gray-700 text-2xl"
            >
              ✕
            </button>
          </div>
          
          <div className="p-6">
            <p className="text-gray-600 mb-6 text-lg">{levelDetails.level.description}</p>
            
            <div className="grid md:grid-cols-2 gap-8">
              {/* Skills */}
              <div>
                <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
                  🎯 Skills to Develop
                </h3>
                <div className="space-y-3">
                  {levelDetails.skills.map(skill => (
                    <div key={skill.id} className="bg-blue-50 p-4 rounded-lg">
                      <h4 className="font-semibold text-blue-800">{skill.name}</h4>
                      <p className="text-blue-600 text-sm">{skill.description}</p>
                      <div className="flex justify-between mt-2">
                        <span className="text-xs bg-blue-200 px-2 py-1 rounded">{skill.category}</span>
                        <span className="text-xs text-blue-600">{skill.estimated_time_hours}h</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Courses */}
              <div>
                <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
                  📚 Recommended Courses
                </h3>
                <div className="space-y-3">
                  {levelDetails.courses.map(course => (
                    <div key={course.id} className="bg-green-50 p-4 rounded-lg">
                      <h4 className="font-semibold text-green-800">{course.title}</h4>
                      <p className="text-green-600 text-sm">{course.description}</p>
                      <div className="flex justify-between mt-2">
                        <span className="text-xs text-green-600">{course.provider}</span>
                        <div className="flex space-x-2">
                          <span className="text-xs bg-green-200 px-2 py-1 rounded">{course.duration_weeks}w</span>
                          <span className="text-xs bg-green-200 px-2 py-1 rounded">{course.cost}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Projects */}
              <div>
                <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
                  🛠️ Projects to Complete
                </h3>
                <div className="space-y-3">
                  {levelDetails.projects.map(project => (
                    <div key={project.id} className="bg-purple-50 p-4 rounded-lg">
                      <h4 className="font-semibold text-purple-800">{project.title}</h4>
                      <p className="text-purple-600 text-sm">{project.description}</p>
                      <div className="flex justify-between mt-2">
                        <span className="text-xs bg-purple-200 px-2 py-1 rounded">{project.estimated_time_weeks}w</span>
                        <div className="flex flex-wrap gap-1">
                          {project.technologies_used.map((tech, idx) => (
                            <span key={idx} className="text-xs bg-purple-200 px-1 py-0.5 rounded">{tech}</span>
                          ))}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Roles */}
              <div>
                <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
                  💼 Career Opportunities
                </h3>
                <div className="space-y-3">
                  {levelDetails.roles.map(role => (
                    <div key={role.id} className="bg-orange-50 p-4 rounded-lg">
                      <h4 className="font-semibold text-orange-800">{role.title}</h4>
                      <p className="text-orange-600 text-sm">{role.description}</p>
                      <div className="flex justify-between mt-2">
                        <span className="text-xs bg-orange-200 px-2 py-1 rounded">{role.salary_range}</span>
                        <span className="text-xs bg-orange-200 px-2 py-1 rounded">{role.industry_demand} demand</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Milestones */}
            <div className="mt-8">
              <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
                🏆 Milestone Achievements
              </h3>
              <div className="grid md:grid-cols-3 gap-4">
                {levelDetails.level.milestone_achievements.map((milestone, idx) => (
                  <div key={idx} className="bg-yellow-50 p-4 rounded-lg text-center">
                    <span className="text-2xl mb-2 block">🎯</span>
                    <p className="text-yellow-800 font-semibold">{milestone}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  const IndustryInsights = () => (
    <div className="max-w-6xl mx-auto">
      <div className="text-center mb-12">
        <h2 className="text-4xl font-bold text-white mb-4">Industry Insights</h2>
        <p className="text-xl text-gray-300">Explore thriving IoT sectors and future opportunities</p>
      </div>
      
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        {industryInsights.map(insight => (
          <div key={insight.id} className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20">
            <h3 className="text-2xl font-bold text-white mb-4 capitalize">
              {insight.specialization.replace('_', ' ')}
            </h3>
            
            <div className="space-y-4">
              <div>
                <p className="text-gray-300 text-sm">Market Size</p>
                <p className="text-white font-bold text-lg">{insight.market_size}</p>
              </div>
              
              <div>
                <p className="text-gray-300 text-sm">Growth Rate</p>
                <p className="text-green-400 font-bold">{insight.growth_rate}</p>
              </div>
              
              <div>
                <p className="text-gray-300 text-sm">Average Salary</p>
                <p className="text-blue-400 font-bold">{insight.avg_salary}</p>
              </div>
              
              <div>
                <p className="text-gray-300 text-sm mb-2">Key Trends</p>
                <div className="flex flex-wrap gap-2">
                  {insight.key_trends.map((trend, idx) => (
                    <span key={idx} className="bg-blue-500/20 text-blue-300 px-2 py-1 rounded text-xs">
                      {trend}
                    </span>
                  ))}
                </div>
              </div>
              
              <div>
                <p className="text-gray-300 text-sm mb-2">Major Companies</p>
                <div className="flex flex-wrap gap-2">
                  {insight.major_companies.map((company, idx) => (
                    <span key={idx} className="bg-purple-500/20 text-purple-300 px-2 py-1 rounded text-xs">
                      {company}
                    </span>
                  ))}
                </div>
              </div>
              
              <div className="border-t border-white/20 pt-4">
                <p className="text-gray-300 text-sm mb-1">Future Outlook</p>
                <p className="text-white text-sm">{insight.future_outlook}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mb-4"></div>
          <p className="text-white text-xl">Loading IoT Roadmap...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900">
      {/* Navigation */}
      <nav className="sticky top-0 bg-black/20 backdrop-blur-sm border-b border-white/20 z-40">
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex justify-center space-x-8 py-4">
            <button
              onClick={() => setActiveTab('roadmap')}
              className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                activeTab === 'roadmap'
                  ? 'bg-blue-500 text-white'
                  : 'text-gray-300 hover:text-white hover:bg-white/10'
              }`}
            >
              📍 Visual Roadmap
            </button>
            <button
              onClick={() => setActiveTab('insights')}
              className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                activeTab === 'insights'
                  ? 'bg-blue-500 text-white'
                  : 'text-gray-300 hover:text-white hover:bg-white/10'
              }`}
            >
              📊 Industry Insights
            </button>
          </div>
        </div>
      </nav>

      {/* Content */}
      <div className="px-4 py-12">
        {activeTab === 'roadmap' && <VisualRoadmap />}
        {activeTab === 'insights' && <IndustryInsights />}
      </div>

      {/* Level Details Modal */}
      {selectedLevel && <LevelDetails />}

      {/* Footer */}
      <footer className="bg-black/20 border-t border-white/20 py-8 mt-16">
        <div className="max-w-6xl mx-auto px-4 text-center">
          <p className="text-gray-300">
            🚀 Your journey to becoming an IoT expert starts here. Click on any level to explore details.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default App;