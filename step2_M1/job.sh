#!/bin/sh

echo "Running java corenlp"
cd ~/stageM1/corenlp/
./run.sh >~/stageM1/debates/step2\_M1/corenlp.log 2>~/stageM1/debates/step2\_M1/corenlp.err

echo "Extracting EDU"
cd ~/stageM1/debates/step2_M1/
cd dataset
python3 parse_types_annotated.py

nbFiles=$?
echo "nbFiles="$nbFiles

cd ../features
echo "Extracting infos features"
python3 saveData $a
echo "Extracting features"
python3 computeFeatures $a

cd ../learning
echo "Learning"
python3 logistic_reg.py $a
