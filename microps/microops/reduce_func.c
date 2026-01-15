#include "microops.h"
PyObject* micro_reduce_func(PyObject* func, PyObject* iterable, PyObject* initial) {
    PyObject* iter = PyObject_GetIter(iterable);
    if (!iter) return NULL;
    PyObject* accumulator = initial;
    Py_INCREF(accumulator);
    PyObject* item;
    while ((item = PyIter_Next(iter))) {
        PyObject* new_acc = PyObject_CallFunctionObjArgs(func, accumulator, item, NULL);
        Py_DECREF(accumulator);
        Py_DECREF(item);
        if (!new_acc) {
            Py_DECREF(iter);
            return NULL;
        }
        accumulator = new_acc;
    }
    Py_DECREF(iter);
    return accumulator;
}
