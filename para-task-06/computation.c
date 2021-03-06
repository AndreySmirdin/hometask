#include <pthread.h>
#include "computation.h"
#include <stdio.h>
#include <stdlib.h>

void thpool_submit_computation(struct ThreadPool *pool,
    						   struct Computation *computation,
    						   OnComputationComplete on_complete,
    						   void* on_complete_arg){

	computation->task.f = computation->f;
	computation->task.arg = computation->arg;
    computation->finished = false;

    pthread_mutex_init(&computation->guard, NULL);
    pthread_cond_init(&computation->finished_cond, NULL);

	computation->on_complete = on_complete;
	computation->on_complete_arg = on_complete_arg;

	thpool_submit(pool, &computation->task);
}


void thpool_complete_computation(struct Computation *computation){
    pthread_mutex_lock(&computation->guard);
    computation->finished = true;
    pthread_cond_signal(&computation->finished_cond);
    pthread_mutex_unlock(&computation->guard);

    if (computation->on_complete)
        (computation->on_complete)(computation->on_complete_arg);
}


void thpool_wait_computation(struct Computation *computation){
	pthread_mutex_lock(&computation->guard);
    while (!computation->finished) {
        pthread_cond_wait(&computation->finished_cond, &computation->guard);
    }
    pthread_mutex_unlock(&computation->guard);

    pthread_cond_destroy(&computation->finished_cond);
    pthread_mutex_destroy(&computation->guard);

    thpool_wait(&computation->task);
}




