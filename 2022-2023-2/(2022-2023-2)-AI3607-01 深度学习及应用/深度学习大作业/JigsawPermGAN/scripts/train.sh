#!/bin/bash

source activate dl2023
python main.py --config config/default.json
python main.py --config config/base.json
python main.py --config config/pretrain.json
python main.py --config config/with_edge_loss.json
python main.py --config config/with_discriminator.json
python main.py --config config/with_both.json
python main.py --config config/no_encode.json