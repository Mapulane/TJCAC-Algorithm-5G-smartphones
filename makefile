CC=g++
CK=-c -std=c++11

driver: markov.o
	$(CC) markov.o -o driver

markov.o: markov.cpp rats.h
	$(CC) markov.cpp -c

run:
	./driver


clean:
	@rm -f *.o
	@rm driver
