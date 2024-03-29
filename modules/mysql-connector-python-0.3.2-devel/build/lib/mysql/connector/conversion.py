# MySQL Connector/Python - MySQL driver written in Python.
# Copyright (c) 2009,2010, Oracle and/or its affiliates. All rights reserved.
# Use is subject to license terms. (See COPYING)

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation.
# 
# There are special exceptions to the terms and conditions of the GNU
# General Public License as it is applied to this software. View the
# full text of the exception in file EXCEPTIONS-CLIENT in the directory
# of this software distribution or see the FOSS License Exception at
# www.mysql.com.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

"""Converting MySQL and Python types
"""

import struct
import datetime
import time
from decimal import Decimal

from . import errors
from .constants import FieldType, FieldFlag

class ConverterBase(object):
    
    def __init__(self, charset='utf8', use_unicode=True):
        self.python_types = None
        self.mysql_types = None
        self.set_charset(charset)
        self.set_unicode(use_unicode)
        
    def set_charset(self, charset):
        if charset is not None:
            self.charset = charset
        else:
            # default to utf8
            self.charset = 'utf8'
    
    def set_unicode(self, value=True):
        self.use_unicode = value
    
    def to_mysql(self, value):
        return value
    
    def to_python(self, vtype, value):
        return value
    
    def escape(self, buf):
        return buf
    
    def quote(self, buf):
        return str(buf)

class MySQLConverter(ConverterBase):
    """
    A converted class grouping:
     o escape method: for escpaing values send to MySQL
     o quoting method: for quoting values send to MySQL in statements
     o conversion mapping: maps Python and MySQL data types to
       function for converting them.
       
    This class should be overloaded whenever one needs differences
    in how values are to be converted. Each MySQLConnection object
    has a default_converter property, which can be set like
      MySQL.converter(CustomMySQLConverter)
      
    """
    def __init__(self, charset=None, use_unicode=True):
        ConverterBase.__init__(self, charset, use_unicode)

        self.python_types = {
            int : int,
            float : float,
            str : self._str_to_mysql,
            bytes: self._bytes_to_mysql,
            bool : self._bool_to_mysql,
            type(None) : self._none_to_mysql,
            datetime.datetime : self._datetime_to_mysql,
            datetime.date : self._date_to_mysql,
            datetime.time : self._time_to_mysql,
            time.struct_time : self._struct_time_to_mysql,
            datetime.timedelta : self._timedelta_to_mysql,
            Decimal : self._decimal_to_mysql,
        }
        
        self.mysql_types = {
            FieldType.TINY : self._int,
            FieldType.SHORT : self._int,
            FieldType.INT24 : self._int,
            FieldType.LONG : self._long,
            FieldType.LONGLONG : self._long,
            FieldType.FLOAT : self._float,
            FieldType.DOUBLE : self._float,
            FieldType.DECIMAL : self._decimal,
            FieldType.NEWDECIMAL : self._decimal,
            FieldType.VAR_STRING : self._STRING_to_python,
            FieldType.STRING : self._STRING_to_python,
            FieldType.SET : self._SET_to_python,
            FieldType.TIME : self._TIME_to_python,
            FieldType.DATE : self._DATE_to_python,
            FieldType.NEWDATE : self._DATE_to_python,
            FieldType.DATETIME : self._DATETIME_to_python,
            FieldType.TIMESTAMP : self._DATETIME_to_python,
            FieldType.BLOB : self._STRING_to_python,
            FieldType.YEAR: self._YEAR_to_python,
            FieldType.BIT: self._BIT_to_python,
        }
    
    def escape(self, value):
        """
        Escapes special characters as they are expected to by when MySQL
        receives them.
        As found in MySQL source mysys/charset.c
        
        Returns the value if not a string, or the escaped string.
        """
        if value is None:
            return value
        elif isinstance(value, (int,float,Decimal)):
            return value
        if isinstance(value,bytes):
            value = value.replace(b'\\',b'\\\\')
            value = value.replace(b'\n',b'\\n')
            value = value.replace(b'\r',b'\\r')
            value = value.replace(b'\047',b'\134\047') # single quotes
            value = value.replace(b'\042',b'\134\042') # double quotes
            value = value.replace(b'\032',b'\134\032') # for Win32
        else:
            value = value.replace('\\','\\\\')
            value = value.replace('\n','\\n')
            value = value.replace('\r','\\r')
            value = value.replace('\047','\134\047') # single quotes
            value = value.replace('\042','\134\042') # double quotes
            value = value.replace('\032','\134\032') # for Win32
        return value
    
    def quote(self, buf):
        """
        Quote the parameters for commands. General rules:
          o numbers are returns as bytes using ascii codec
          o None is returned as bytes('NULL')
          o Everything else is single quoted '<bytes>'
        
        Returns a bytes object.
        """
        if isinstance(buf, (int,float,Decimal)):
            return str(buf).encode('ascii')
        elif isinstance(buf, type(None)):
            return b"NULL"
        else:
            return b"'" + buf + b"'"
    
    def to_mysql(self, value):
        vtype = type(value)
        return self.python_types[vtype](value)
    
    def _str_to_mysql(self, value):
        return value.encode(self.charset)
    
    def _bytes_to_mysql(self, value):
        return value
    
    def _bool_to_mysql(self, value):
        if value:
            return 1
        else:
            return 0
        
    def _none_to_mysql(self, value):
        """
        This would return what None would be in MySQL, but instead we
        leave it None and return it right away. The actual convertion
        from None to NULL happens in the quoting functionality.
        
        Return None.
        """
        return None
        
    def _datetime_to_mysql(self, value):
        """
        Converts a datetime instance to a string suitable for MySQL.
        The returned string has format: %Y-%m-%d %H:%M:%S
        
        If the instance isn't a datetime.datetime type, it return None.
        
        Returns a bytes.
        """
        return '{:d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(
            value.year, value.month, value.day,
            value.hour, value.minute, value.second).encode('ascii')
        
    def _date_to_mysql(self, value):
        """
        Converts a date instance to a string suitable for MySQL.
        The returned string has format: %Y-%m-%d
        
        If the instance isn't a datetime.date type, it return None.
        
        Returns a bytes.
        """
        return '{:d}-{:02d}-{:02d}'.format(value.year, value.month,
            value.day).encode('ascii')
        
    def _time_to_mysql(self, value):
        """
        Converts a time instance to a string suitable for MySQL.
        The returned string has format: %H:%M:%S
        
        If the instance isn't a datetime.time type, it return None.
        
        Returns a bytes.
        """
        return value.strftime('%H:%M:%S').encode('ascii')
    
    def _struct_time_to_mysql(self, value):
        """
        Converts a time.struct_time sequence to a string suitable
        for MySQL.
        The returned string has format: %Y-%m-%d %H:%M:%S
        
        Returns a bytes or None when not valid.
        """
        return time.strftime('%Y-%m-%d %H:%M:%S',value).encode('ascii')
        
    def _timedelta_to_mysql(self, value):
        """
        Converts a timedelta instance to a string suitable for MySQL.
        The returned string has format: %H:%M:%S

        Returns a bytes.
        """
        (hours, r) = divmod(value.seconds, 3600)
        (mins, secs) = divmod(r, 60)
        hours = hours + (value.days * 24)
        return '{:02d}:{:02d}:{:02d}'.format(hours,mins,secs).encode('ascii')
        
    def _decimal_to_mysql(self, value):
        """
        Converts a decimal.Decimal instance to a string suitable for
        MySQL.
        
        Returns a bytes or None when not valid.
        """
        if isinstance(value, Decimal):
            return str(value).encode('ascii')
        
        return None
         
    def to_python(self, flddsc, value):
        """
        Converts a given value coming from MySQL to a certain type in Python.
        The flddsc contains additional information for the field in the
        table. It's an element from MySQLCursor.description.
        
        Returns a mixed value.
        """
        res = value
        
        if value == 0 and flddsc[1] != FieldType.BIT: # \x00
            # Don't go further when we hit a NULL value
            return None
        if value is None:
            return None
        
        try:
            res = self.mysql_types[flddsc[1]](value, flddsc)
        except KeyError:
            # If one type is not defined, we just return the value as str
            return value.decode('utf-8')
        except ValueError as e:
            raise ValueError("%s (field %s)" % (e, flddsc[0]))
        except TypeError as e:
            raise TypeError("%s (field %s)" % (e, flddsc[0]))
        except:
            raise
        
        return res
    
    def _float(self, v, desc=None):
        """
        Returns v as float type.
        """
        return float(v)
    
    def _int(self, v, desc=None):
        """
        Returns v as int type.
        """
        return int(v)
        
    def _long(self, v, desc=None):
        """
        Returns v as long type.
        """
        return int(v)
    
    def _decimal(self, v, desc=None):
        """
        Returns v as a decimal.Decimal.
        """
        s = v.decode(self.charset)
        return Decimal(s)
        
    def _str(self, v, desc=None):
        """
        Returns v as str type.
        """
        return str(v)
    
    def _BIT_to_python(self, v, dsc=None):
        """Returns BIT columntype as integer"""
        s = v
        if len(s) < 8:
            s = b'\x00'*(8-len(s)) + s
        return struct.unpack('>Q', s)[0]
    
    def _DATE_to_python(self, v, dsc=None):
        """
        Returns DATE column type as datetime.date type.
        """
        pv = None
        try:
            pv = datetime.date(*[ int(s) for s in v.split(b'-')])
        except ValueError:
            return None
        else:
            return pv
            
    def _TIME_to_python(self, v, dsc=None):
        """
        Returns TIME column type as datetime.time type.
        """
        pv = None
        try:
            (h, m, s) = [ int(s) for s in v.split(b':')]
            pv = datetime.timedelta(hours=h,minutes=m,seconds=s)
        except ValueError:
            raise ValueError("Could not convert %s to python datetime.timedelta" % v)
        else:
            return pv
            
    def _DATETIME_to_python(self, v, dsc=None):
        """
        Returns DATETIME column type as datetime.datetime type.
        """
        pv = None
        try:
            (sd,st) = v.split(b' ')
            dt = [ int(v) for v in sd.split(b'-') ] +\
                 [ int(v) for v in st.split(b':') ]
            pv = datetime.datetime(*dt)
        except ValueError:
            pv = None
        
        return pv
    
    def _YEAR_to_python(self, v, desc=None):
        """Returns YEAR column type as integer"""
        try:
            year = int(v)
        except ValueError:
            raise ValueError("Failed converting YEAR to int (%s)" % v)

        return year

    def _SET_to_python(self, v, dsc=None):
        """Returns SET column typs as set
        
        Actually, MySQL protocol sees a SET as a string type field. So this
        code isn't called directly, but used by STRING_to_python() method.
        
        Returns SET column type as a set.
        """
        pv = None
        s = v.decode(self.charset)
        try:
            pv = set(s.split(','))
        except ValueError:
            raise ValueError("Could not convert set %s to a sequence." % v)
        return pv

    def _STRING_to_python(self, v, dsc=None):
        """
        Note that a SET is a string too, but using the FieldFlag we can see
        whether we have to split it.
        
        Returns string typed columns as string type.
        """
        if dsc is not None:
            # Check if we deal with a SET
            if dsc[7] & FieldFlag.SET:
                return self._SET_to_python(v, dsc)
            if dsc[7] & FieldFlag.BINARY:
                return v
        
        if isinstance(v, bytes) and self.use_unicode:
            return v.decode(self.charset)
            
        return v

    def _BLOB_to_python(self, v, dsc=None):
        if dsc is not None:
            if dsc[7] & FieldFlag.BINARY:
                return bytes(v)

        return self._STRING_to_python(v, dsc)
