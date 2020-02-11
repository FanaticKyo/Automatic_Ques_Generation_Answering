# Automatic_Ques_Generation_Answering

1.Question generation

The ask program have the following command-line interface:

./ask article.txt nquestions

Where:

article.txt is a path to an arbitrary plain text file (the document) nquestions is an integer (the number of questions to be generated).

2.Question answering

The answer program have the following command-line interface:

./answer article.txt questions.txt

Where:

article.txt is a path to an arbitrary plain text file (the document) questions.txt is a path to an arbitrary file of questions (one question per line with no extraneous material).

#### To watch the description about the system, please visit: https://www.youtube.com/watch?v=M4sZqee2yX8&t=7s

#### We also built a docker image for the system, and we recommend you run in this way as it's faster and simpler.

To run the system using docker, please use command: docker pull fanatickyo/nlpproject
