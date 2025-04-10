from flask import Flask, request, jsonify, render_template
from config import Config
import google.generativeai as genai
from nlp import offline_processor, get_pretrained_response
import logging
from datetime import datetime

# Initialize configuration
Config.validate_config()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Gemini
if Config.GEMINI_API_KEY:
    genai.configure(api_key=Config.GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel(Config.GEMINI_MODEL_NAME)
else:
    gemini_model = None
    logger.warning("Gemini API key not configured, running in offline mode only")

# System prompt template
SYSTEM_PROMPT = """
You are PyTutor, an expert Python programming tutor with these capabilities:
1. Teaching Python concepts from basics to advanced
2. Debugging and error explanation
3. Code generation with examples
4. Best practices guidance

Guidelines:
- Format code with Markdown
- Explain concepts clearly
- Provide practical examples
- Adapt to user's skill level
- Be concise but thorough
"""

@app.route('/')
def home():
    """Render the main chat interface"""
    return render_template('index.html', 
                         offline_mode=not bool(Config.GEMINI_API_KEY))

@app.route('/about')
def about():
    """Render the about page"""
    return render_template('about.html')

@app.route('/chat', methods=['POST'])
def handle_chat():
    """Handle chat messages with hybrid offline/online processing"""
    start_time = datetime.now()
    user_message = request.json.get('message', '').strip().lower()
    
    if not user_message:
        return jsonify({'error': 'Empty message'}), 400
    
    logger.info(f"Processing message: {user_message[:50]}...")
    
    # 1. Check pretrained responses
    pretrained_response = get_pretrained_response(user_message)
    if pretrained_response:
        logger.info("Served from pretrained queries")
        return jsonify({
            'response': pretrained_response,
            'source': 'local',
            'processing_time': (datetime.now() - start_time).total_seconds()
        })
    
    # 2. Try offline processing
    if Config.OFFLINE_NLP_ENABLED and offline_processor:
        offline_response = offline_processor.process(user_message)
        if offline_response:
            logger.info("Served from offline processor")
            return jsonify({
                'response': offline_response,
                'source': 'local',
                'processing_time': (datetime.now() - start_time).total_seconds()
            })
    
    # 3. Fall back to Gemini
    if gemini_model:
        try:
            chat_session = gemini_model.start_chat(history=[
                {"role": "user", "parts": [SYSTEM_PROMPT]},
                {"role": "model", "parts": ["I'm ready to help with Python!"]}
            ])
            
            response = chat_session.send_message(user_message)
            logger.info("Served from Gemini API")
            
            return jsonify({
                'response': response.text,
                'source': 'gemini',
                'processing_time': (datetime.now() - start_time).total_seconds()
            })
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            return jsonify({
                'error': f"API Error: {str(e)}",
                'fallback': True
            }), 500
    
    # 4. Final fallback if no options available
    return jsonify({
        'response': "I'm currently unable to process your request. Please try again later.",
        'source': 'system'
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=(Config.FLASK_ENV == 'development')
    )
