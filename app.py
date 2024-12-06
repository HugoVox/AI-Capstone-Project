import gradio as gr
from reader import Reader
from utils import *
import shutil
from pathlib import Path
from typing import Union

OUTPUT_FOLDER = 'ag4mout'

def geogeosolver(question:str, model:str="gpt-4o-mini"):
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

def clear_directory(directory_path: Union[str, Path] = OUTPUT_FOLDER) -> None:
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

if __name__ == '__main__':
    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column():
                question = gr.Textbox(lines=1, placeholder="Hãy nhập đề bài cần giải", label="Đề bài")
                solve_button = gr.Button(value="Giải")
                premises = gr.Textbox(lines=3, label="Các Giả Thuyết của Đề Bài")
                constructions = gr.Textbox(lines=3, label="Các điểm được dựng thêm")
                steps = gr.Textbox(lines=3, label="Các Bước Giải")
            with gr.Column():
                image = gr.Image(type="filepath", label="Hình Vẽ")
        solve_button.click(geogeosolver, inputs=question, outputs=[image, premises, constructions, steps]).then(clear_directory)
        example = gr.Examples(
            examples = [
            'Cho tam giác ABC nhọn, vẽ các đường cao AD, BE, CF. Gọi H là trực tâm của tam giác. Gọi M, N, P, Q lần lượt là các hình chiếu vuông góc của D lên AB, BE, CF, AC. Chứng minh: tứ giác BMND nội tiếp.',
            'Cho tam giác ABC có ba góc nhọn nội tiếp đường tròn (O). Các đường cao AD, BE, CF cắt nhau tại H và cắt đường tròn (O) lần lượt tại M,N,P. Chứng minh rằng: Tứ giác CEHD nội tiếp.',
            ],
            inputs = [question],
            )
    demo.launch()

os.getenv