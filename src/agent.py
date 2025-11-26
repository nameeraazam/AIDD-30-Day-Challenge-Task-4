import os
import google.generativeai as genai
from dotenv import load_dotenv

# --- Load Environment Variables and Configure API ---
load_dotenv()

try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
except KeyError:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")
except Exception as e:
    raise RuntimeError(f"Failed to configure Gemini API: {e}")


class StudyNotesAgent:
    def __init__(self):
        # ONLY working models for your SDK version
        model_names = [
            "gemini-pro-latest"
        ]

        self.model = None

        for model_name in model_names:
            try:
                self.model = genai.GenerativeModel(model_name)
                print(f"Successfully loaded model: {model_name}")
                break
            except Exception as e:
                print(f"Failed to load {model_name}: {e}")

        if self.model is None:
            raise RuntimeError(
                "Failed to initialize any Gemini model. "
                "Update your google-generativeai library if you want access to 1.5 models."
            )

    def generate_summary(self, text: str) -> str:
        if not text:
            return "Input text is empty. Cannot generate summary."

        prompt = f"Summarize the following notes:\n\n{text}"

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"An error occurred during summarization: {e}"

    def generate_quiz(self, text: str) -> str:
        if not text:
            return "Input text is empty. Cannot generate quiz."

        prompt = f"""
        Create:
        - 2 MCQs (A, B, C, D)
        - 1 short-answer question
        Based on:
        {text}
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"An error occurred during quiz generation: {e}"


def get_agent():
    return StudyNotesAgent()
