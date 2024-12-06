# GeoGenSolver: Generative Illustration and Solver for Vietnamese Geometric Problem
# Link to Huggingface Space
[GeoGenSolver](https://hugovoxx-geogensolve.hf.space)
# Requirements
Linux or Windows WSL with Python 3.10
# Setup
## Clone this Repo
```
git clone https://github.com/HugoVox/GeoGenSolver.git
cd GeoGenSolver
```
## Install necessary Linux packages
Depending on the exact Linux distribution/version, you may need to install these packages if they are not already installed.
```
sudo apt update
sudo apt install python3-virtualenv
sudo apt install python3-tk
```
## Install Python module dependencies
Create a virtual env `pyenv` for GeoGenSolver
```
virtualenv -p python3 pyenv
. pyenv/bin/activate
pip install --require-hashes --no-deps -r pre-requirements.txt
pip install --no-deps -r requirements.txt
```
**Note** It is important to install the requirements in the instructed order and templates.
## Run
### Run GUI
```
python app.py
```
Then go to `http://127.0.0.1:7860` to use.
### Run from terminal
For example we have the following geometric problem: `Cho tam giác cân ABC (AB = AC), các đường cao AD, BE, cắt nhau tại H. Gọi O là tâm đường tròn ngoại tiếp tam giác AHE. Chứng minh rằng: Bốn điểm A, E, D, B cùng nằm trên một đường tròn.`, here is how to run:
```
python main.py --question "Cho tam giác cân ABC (AB = AC), các đường cao AD, BE, cắt nhau tại H. Gọi O là tâm đường tròn ngoại tiếp tam giác AHE. Chứng minh rằng: Bốn điểm A, E, D, B cùng nằm trên một đường tròn."
```
We implement both Gemma2 and GPT 4o. Default is GPT 4o.
```
# If you want to use Gemma2
python main.py --model "gemma2-9b-it" --question <input question here>
```
# Issue Log
**Error:** Running main.py returns `Permission Denied`

**Solution:** Run the following command: `chmod +x ag4masses/utils/run.sh`. Then rerun.
