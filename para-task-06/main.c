#include <stdio.h>
#include "computation.h"
#include <stdlib.h>

pthread_mutex_t done_mutex;
pthread_cond_t cond_exit;
struct ThreadPool pool;
struct Computation* c1;
struct Computation* c2;

void foo1_complete() {
  printf("Hurray!");
}

void foo2_complete() {
  	printf("wow");
}

void foo2(){
	thpool_complete_computation(&c2);
}

void foo1() {
	printf("foo1 \n");
    c2 = malloc(sizeof(struct Computation));
	c2->finished = false;
	c2->f = (void*)foo2;
	c2->arg = NULL;
	thpool_submit_computation(&pool, &c2, foo2_complete, NULL); 
}




int main(){
	printf("lets start");
    thpool_init(&pool, 2);
    c1 = malloc(sizeof(struct Computation));
	c1->finished = false;
	c1->f = (void*)foo1;
	c1->arg = NULL;
	thpool_submit_computation(&pool, &c1, foo1_complete, NULL);
	thpool_wait_computation(&c1);
}

