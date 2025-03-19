from openai import OpenAI
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

class QuestionGenerator:
    def __init__(self):
        """
        Initialize the question generator agent.
        """
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def translate_content(self, content):
        """
        Translates content to English (if necessary)
        
        Args:
            content (str): Content to be translated
            
        Returns:
            str: Translated content
        """
        response = self.client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": "You are a professional translator. Translate the given text to English."},
                {"role": "user", "content": content}
            ]
        )
        return response.choices[0].message.content
    
    def generate_questions(self, content, num_questions=5):
        """
        Generates a specified number of questions from the given content.
        
        Args:
            content (str): Content from which questions will be generated
            num_questions (int): Number of questions to generate
            
        Returns:
            list: List of generated questions
        """
        prompt = f"""
       

 {num_questions} 


{content}

Return the questions in this format:

QUESTION 1: [Question text]  
A) [Option A]  
B) [Option B]  
C) [Option C]  
D) [Option D]  
CORRECT ANSWER: [Correct option]  
EXPLANATION: [Explain why the correct answer is correct]

        
        QUESTION 2: ...
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": "****"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        return self._parse_questions(response.choices[0].message.content)
    
    def _parse_questions(self, raw_questions):
        """
        Parses the raw question text from OpenAI.
        
        Args:
            raw_questions (str): Raw question text
            
        Returns:
            list: List of question objects
        """
        questions = []
        current_question = {}
        
        lines = raw_questions.strip().split('\n')
        question_index = -1
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith("QUESTION") or line.startswith("SORU"):
                if current_question:
                    questions.append(current_question)
                current_question = {"question": line.split(":", 1)[1].strip(), "options": {}}
                question_index += 1
            elif line.startswith(("A)", "B)", "C)", "D)")):
                option_letter = line[0]
                option_text = line[2:].strip()
                if "options" in current_question:
                    current_question["options"][option_letter] = option_text
            elif line.startswith("CORRECT ANSWER:") or line.startswith("DOĞRU CEVAP:"):
                current_question["correct_answer"] = line.split(":", 1)[1].strip()
            elif line.startswith("EXPLANATION:") or line.startswith("AÇIKLAMA:"):
                current_question["explanation"] = line.split(":", 1)[1].strip()
        
        if current_question:
            questions.append(current_question)
            
        return questions
