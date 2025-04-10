import spacy
from spacy.matcher import PhraseMatcher
from config import Config

class OfflineProcessor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.matcher = PhraseMatcher(self.nlp.vocab)
        self.setup_patterns()
    
    def setup_patterns(self):
        patterns = [
            "how to create a function",
            "what is a loop",
            "explain lists",
            "python dictionary example",
            "debug my code"
        ]
        phrase_patterns = [self.nlp(text) for text in patterns]
        self.matcher.add("PYTHON_PATTERNS", phrase_patterns)
    
    def process(self, text):
        doc = self.nlp(text.lower())
        matches = self.matcher(doc)
        
        if matches:
            return self.get_offline_response(text)
        return None
    
    def get_offline_response(self, query):
        responses = {
            "function": "To create a function:\n\n```python\ndef function_name(parameters):\n    # Function body\n    return value\n```",
            "loop": "Python has:\n1. `for` loops:\n```python\nfor item in sequence:\n    # Code block\n```\n2. `while` loops:\n```python\nwhile condition:\n    # Code block\n```",
            "lists": "Lists are ordered collections:\n```python\nmy_list = [1, 2, 3]\nmy_list.append(4)\n```",
            "dictionary": "Dictionaries store key-value pairs:\n```python\nmy_dict = {'key': 'value'}\nprint(my_dict['key'])\n```",
            "debug": "Common debugging steps:\n1. Check error messages\n2. Print variable values\n3. Use try-except blocks\n4. Step through code with debugger"
        }
        
        query = query.lower()
        if "function" in query:
            return responses["function"]
        elif "loop" in query:
            return responses["loop"]
        elif "list" in query:
            return responses["lists"]
        elif "diction" in query:
            return responses["dictionary"]
        elif "debug" in query:
            return responses["debug"]
        
        return None
