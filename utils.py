import subprocess, os
import regex as re
from deep_translator import GoogleTranslator
def get_grog_api():
    os.environ["GROQ_API_KEY"]="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"
def get_github_token():
    os.environ['GITHUB_TOKEN'] ="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"
def translate(input:str) -> str:
    translated = GoogleTranslator(source='vi', target='en').translate(text=input)
    return translated
def run_ag():
    # if os.path.exists('ag4mout'):
    #     subprocess.run(["rm", "-rf", "ag4mout"])
    # subprocess.run(["mkdir", "ag4mout"])
    subprocess.run(["ag4masses/utils/run.sh"])
def read_solution():
    if os.path.exists('ag4mout/solution.out'):
        with open('ag4mout/solution.out', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            paragraphs = ''.join(lines).split('\n\n')
            theorem_premises = paragraphs[0].strip()
            auxiliary_constructions = paragraphs[1].strip()
            proof_steps = paragraphs[2].strip()
            proof_steps = re.sub(r'\d+\. ', '- Ta có:\n', proof_steps)
            proof_steps = re.sub(r' & ', '\n', proof_steps)
            proof_steps = re.sub(r' ⇒ ', '\n⇒ ', proof_steps)
            result = {
                theorem_premises.split('\n')[0]: GoogleTranslator(target='vi').translate(text='\n'.join(theorem_premises.split('\n')[1:])),
                auxiliary_constructions.split('\n')[0]: GoogleTranslator(target='vi').translate(text='\n'.join(auxiliary_constructions.split('\n')[1:])),
                proof_steps.split('\n')[0]: GoogleTranslator(target='vi').translate(text='\n'.join(proof_steps.split('\n')[1:]))
            }
        return result
    else:
        return {"key_1": "Bài toán không thể giải được/Đề bài bị lỗi", 
                "key_2": "Bài toán không thể giải được/Đề bài bị lỗi", 
                "key_3": "Bài toán không thể giải được/Đề bài bị lỗi",
                }