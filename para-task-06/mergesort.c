#include <stdlib.h>
#include "computation.h"
int *tmp;

struct Args{
    int l, r;
    int *arr, *tmp;
    struct ThreadPool *pool;
};

void sort(struct Computation* c, int l, int r, int* arr){
    if (r - l <= 1){
        c->finished = true;
        return;
    }
    struct Computation left, right;
    int m = (l + r) / 2;
    left.f = sort;
    left.arg = (void*) fill_args(c->pool, l, r, arr);
    right.f = sort;
    right.arg = (void*) fill_args(pool, m, r, arr);
    thpool_submit_computation(pool, &left, merge_arr, (void*) fill_args(pool, l, m, arr));
    thpool_submit_computation(pool, &right, merge_arr, (void*) fill_args(pool, m, r, arr));
    thpool_wait_computation(&left);
    thpool_wait_computation(&right);
}

void mergesort(struct ThreadPool *pool, int *arr, int n){
    tmp = malloc(sizeof(int) * n);
    struct Computation first;
    first.f = sort;
    first.arg = (void*) fill_args(pool, 0, n, arr);
    thpool_submit_computation(pool, &first, merge_arr, (void*) fill_args(pool, 0, n, arr));
    thpool_wait_computation(&first);
}

struct Args* fill_args(struct ThreadPool *pool, int l, int r, int *arr){
    struct Args *args = malloc(sizeof(struct Args));
    args->l = l;
    args->r = r;
    args->arr = arr;
    args->tmp = tmp;
    args->pool = pool;
    return args;
}



void merge_arr(struct ThreadPool *pool, int l, int r, int *arr) {
    // Merges sorted [l, m) and [m, r) into [l, r)
    int m = (l + r) / 2;
    int p1 = l, p2 = m;
    for (int ptr = l; ptr < r; ptr++) {
        if (p1 < m && (p2 >= r || arr[p1] <= arr[p2])) {
            tmp[ptr] = arr[p1++];
        } else {
            tmp[ptr] = arr[p2++];
        }
    }
    for (int ptr = l; ptr < r; ptr++) {
        arr[ptr] = tmp[ptr];
    }
}