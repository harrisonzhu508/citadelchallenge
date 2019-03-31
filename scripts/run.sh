#!bin/bash
python3 dkl.py > dkl.txt
python3 spatiotemporal_classify.py > spatiotemporal_classify.txt
python3 kriging.py > kriging.txt