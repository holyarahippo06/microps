#include "microops.h"
PyObject* micro_filter_func(PyObject* func, PyObject* iterable) {
    PyObject* result = PyList_New(0);
    PyObject* iter = PyObject_GetIter(iterable);
    if (!iter) return NULL;
    PyObject* item;
    while ((item = PyIter_Next(iter))) {
        PyObject* keep = PyObject_CallFunctionObjArgs(func, item, NULL);
        if (!keep) {
            Py_DECREF(item);
            Py_DECREF(iter);
            Py_DECREF(result);
            return NULL;
        }
        if (PyObject_IsTrue(keep)) {
            PyList_Append(result, item);
        }
        Py_DECREF(keep);
        Py_DECREF(item);
    }
    Py_DECREF(iter);
    return result;
}
