#include "microops.h"
PyObject* micro_floor_div(PyObject* a, PyObject* b) { 
    return PyNumber_FloorDivide(a, b); 
}
