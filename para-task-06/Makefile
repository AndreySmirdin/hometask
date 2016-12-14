all: bin main
bin:
	mkdir -p bin 
main: bin/main.o bin/computation.o bin/thread_pool.o bin/wsqueue.o bin/squeue.o bin/queue.o bin/linkedlist.o
	gcc bin/main.o bin/computation.o bin/thread_pool.o bin/wsqueue.o bin/squeue.o bin/queue.o bin/linkedlist.o  -pthread -o main

bin/main.o: main.c computation.h
	gcc -c main.c -o bin/main.o

bin/computation.o: computation.c computation.h
	gcc -c computation.c -o bin/computation.o
	
bin/thread_pool.o: thread_pool.c thread_pool.h
	gcc -c thread_pool.c -o bin/thread_pool.o
	
bin/wsqueue.o: wsqueue.c wsqueue.h
	gcc -c wsqueue.c -o bin/wsqueue.o
	
bin/squeue.o: squeue.c squeue.h
	gcc -c squeue.c -o bin/squeue.o
	
bin/queue.o: queue.c queue.h
	gcc -c queue.c -o bin/queue.o
	
bin/linkedlist.o: linkedlist.c linkedlist.h
	gcc -c linkedlist.c -o bin/linkedlist.o
clean:
	rm -rf bin
