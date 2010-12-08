/***************************************************************************
 *   Copyright (C) 2006 by Patrick Stinson                                 *
 *   patrickkidd@gmail.com                                                 *
 *                                                                         *
 *   Permission is hereby granted, free of charge, to any person obtaining *
 *   a copy of this software and associated documentation files (the       *
 *   "Software"), to deal in the Software without restriction, including   *
 *   without limitation the rights to use, copy, modify, merge, publish,   *
 *   distribute, sublicense, and/or sell copies of the Software, and to    *
 *   permit persons to whom the Software is furnished to do so, subject to *
 *   the following conditions:                                             *
 *                                                                         *
 *   The above copyright notice and this permission notice shall be        *
 *   included in all copies or substantial portions of the Software.       *
 *                                                                         *
 *   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,       *
 *   EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF    *
 *   MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.*
 *   IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR     *
 *   OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, *
 *   ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR *
 *   OTHER DEALINGS IN THE SOFTWARE.                                       *
 ***************************************************************************/


#include <Python.h>
#include "openGuru.h"



/* uGuru module documentation */
PyDoc_STRVAR(read_sensor_doc, 
"read_sensor(sensor)\n\
\n\
Read a sensor and return its current value.\n\
\n\
sensor must be one of the following module attributes:\n\
Root access is required to read the uGuru device.\n\
\n\
SENS_CPUTEMP\n\
SENS_SYSTEMP\n\
SENS_PWMTEMP\n\
SENS_VCORE\n\
SENS_DDRVDD\n\
SENS_DDRVTT\n\
SENS_NBVDD\n\
SENS_SBVDD\n\
SENS_HTV\n\
SENS_AGP\n\
SENS_5V\n\
SENS_3V3\n\
SENS_5VSB\n\
SENS_3VDUAL\n\
SENS_CPUFAN\n\
SENS_NBFAN\n\
SENS_SYSFAN\n\
SENS_AUXFAN1\n\
SENS_AUXFAN2");
static int uguru_detected;
typedef struct sensor
{
  unsigned short id;
  int index;
  float coef;
} sensor_t;

static sensor_t sensors[19] = {
  {SENS_CPUTEMP, 0, 1.0f},
  {SENS_SYSTEMP, 1, 1.0f},
  {SENS_PWMTEMP, 2, 1.0f},
  {SENS_VCORE, 3, MLTP_3V49},
  {SENS_DDRVDD, 4, MLTP_3V49},
  {SENS_DDRVTT, 5, MLTP_3V49},
  {SENS_NBVDD, 6, MLTP_3V49},
  {SENS_SBVDD, 7, MLTP_3V49},
  {SENS_HTV, 8, MLTP_3V49},
  {SENS_AGP, 9, MLTP_3V49},
  {SENS_5V, 10, MLTP_6V25},
  {SENS_3V3, 11, MLTP_4V36},
  {SENS_5VSB, 12, MLTP_6V25},
  {SENS_3VDUAL, 13, MLTP_4V36},
  {SENS_CPUFAN, 14, MLTP_FAN},
  {SENS_NBFAN, 15, MLTP_FAN},
  {SENS_SYSFAN, 16, MLTP_FAN},
  {SENS_AUXFAN1, 17, MLTP_FAN},
  {SENS_AUXFAN2, 18, MLTP_FAN},
};

static PyObject *uguru_error;

static PyObject *
uguru_read_sensor (PyObject * self, PyObject * args)
{
  int i;
  float ret;
  int index;

  switch(uguru_detected)
    {
    case FALSE:
      PyErr_SetString(uguru_error, "uGuru not detected");
      return NULL;
    case -1:
      PyErr_SetString(uguru_error, "permission denied");
      return NULL;
    }

  if (!PyArg_ParseTuple (args, "i", &index))
    return NULL;

  if (index < 0 || index > 18)
    {
      PyErr_SetString (uguru_error, "invalid sensor");
      return NULL;
    }

  ret = uGuru_ReadSensor (sensors[index].id) * sensors[index].coef;
  uGuru_Ready ();

  return Py_BuildValue ("f", ret);
}


static PyMethodDef uguru_methods[] = {
  {"read_sensor", uguru_read_sensor, METH_VARARGS,
   read_sensor_doc},
  {NULL}			/* Sentinel */
};


#ifndef PyMODINIT_FUNC		/* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC
inituguru (void)
{
  PyObject *m;

  m = Py_InitModule3 ("uguru", uguru_methods,
		      "Interface to read sensors from an A-Bit uGuru motherboard.");

  PyModule_AddIntConstant (m, "SENS_CPUTEMP", 0);
  PyModule_AddIntConstant (m, "SENS_SYSTEMP", 1);
  PyModule_AddIntConstant (m, "SENS_PWMTEMP", 2);
  PyModule_AddIntConstant (m, "SENS_VCORE", 3);
  PyModule_AddIntConstant (m, "SENS_DDRVDD", 4);
  PyModule_AddIntConstant (m, "SENS_DDRVTT", 5);
  PyModule_AddIntConstant (m, "SENS_NBVDD", 6);
  PyModule_AddIntConstant (m, "SENS_SBVDD", 7);
  PyModule_AddIntConstant (m, "SENS_HTV", 8);
  PyModule_AddIntConstant (m, "SENS_AGP", 9);
  PyModule_AddIntConstant (m, "SENS_5V", 10);
  PyModule_AddIntConstant (m, "SENS_3V3", 11);
  PyModule_AddIntConstant (m, "SENS_5VSB", 12);
  PyModule_AddIntConstant (m, "SENS_3VDUAL", 13);
  PyModule_AddIntConstant (m, "SENS_CPUFAN", 14);
  PyModule_AddIntConstant (m, "SENS_NBFAN", 15);
  PyModule_AddIntConstant (m, "SENS_SYSFAN", 16);
  PyModule_AddIntConstant (m, "SENS_AUXFAN1", 17);
  PyModule_AddIntConstant (m, "SENS_AUXFAN2", 18);

  uguru_error = PyErr_NewException ("uguru.error", NULL, NULL);
  Py_INCREF (uguru_error);
  PyModule_AddObject (m, "error", uguru_error);

  uguru_detected = uGuru_Detect();
}
