import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask Configuration
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # Gemini API Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL_NAME = os.getenv('GEMINI_MODEL_NAME', 'gemini-1.5-flash')
    
    # Offline NLP Configuration
    OFFLINE_NLP_ENABLED = os.getenv('OFFLINE_NLP_ENABLED', 'true').lower() == 'true'
    SPACY_MODEL = os.getenv('SPACY_MODEL', 'en_core_web_sm')
    
    # Pretrained Queries
    PRETRAINED_QUERIES = {
        'hello': "Hello! I'm PyTutor, your Python programming assistant. How can I help you today?",
        'help': "I can help with:\n- Python concepts\n- Code debugging\n- Error explanations\n- Code generation",
        'basics': "Python basics include:\n1. Variables\n2. Data types\n3. Control structures\n4. Functions\n5. Modules",
        'function': "To create a function:\n```python\ndef function_name(parameters):\n    # Function body\n    return value\n```",
        'loop': "Python has:\n1. `for` loops:\n```python\nfor item in sequence:\n    # Code block\n```\n2. `while` loops:\n```python\nwhile condition:\n    # Code block\n```"
    }
    
    # Application Settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size
    SESSION_COOKIE_NAME = 'pytutor_session'
    
    @classmethod
    def validate_config(cls):
        """Validate required configuration"""
        if not cls.GEMINI_API_KEY and cls.OFFLINE_NLP_ENABLED is False:
            raise ValueError("Either GEMINI_API_KEY must be set or OFFLINE_NLP_ENABLED must be True")
