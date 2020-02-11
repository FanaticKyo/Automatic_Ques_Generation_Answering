# Ubuntu Linux as the base imag
FROM python:3.7
# FROM java:8-jdk
# CMD ["/bin/bash"]
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# ENV JAVA_VER 8
# ENV JAVA_HOME /usr/lib/jvm/java-8-oracle/jre/bin/java
# Add the files
ADD . /QA

WORKDIR /QA
# Install packages 
RUN apt-get -y update && \
    apt-get -y upgrade && \
	apt-get -y install ant && \
	apt-get -y install git && \
	apt-get -y install wget && \
	apt-get -y install unzip && \
	pip3 install fuzzywuzzy[speedup] && \
	pip3 install textblob && \
	python3 -m textblob.download_corpora && \
	pip3 install -U nltk && \
	pip3 install scikit-learn && \
	pip3 install pyopenssl && \
	# export REL_DATE="2018-10-05" && \
	# unzip stanford-corenlp-full-${REL_DATE}.zip && \
	# mv stanford-corenlp-full-${REL_DATE} CoreNLP && \
	git clone https://github.com/explosion/spaCy && \
	cd spaCy && \
	export PYTHONPATH=`pwd` && \
	pip3 install -r requirements.txt && \
	python3 setup.py build_ext --inplace && \
	python3 -m spacy download en_core_web_lg && \
	python3 -m spacy download en_core_web_sm && \
	cd .. && \
	pip3 install spacy-transformers && \
	git clone https://github.com/huggingface/neuralcoref.git && \
	cd neuralcoref && \
	pip3 install -e . && \
	cd ..

CMD ["chmod 777 ask"]
CMD ["chmod 777 answer"]
RUN python3 requirement.py

# ENV PORT 9000
# EXPOSE 9000
# ENTRYPOINT ["./start.sh"]
# ENTRYPOINT ["/bin/bash", "-c"]