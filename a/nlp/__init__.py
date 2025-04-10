from .offline_processor import OfflineProcessor
from .pretrained_queries import get_pretrained_response

# Initialize the NLP components when package is imported
try:
    offline_processor = OfflineProcessor()
except Exception as e:
    print(f"Warning: Could not initialize offline processor - {str(e)}")
    offline_processor = None

__all__ = [
    'OfflineProcessor',
    'get_pretrained_response',
    'offline_processor'
]

# Package version
__version__ = '1.0.0'
