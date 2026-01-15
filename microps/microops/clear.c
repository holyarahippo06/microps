#include "microops.h"
PyObject* micro_clear(PyObject* container) {
    if (PyList_Check(container)) {
        PyList_SetSlice(container, 0, PyList_Size(container), NULL);
    } else if (PyDict_Check(container)) {
        PyDict_Clear(container);
    }
    Py_RETURN_NONE;
}
