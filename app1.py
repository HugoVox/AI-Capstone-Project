from flask import Flask, render_template, request, url_for
from reader import Reader
from utils import *
import shutil
from pathlib import Path
from typing import Union


OUTPUT_FOLDER = 'ag4mout'

def geogeosolver(question:str, model:str="gemma2-9b-it"):
    if model == 'gpt-4o-mini':
        get_github_token()
    elif model == 'gemma2-9b-it':
        get_grog_api()
    reader = Reader(model=model)
    input = translate(question)
    reader.main(input)
    run_ag()
    if os.path.exists(f'{OUTPUT_FOLDER}/output.png'):
        image_path = f'{OUTPUT_FOLDER}/output.png'
    else:
        image_path = f'{OUTPUT_FOLDER}/error.png'
    result_dict = read_solution()
    key_list = list(result_dict.keys())
    premises = result_dict[key_list[0]]
    constructions = result_dict[key_list[1]]
    steps = result_dict[key_list[2]]
    return image_path, premises, constructions, steps

def clear_directory(directory_path: Union[str, Path] = 'static/ag4mout') -> None:
    """Irreversibly removes all files and folders inside the specified
    directory. Returns a list with paths Python lacks permission to delete."""
    # erroneous_paths = []
    for path_object in Path(directory_path).iterdir():
        try:
            if path_object.is_dir():
                shutil.rmtree(path_object)
            elif path_object.name != 'error.png':
                path_object.unlink()
        except PermissionError:
            pass
            # erroneous_paths.append(path_object)

def clear_static_directory(directory_path: Union[str, Path] = OUTPUT_FOLDER) -> None:
    """Irreversibly removes all files and folders inside the specified
    directory. Returns a list with paths Python lacks permission to delete."""
    # erroneous_paths = []
    for path_object in Path(directory_path).iterdir():
        try:
            if path_object.is_dir():
                shutil.rmtree(path_object)
            elif path_object.name != 'error.png':
                path_object.unlink()
        except PermissionError:
            pass
            # erroneous_paths.append(path_object)

app1 = Flask(__name__)

@app1.route('/', methods=['GET'])
def main():
    return render_template('index.html')

@app1.route('/',methods=["GET","POST"])
def predict():
    clear_directory()
    clear_static_directory()
    problem = request.form.get("problem")
    image, premises, constructions, step = geogeosolver(problem)
    try:
        shutil.copy2('ag4mout/output.png','static/ag4mout')
        image = "../static/" + image
    except:
        image = "../static/ag4mout/error.png    
    return render_template('index.html', image = image, premises = premises, constructions=constructions, step = step)


if __name__ == '__main__':
    app1.run(port=7860, debug=True)
    clear_directory()
    clear_static_directory()
    
os.getenv
