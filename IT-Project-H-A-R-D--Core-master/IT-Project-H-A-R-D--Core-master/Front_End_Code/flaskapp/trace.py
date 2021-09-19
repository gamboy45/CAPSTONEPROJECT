#!/usr/bin/env python
#
#  Purpose:  Write trace info to file
#
#------------------------------------------------------------------------------

import pytz

from datetime import datetime

#------------------------------------------------------------------------------

from . import CONFIG

#------------------------------------------------------------------------------

class Trace:

    tfp        = None
    trace_file = CONFIG.DebugFile  # "C:/Temp/flaskapp.trace"

    #--------------------------------------------------------------------------

    def __init__(self):
        self.tfp = open(self.trace_file, 'a+')

    #--------------------------------------------------------------------------

    def open(self):
        self.tfp = open(self.trace_file, 'a+')

    #--------------------------------------------------------------------------

    def write(self, s):
    
        now = datetime.now(pytz.timezone('Australia/Sydney'))
        
        ts = now.strftime("%Y-%m-%d %H:%M:%S")
        
        if not self.tfp:
            self.open()

        self.tfp.write("%s:  %s\n" % (ts, s))

    #--------------------------------------------------------------------------

    def flush(self):
        self.tfp.flush()

    #--------------------------------------------------------------------------

    def close(self):
        self.tfp.close()
        self.tfp = None

    #--------------------------------------------------------------------------

    @classmethod
    def Write(cls, s):
    
        now = datetime.now(pytz.timezone('Australia/Sydney'))
        
        ts = now.strftime("%Y-%m-%d %H:%M:%S")
        
        if not cls.tfp:
            cls.tfp = open(cls.trace_file, 'a+')

        cls.tfp.write("%s:  %s\n" % (ts, s))
        cls.tfp.flush()
        
    #--------------------------------------------------------------------------

    @classmethod
    def Close(cls):
        if cls.tfp:
            cls.tfp.close()
            cls.tfp = None
        
    #--------------------------------------------------------------------------

          
        
        
#------------------------------------------------------------------------------

