from groq import Groq
from openai import OpenAI
import os
import regex as re
class Reader:
    def __init__(self, model:str):
        self.model_name = model
        if model == 'gemma2-9b-it':
            self.client = Groq()
        elif model == 'gpt-4o-mini':
            token = os.environ["GITHUB_TOKEN"]
            endpoint = "https://models.inference.ai.azure.com"
            self.client = OpenAI(base_url=endpoint,api_key=token)
        self.prompt = None
    def get_prompt(self) -> str:
        """
        Get the prompt from the prompt.txt file
        """
        with open('prompt.txt', 'r', encoding='utf-8') as f:
            self.prompt = f.read()
    def refine(self, input:str) -> str:
        """
        Refine the input
        """
        fix = re.sub(r'[;]\s*[?]\s*', ' ? ', input)
        clean = re.sub(r'\s+', ' ', fix)
        return clean
    def reader(self, input: str) -> str:
        """
        Generate a response from the input
        Args:
            input (str): Math question from the user

        Returns:
            str: The generated response
        """

        chat_completion = self.client.chat.completions.create(
            messages=[
                { "role": "system", "content": self.prompt},
                { "role": "user", "content": input,}
            ],
            model=self.model_name,
            temperature=0.5,
            max_tokens=2048,
            top_p=1.0,
            stop=None,
            stream=False,
            )
        return self.refine(chat_completion.choices[0].message.content)
    def write_output(self, output:str):
        """
        Write the output to the output.txt file
        """
        with open('ag4mout/output.txt', 'w', encoding='utf-8') as f:
            f.write("Output\n")
            f.write(output.strip())
    def main(self, input:str) -> str:
        self.get_prompt()
        result = self.reader(input)
        self.write_output(result)
