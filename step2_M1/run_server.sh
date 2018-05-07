#!/bin/sh

# Run server of standford corenlp
# Author : SABLAYROLLES Louis
# Date : 07 / 05 / 17

# Run server of standford corenlp

cd ../../corenlp/
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -annotators "tokenize,ssplit,pos,lemma,parse,sentiment" -port 9000 -timeout 30000 
