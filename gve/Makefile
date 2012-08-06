all: plan.h
	g++ -O2 -mssse3 gve.cpp

plan.h: gen_plan.py
	python gen_plan.py

run:
	./a.out

clean:
	rm -f *~ a.out plan.h
