"""
Low-level python audio framework.

The primary requirements are:

 * play notes at given times
 * automate sequential playing (looping)
 * set the 'tempo' of a sample based on a global metric

Components:

 * hardware callback
 * timed stream writes
 * time-based writing of sources to hardware output
 * ring buffer
 * raw sources
 * rate filter
 * threaded buffering

Critical classes:

 * Sound
 * RingBuffer
 * RateFilter
 * Media
   * SndFile

 * Output
 * Scheduler
 * Clock
 
"""
