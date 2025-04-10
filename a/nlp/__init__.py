from .pretrained_queries import get_pretrained_response
from config import Config
import logging

logger = logging.getLogger(__name__)

# Initialize the NLP components when package is imported
try:
    # Only import OfflineProcessor if offline NLP is enabled
    if Config.OFFLINE_NLP_ENABLED:
        from .offline_processor import OfflineProcessor
        try:
            offline_processor = OfflineProcessor()
        except Exception as e:
            logger.warning(f"Could not initialize offline processor - {str(e)}")
            logger.warning("Make sure to install spaCy and the required model with: python -m spacy download en_core_web_sm")
            offline_processor = None
    else:
        offline_processor = None
except ImportError:
    logger.warning("OfflineProcessor could not be imported")
    offline_processor = None

__all__ = [
    'get_pretrained_response',
    'offline_processor'
]

# Package version
__version__ = '1.0.0'
