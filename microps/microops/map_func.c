#include "microops.h"
PyObject* micro_map_func(PyObject* func, PyObject* iterable) {
    PyObject* result = PyList_New(0);
    PyObject* iter = PyObject_GetIter(iterable);
    if (!iter) return NULL;
    PyObject* item;
    while ((item = PyIter_Next(iter))) {
        PyObject* mapped = PyObject_CallFunctionObjArgs(func, item, NULL);
        Py_DECREF(item);
        if (!mapped) {
            Py_DECREF(iter);
            Py_DECREF(result);
            return NULL;
        }
        PyList_Append(result, mapped);
        Py_DECREF(mapped);
    }
    Py_DECREF(iter);
    return result;
}
