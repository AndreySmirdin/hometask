cmake_minimum_required(VERSION 3.6)
project(para_task_06)

set(CMAKE_CXX_COMPILER  "clang")

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -Wextra ")
set(CMAKE_C_FLAGS_DEBUG  "${CMAKE_C_FLAGS_DEBUG} -Wall -Wextra  -fsanitize=thread")
set(SOURCE_FILES
    computation.c
    computation.h
    linkedlist.c
    linkedlist.h
    main.c
    queue.c
    queue.h
    squeue.c
    squeue.h
    thread_pool.c
    thread_pool.h
    wsqueue.c
    wsqueue.h)

find_package(Threads)
add_executable(para_task_06 ${SOURCE_FILES})
target_link_libraries(${PROJECT_NAME} ${CMAKE_THREAD_LIBS_INIT})