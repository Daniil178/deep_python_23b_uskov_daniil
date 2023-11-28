#include <Python.h>

#include "loads.c"
#include "dumps.c"


static PyMethodDef cjson_methods[] = {
    {"loads", cjson_loads, METH_VARARGS, "Load json in str format and create dictionary"},
    {"dumps", cjson_dumps, METH_VARARGS, "transform dictionary to str"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef cjson_module = {
    PyModuleDef_HEAD_INIT,
    "cjson",
    NULL,
    -1,
    cjson_methods
};

PyMODINIT_FUNC PyInit_cjson(void) {
    return PyModule_Create(&cjson_module);
}
