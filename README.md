# PDF Question Generator

This project automatically generates multiple-choice questions from PDF content using OpenAI's GPT models. It can read PDF files, extract text, generate questions based on the content, and verify the quality of the generated questions.

## Features

- **PDF Text Extraction**: Extract text from PDF files
- **Question Generation**: Generate multiple-choice questions from the extracted text
- **Content Translation**: Translate content if needed
- **Question Verification**: Verify the quality and accuracy of generated questions
- **Result Storage**: Save generated questions and verification results to a file

## Installation

1. Clone this repository
2. Install the required packages:
```bash
pip install -r requirements.txt
```
3. Create a `.env` file in the project root directory with your OpenAI API key:
