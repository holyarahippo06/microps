#include "microops.h"
PyObject* micro_extend(PyObject* list, PyObject* iterable) {
    if (PyList_Check(list)) {
        PyObject* iter = PyObject_GetIter(iterable);
        if (!iter) return NULL;
        PyObject* item;
        while ((item = PyIter_Next(iter))) {
            PyList_Append(list, item);
            Py_DECREF(item);
        }
        Py_DECREF(iter);
    }
    Py_RETURN_NONE;
}
