@echo off
conda create -n dl2023 python=3.9
call conda activate dl2023
pip install -r requirements.txt
python main.py --config config/default.json
