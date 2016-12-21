#ifndef __COMPUTATION_H__
#define __COMPUTATION_H__

#include <pthread.h>
#include "thread_pool.h"

typedef void (*OnComputationComplete)(void*);

struct Computation {
    void (*f)(void*);
    void* arg;
    
    pthread_mutex_t guard;
    pthread_cond_t finished_cond;
    bool finished;
    struct Task task;
    OnComputationComplete on_complete;
    void* on_complete_arg;
    // Любые поля на ваше усмотрение.
};


// Отправляет вычисление в очередь thread pool. Функция
// on_complete будет вызвана с параметром on_complete_arg,
// как только вычисление будет завершено функцией
// thpool_complete_computation.
void thpool_submit_computation(
    struct ThreadPool *pool,
    struct Computation *computation,
    OnComputationComplete on_complete,
    void* on_complete_arg
);


// Помечает вычисление как “завершённое с учётом подзадач” и
// вызывает функцию on_complete, которая была передана в
// thpool_submit_computation. Такая функция on_complete,
// которая вызывается как реакция на некоторое событие,
// называется “callback”.
void thpool_complete_computation(struct Computation *computation);


// Блокируется, пока вычислительная задача не завершена,
// освобождает выделенные в thpool_submit_computation ресурсы.
void thpool_wait_computation(struct Computation *computation);

#endif
