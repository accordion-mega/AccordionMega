#include <Python.h>
#include <sys/time.h>
#include <sys/resource.h>

#include "RtAudio.h" // must precede arrayobject.h
#include <numarray/numarray.h>
#include <numarray/arrayobject.h>
#include <pthread.h>
#include <queue>


#ifndef Py_RETURN_NONE
#define Py_RETURN_NONE Py_INCREF(Py_None); return Py_None;
#endif


extern "C" 
{

static PyObject *RtAudioError;

static PyObject *PyRTAUDIO_SINT8;
static PyObject *PyRTAUDIO_SINT16;
static PyObject *PyRTAUDIO_SINT24;
static PyObject *PyRTAUDIO_SINT32;
static PyObject *PyRTAUDIO_FLOAT32;
static PyObject *PyRTAUDIO_FLOAT64;

typedef struct 
{
  PyObject_HEAD;
  RtAudio *rtaudio;
  RtAudioFormat _format;
  int _bufferSize;
  PyArrayObject *_streamBuffer;
} PyRtAudio;


static int RtAudioFormat_2_NumarrayType(RtAudioFormat format)
{
  switch (format)
    {
    case RTAUDIO_SINT8:
      return tInt8;      
    case RTAUDIO_SINT16:
      return tInt16;
    case RTAUDIO_SINT24:
      return tInt32; // eh?
    case RTAUDIO_SINT32:
      return tInt32;
    case RTAUDIO_FLOAT32:
      return tFloat32;
    case RTAUDIO_FLOAT64:
      return tFloat64;
    }
  return -1;
}


static void
RtAudio_dealloc(PyRtAudio *self)
{
  delete self->rtaudio;
  Py_XDECREF(self->_streamBuffer);
  self->ob_type->tp_free((PyObject *) self);
}


static PyObject *
RtAudio_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
  PyRtAudio *self;
  char *api = NULL;
  
  if(!PyArg_ParseTuple(args, "|s", &api))
    return NULL;

  self = (PyRtAudio *) type->tp_alloc(type, 0);
  if(self == NULL)
    return NULL;

  try
    {
      if(api == NULL)
        self->rtaudio = new RtAudio;
      else if(!strcmp(api, "jack"))
        self->rtaudio = new RtAudio(RtAudio::LINUX_JACK);
      else if(!strcmp(api, "alsa"))
        self->rtaudio = new RtAudio(RtAudio::LINUX_ALSA);
      else if(!strcmp(api, "oss"))
        self->rtaudio = new RtAudio(RtAudio::LINUX_ALSA);
      else if(!strcmp(api, "core"))
        self->rtaudio = new RtAudio(RtAudio::MACOSX_CORE);
      else if(!strcmp(api, "irix"))
        self->rtaudio = new RtAudio(RtAudio::IRIX_AL);
      else if(!strcmp(api, "asio"))
        self->rtaudio = new RtAudio(RtAudio::WINDOWS_ASIO);
      else if(!strcmp(api, "directsound"))
        self->rtaudio = new RtAudio(RtAudio::WINDOWS_DS);
    }
  catch(RtError &error)
    {
      PyErr_Format(RtAudioError, error.getMessageString());
      Py_DECREF(self);
      return NULL;
    }

  self->_streamBuffer = NULL;
  return (PyObject *) self;
}

static int
RtAudio_init(PyRtAudio *self, PyObject *args, PyObject *kwds)
{
  return 0;
}


static PyObject *
RtAudio_openStream(PyRtAudio *self, PyObject *args)
{
  int outputDevice;
  int outputChannels;
  int inputDevice;
  int inputChannels;
  RtAudioFormat format;
  int sampleRate;
  int bufferSize;
  int numberOfBuffers;

  char *buffer;
  int dims[1];
  int type;

  if(!PyArg_ParseTuple(args, "iiiikiii", 
                       &outputDevice,
                       &outputChannels,
                       &inputDevice,
                       &inputChannels,
                       &format,
                       &sampleRate,
                       &bufferSize,
                       &numberOfBuffers))
    return NULL;

  try
    {
      
      self->rtaudio->openStream(outputDevice, outputChannels,
                                inputDevice, inputChannels,
                                format, sampleRate, 
                                &bufferSize, &numberOfBuffers);
    }
  catch(RtError &error)
    {
      PyErr_Format(RtAudioError, error.getMessageString());
      return NULL;
    }

  bufferSize *= outputChannels; // fix for input, duplex

  /* the stream buffer is only allocated after a stream has been opened. */
  try
    {
      buffer = self->rtaudio->getStreamBuffer();
    }
  catch(RtError &error)
    {
      PyErr_Format(RtAudioError, error.getMessageString());
      return NULL;
    }

  dims[0] = bufferSize;
  type = RtAudioFormat_2_NumarrayType(format);

  Py_XDECREF(self->_streamBuffer);
  if(self->_streamBuffer == NULL)
    {
      self->_streamBuffer = (PyArrayObject *)
        PyArray_FromDimsAndData(1, dims, type, buffer);
      if(self->_streamBuffer == NULL)
        return NULL;
    }
  
  Py_RETURN_NONE;
  
}


static PyObject *
RtAudio_cancelStreamCallback(PyRtAudio *self, PyObject *args)
{
 try
   {
     self->rtaudio->cancelStreamCallback();
   }
 catch(RtError &error)
   {
      PyErr_Format(RtAudioError, error.getMessageString());
      return NULL;
   }

 Py_RETURN_NONE;
}


static PyObject *
RtAudio_getDeviceCount(PyRtAudio *self, PyObject *args)
{
  return Py_BuildValue("i", self->rtaudio->getDeviceCount());
}


static PyObject *
RtAudio_getDeviceInfo(PyRtAudio *self, PyObject *args)
{
  int device;
  RtAudioDeviceInfo info;

  PyObject *name = NULL;
  PyObject *probed = NULL;
  PyObject *outputChannels = NULL;
  PyObject *inputChannels = NULL;
  PyObject *duplexChannels = NULL;
  PyObject *isDefault = NULL;
  PyObject *sampleRates = NULL;
  PyObject *nativeFormats = NULL;
  PyObject *deviceInfo = NULL;


  if(!PyArg_ParseTuple(args, "i", &device))
    return NULL;

  try
    {
      info = self->rtaudio->getDeviceInfo(device);
    }
  catch(RtError &error)
    {
      PyErr_Format(RtAudioError, error.getMessageString());
      return NULL;
    }

  name = PyString_FromString(info.name.c_str());
  if(name == NULL) return NULL;
  
  if(info.probed)
    {
      probed = Py_True;
      Py_INCREF(Py_True);
    }
  else
    {
      probed = Py_False;
      Py_INCREF(Py_False);
    }
  
  outputChannels = PyInt_FromLong(info.outputChannels);
  if(outputChannels == NULL) goto fail;
  
  inputChannels = PyInt_FromLong(info.inputChannels);
  if(inputChannels == NULL) goto fail;
  
  duplexChannels = PyInt_FromLong(info.duplexChannels);
  if(duplexChannels == NULL) goto fail;
  
  if(info.isDefault)
    {
      isDefault = Py_True;
      Py_INCREF(Py_True);
    }
  else
    {
      isDefault = Py_False;
      Py_INCREF(Py_False);
    }
  
  sampleRates = PyTuple_New(info.sampleRates.size());
  if(sampleRates == NULL)
    goto fail;

  for(uint i=0; i < info.sampleRates.size(); i++)
    {
      PyObject *rate = PyInt_FromLong(info.sampleRates[i]);
      if(rate == NULL)
        goto fail;
      if(PyTuple_SetItem(sampleRates, i, rate))
        {
          Py_DECREF(rate);
          goto fail;
        }
    }

  nativeFormats = PyLong_FromUnsignedLong(info.nativeFormats);
  if(nativeFormats == NULL)
    return NULL;
  
  deviceInfo = PyDict_New();
  if(deviceInfo == NULL)
    goto fail;

  if(PyDict_SetItemString(deviceInfo, "name", name))
    goto fail;
  if(PyDict_SetItemString(deviceInfo, "probed", probed))
    goto fail;
  if(PyDict_SetItemString(deviceInfo, "outputChannels", outputChannels))
    goto fail;
  if(PyDict_SetItemString(deviceInfo, "inputChannels", inputChannels)) 
    goto fail;
  if(PyDict_SetItemString(deviceInfo, "deviceChannels", duplexChannels))
    goto fail;
  if(PyDict_SetItemString(deviceInfo, "isDefault", isDefault))
    goto fail;
  if(PyDict_SetItemString(deviceInfo, "sampleRates", sampleRates))
    goto fail;
  if(PyDict_SetItemString(deviceInfo, "nativeFormats", nativeFormats))
    goto fail;

  return deviceInfo;

 fail:
  Py_XDECREF(name);
  Py_XDECREF(probed);
  Py_XDECREF(outputChannels);
  Py_XDECREF(inputChannels);
  Py_XDECREF(duplexChannels);
  Py_XDECREF(isDefault);
  Py_XDECREF(sampleRates);
  Py_XDECREF(nativeFormats);
  Py_XDECREF(deviceInfo);
  return NULL;
}


static PyObject *
RtAudio_getStreamBuffer(PyRtAudio *self, PyObject *args)
{
  try
    {
      // the buffer is gotten on openStream()
      self->rtaudio->getStreamBuffer();
    }
  catch(RtError &error)
    {
      PyErr_Format(RtAudioError, error.getMessageString());
      return NULL;
    }

  Py_INCREF(self->_streamBuffer);
  return (PyObject *) self->_streamBuffer;
}

static PyObject *
RtAudio_tickStream(PyRtAudio *self, PyObject *args)
{
  try
    {
      self->rtaudio->tickStream();
    }
  catch(RtError &error)
    {
      PyErr_Format(RtAudioError, error.getMessageString());
      return NULL;
    }
  
  Py_RETURN_NONE;
}


static PyObject *
RtAudio_closeStream(PyRtAudio *self, PyObject *args)
{
  try
    {
      self->rtaudio->closeStream();
    }
  catch(RtError &error)
   {
     PyErr_Format(RtAudioError, error.getMessageString());
     return NULL;
   }
  
  Py_RETURN_NONE;
}


static PyObject *
RtAudio_startStream(PyRtAudio *self, PyObject *args)
{
  try
    {
      self->rtaudio->startStream();
    }
  catch(RtError &error)
    {
      PyErr_Format(RtAudioError, error.getMessageString());
      return NULL;
    }
  
  Py_RETURN_NONE;
}


static PyObject *
RtAudio_stopStream(PyRtAudio *self, PyObject *args)
{
  try
    {
      self->rtaudio->stopStream();
    }
  catch(RtError &error)
    {
      PyErr_Format(RtAudioError, error.getMessageString());
      return NULL;
    }

  Py_XDECREF(self->_streamBuffer);
  self->_streamBuffer = NULL;

  Py_RETURN_NONE;
}


static PyObject *
RtAudio_abortStream(PyRtAudio *self, PyObject *args)
{
  try
    {
      self->rtaudio->abortStream();
    }
  catch(RtError &error)
    {
      PyErr_Format(RtAudioError, error.getMessageString());
      return NULL;
    }

  Py_XDECREF(self->_streamBuffer);
  self->_streamBuffer = NULL;

  Py_RETURN_NONE;
}


static PyMethodDef RtAudio_methods[] = 
{
  {"openStream", (PyCFunction) RtAudio_openStream, METH_VARARGS,
   "A public method for opening a stream with the specified parameters."},

  /*
  {"setStreamCallback", (PyCFunction) RtAudio_setStreamCallback, METH_VARARGS,
   "A public method which sets a user-defined callback function for a "
   "given stream."},
  */

  {"cancelStreamCallback", (PyCFunction) RtAudio_cancelStreamCallback, METH_NOARGS,
   "A public method which cancels a callback process and function for the "
   "stream."},

  {"getDeviceCount", (PyCFunction) RtAudio_getDeviceCount, METH_NOARGS,
   "A public method which returns the number of audio devices found."},
  
  {"getDeviceInfo", (PyCFunction) RtAudio_getDeviceInfo, METH_VARARGS,
   "Return a dictionary containing information for a specified device number"},

  {"getStreamBuffer", (PyCFunction) RtAudio_getStreamBuffer, METH_NOARGS,
   "A public method which returns a pointer to the buffer for an open "
   "stream."},
  
  {"tickStream", (PyCFunction) RtAudio_tickStream, METH_NOARGS,
   "Public method used to trigger processing of input/output data for a stream."},

  {"closeStream", (PyCFunction) RtAudio_stopStream, METH_NOARGS,
   "Public method which closes a stream and frees any associated buffers."},

  {"startStream", (PyCFunction) RtAudio_startStream, METH_NOARGS,
   "Public method which starts a stream."},

  {"stopStream", (PyCFunction) RtAudio_stopStream, METH_NOARGS,
   "Stop a stream, allowing any samples remaining in the queue to be played "
   "out and/or read in."},

  {"abortStream", (PyCFunction) RtAudio_abortStream, METH_NOARGS,
   "Stop a stream, discarding any samples remaining in the input/output "
   "queue."},

  {NULL}
};


static PyTypeObject RtAudio_type = {
    PyObject_HEAD_INIT(NULL)
    0,                         /*ob_size*/
    "rtaudio.RtAudio",             /*tp_name*/
    sizeof(RtAudio), /*tp_basicsize*/
    0,                         /*tp_itemsize*/
    (destructor) RtAudio_dealloc,                         /*tp_dealloc*/
    0,                         /*tp_print*/
    0,                         /*tp_getattr*/
    0,                         /*tp_setattr*/
    0,                         /*tp_compare*/
    0,                         /*tp_repr*/
    0,                         /*tp_as_number*/
    0,                         /*tp_as_sequence*/
    0,                         /*tp_as_mapping*/
    0,                         /*tp_hash */
    0,                         /*tp_call*/
    0,                         /*tp_str*/
    0,                         /*tp_getattro*/
    0,                         /*tp_setattro*/
    0,                         /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,        /*tp_flags*/
    "Midi input device",           /* tp_doc */
    0,               /* tp_traverse */
    0,               /* tp_clear */
    0,               /* tp_richcompare */
    0,               /* tp_weaklistoffset */
    0,               /* tp_iter */
    0,               /* tp_iternext */
    RtAudio_methods,             /* tp_methods */
    0,              /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)RtAudio_init,      /* tp_init */
    0,                         /* tp_alloc */
    RtAudio_new,                 /* tp_new */
};




static PyObject *
rtaudio_get_priority(PyObject *obj, PyObject *args)
{
#if defined(__LINUX_ALSA__) || defined(__LINUX_OSS__) || defined(__LINUX_JACK__)
  struct sched_param schp = { 0 };
  int ret;

  ret = sched_getparam(0, &schp);
  if(ret == -1)
    {
      PyErr_Format(RtAudioError, strerror(errno));
      return NULL;
    }
  return Py_BuildValue("i", schp.sched_priority);
#endif

#ifdef __MACOSX_CORE__

  struct sched_param sp;
  memset(&sp, 0, sizeof(struct sched_param));
  int policy;

  if (pthread_getschedparam(pthread_self(), &policy, &sp) == -1)
    {
      PyErr_SetString(RtAudioError, strerror(errno));
      return NULL;
    }

  return Py_BuildValue("i", sp.sched_priority);
#endif

  Py_RETURN_NONE;
}


static PyObject *
rtaudio_set_priority(PyObject *obj, PyObject *args)
{
  int priority;
  if(!PyArg_ParseTuple(args, "i", &priority))
    return NULL;

#if defined(__LINUX_ALSA__) || defined(__LINUX_OSS__) || defined(__LINUX_JACK__)
  struct sched_param schp = { 0 };
  int ret;
  schp.sched_priority = priority;

  ret = sched_setparam(0, &schp);
  if(ret == -1)
    {
      PyErr_Format(RtAudioError, strerror(errno));
      return NULL;
    }

#elif defined(__MACOSX_CORE__)

  struct sched_param sp;
 
  memset(&sp, 0, sizeof(struct sched_param));
  sp.sched_priority=priority;
  if (pthread_setschedparam(pthread_self(), SCHED_RR, &sp)  == -1) 
    {
      PyErr_SetString(RtAudioError, strerror(errno));
      return NULL;
    }

#endif
  Py_RETURN_NONE;
}


#define SCHEDULER_POLICY SCHED_RR

static PyObject *
rtaudio_boost_priority(PyObject *obj, PyObject *args)
{
#if defined(__LINUX_ALSA__) || defined(__LINUX_OSS__) || defined(__LINUX_JACK__)
  struct sched_param schp = { 0 };
  int priority = (sched_get_priority_max(SCHEDULER_POLICY) -
                  sched_get_priority_min(SCHEDULER_POLICY)) / 2;
  schp.sched_priority = priority;
  
  if (sched_setscheduler(0, SCHEDULER_POLICY, &schp) != 0)
    {
      PyErr_Format(RtAudioError, "insufficient priveledges");
      return NULL;
    }

  /* We are running at high priority so we should have a watchdog in
     case audio goes wild. */
#endif

#if defined(__MACOSX_CORE__)

  struct sched_param sp;
  memset(&sp, 0, sizeof(struct sched_param));
  int policy;

  if (pthread_getschedparam(pthread_self(), &policy, &sp) == -1)
    {
      PyErr_SetString(RtAudioError, strerror(errno));
      return NULL;
    }

  sp.sched_priority += 40;
  if (pthread_setschedparam(pthread_self(), SCHED_RR, &sp)  == -1) 
    {
      PyErr_SetString(RtAudioError, strerror(errno));
      return NULL;
    }

#endif
  Py_RETURN_NONE;
}


static PyMethodDef rtaudio_methods[] = {
  {"get_priority", rtaudio_get_priority, METH_NOARGS,
   "Return the platform-specific value indicating the current priority of "
   "the calling thread."},

  {"set_priority", rtaudio_set_priority, METH_VARARGS,
   "Set the platform-specific scheduling priority of the calling thread"},

  {"boost_priority", rtaudio_boost_priority, METH_NOARGS,
   "Bump priority of audio thread if priveledges allow it."},

    {NULL}  /* Sentinel */
};


#ifndef PyMODINIT_FUNC	/* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC
initrtaudio(void) 
{
  PyEval_InitThreads();
  import_libnumarray();
  import_libnumeric();

  PyObject* module;
  
  if (PyType_Ready(&RtAudio_type) < 0)
    return;
  
  module = Py_InitModule3("rtaudio", rtaudio_methods,
			  "RtAudio wrapper.");

  PyRTAUDIO_SINT8 = PyLong_FromUnsignedLong(RTAUDIO_SINT8);
  PyModule_AddObject(module, "RTAUDIO_SINT8", PyRTAUDIO_SINT8);
  Py_INCREF(PyRTAUDIO_SINT8);

  PyRTAUDIO_SINT16 = PyLong_FromUnsignedLong(RTAUDIO_SINT16);
  PyModule_AddObject(module, "RTAUDIO_SINT16", PyRTAUDIO_SINT16);
  Py_INCREF(PyRTAUDIO_SINT16);

  PyRTAUDIO_SINT24 = PyLong_FromUnsignedLong(RTAUDIO_SINT24);
  PyModule_AddObject(module, "RTAUDIO_SINT24", PyRTAUDIO_SINT24);
  Py_INCREF(PyRTAUDIO_SINT24);

  PyRTAUDIO_SINT32 = PyLong_FromUnsignedLong(RTAUDIO_SINT32);
  PyModule_AddObject(module, "RTAUDIO_SINT32", PyRTAUDIO_SINT32);
  Py_INCREF(PyRTAUDIO_SINT32);

  PyRTAUDIO_FLOAT32 = PyLong_FromUnsignedLong(RTAUDIO_FLOAT32);
  PyModule_AddObject(module, "RTAUDIO_FLOAT32", PyRTAUDIO_FLOAT32);
  Py_INCREF(PyRTAUDIO_FLOAT32);

  PyRTAUDIO_FLOAT64 = PyLong_FromUnsignedLong(RTAUDIO_FLOAT64);
  PyModule_AddObject(module, "RTAUDIO_FLOAT64", PyRTAUDIO_FLOAT64);
  Py_INCREF(PyRTAUDIO_FLOAT64);
  
  Py_INCREF(&RtAudio_type);
  PyModule_AddObject(module, "RtAudio", (PyObject *)&RtAudio_type);
  
  RtAudioError = PyErr_NewException("rtaudio.RtError", NULL, NULL);
  PyModule_AddObject(module, "RtError", RtAudioError);
  Py_INCREF(RtAudioError);
}

} // extern "C"
