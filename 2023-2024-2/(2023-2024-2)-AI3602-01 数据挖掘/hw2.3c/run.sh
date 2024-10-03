# NOTE: You might need to change the source path according to your workdir
TUGRAPH_DIR=/root/tugraph-db/build/output
P3_DIR=/root/ai3602/p3_LinkPrediction
if [ ! -d "$P2_DIR" ]; then
    # this is my workspace, and I'm not willing to change it
    P3_DIR=/root/workspace/p3_LinkPrediction
fi
cd ${TUGRAPH_DIR}

# check if p3_main.py exists, if not, create a symbolic link
if [ ! -f ./p3_main.py ]; then
    ln -s ${P3_DIR}/p3_main.py ./p3_main.py
fi

# run p3_main.py under TUGRAPH_DIR
python p3_main.py --epochs 5 --batch_size 256 --lr 0.01 --window_size 5 --walk_length 12 --num_neg_samples 3 --p 0.8 --q 1.2

# return to the original directory
cd ${P3_DIR}
