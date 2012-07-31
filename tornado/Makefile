prepare:
	tar xvfz tornado-2.3.tar.gz
	cp -R tornado-2.3/tornado tornado
	cp *.py tornado

clean:
	rm -rf tornado tornado-2.3
	rm -f *~
	rm -f *.pyc

run:
	python helloworld.py --log_file_prefix=./access.log
	#pypy helloworld.py --log_file_prefix=./access.log
