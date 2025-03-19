from openai import OpenAI
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

class QuestionVerifier:
    def __init__(self):
        """
        Initialize the question verifier agent.
        """
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def verify_questions(self, questions, original_content):
        """
        Verifies the generated questions.
        
        Args:
            questions (list): List of questions to verify
            original_content (str): Original content from which questions were generated
            
        Returns:
            list: List containing verification results
        """
        verification_results = []
        
        for i, question in enumerate(questions):
            result = self.verify_single_question(question, original_content)
            verification_results.append(result)
            
        return verification_results
    
    def verify_single_question(self, question, original_content):
        """
        Verifies a single question.
        
        Args:
            question (dict): Question to verify
            original_content (str): Original content from which the question was generated
            
        Returns:
            dict: Verification result
        """
        # Convert the question to a readable format
        formatted_question = f"""
        QUESTION: {question['question']}
        A) {question['options']['A']}
        B) {question['options']['B']}
        C) {question['options']['C']}
        D) {question['options']['D']}
        CORRECT ANSWER: {question['correct_answer']}
        EXPLANATION: {question['explanation']}
        """
        
        prompt = f"""
        Evaluate and verify the following question:
        
        {formatted_question}
        

       ***************************
        

        """
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": "You are an expert exam creator who evaluates educational content."},
                {"role": "user", "content": f"Original Content:\n{original_content}\n\n{prompt}"}
            ]
        )
        
        verification_result = {
            "question": question,
            "verification": response.choices[0].message.content
        }
        
        return verification_result
