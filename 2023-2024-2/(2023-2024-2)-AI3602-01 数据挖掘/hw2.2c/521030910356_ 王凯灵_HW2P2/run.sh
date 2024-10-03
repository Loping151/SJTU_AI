# NOTE: You might need to change the source path according to your workdir
TUGRAPH_DIR=/root/tugraph-db/build/output
P2_DIR=/root/ai3602/p2_CommunityDetection
if [ ! -d "$P2_DIR" ]; then
    # this is my workspace, and I'm not willing to change it
    P2_DIR=/root/workspace/p2_CommunityDetection
fi
echo "Using P2_DIR at: $P2_DIR"

cd ${TUGRAPH_DIR}

# whatever, remove it.
rm -f ./p2_main.py
ln -s ${P2_DIR}/p2_main.py ./p2_main.py

# run p2_main.py under TUGRAPH_DIR
python p2_main.py --base_path ${P2_DIR}

# return to the original directory
cd ${P2_DIR}
