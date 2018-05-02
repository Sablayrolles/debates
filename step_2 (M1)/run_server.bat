@echo off

cd C:\Users\louis\Desktop\stage\step_2 (M1)\corenlp
java -mx1405m -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -annotators "tokenize,ssplit,pos,lemma,parse,sentiment" -port 9000 -timeout 30000
pause