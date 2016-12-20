#include <stdio.h>
#include "computation.h"
#include <stdlib.h>

pthread_mutex_t done_mutex;
pthread_cond_t cond_exit;
struct ThreadPool pool;
struct Computation c1;
struct Computation c2;

void foo1_complete(void* arg) {
	printf("foo1_complete \n");
}

void foo2_complete(void* arg) {
  	printf("foo2_complete \n");
	thpool_complete_computation(&c1);
}

void foo2(void* arg){
	printf("foo2 \n");
	
	thpool_complete_computation(&c2);

}

void foo1(void* arg) {
	printf("foo1 \n");
	c2.f = foo2;
	c2.arg = NULL;
	thpool_submit_computation(&pool, &c2, foo2_complete, NULL);
}




int main(){
	printf("lets start \n");
    thpool_init(&pool, 2);
	c1.f = foo1;
	c1.arg = NULL;
	thpool_submit_computation(&pool, &c1, foo1_complete, NULL);
	thpool_wait_computation(&c1);
	thpool_finit(&pool);
    return 0;
}

