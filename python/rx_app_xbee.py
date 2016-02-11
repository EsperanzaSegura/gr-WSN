#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2016 Miguel Sastoque - Claudia Segura - Grupo LIMER Universidad Distrital
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy as np
import string
import pmt
import struct
from gnuradio import gr
from gnuradio import digital

class rx_app_xbee(gr.sync_block):
	"""
	docstring for block rx_app_xbee
	"""
	def __init__(self):
		gr.sync_block.__init__(self,
			name="rx_app_xbee",
			in_sig=[],
			out_sig=[])
		self.message_port_register_in(pmt.intern("in"))
		self.message_port_register_out(pmt.intern("out"))
		self.set_msg_handler(pmt.intern("in"), self.deframe_MSJ)  #Funcion 


	def deframe_MSJ(self,msg_pmt):
		if pmt.is_blob(msg_pmt):
			blob = msg_pmt
			#print "is blob"
		elif pmt.is_pair(msg_pmt):
			blob = pmt.cdr(msg_pmt)
			#print "is pair"
		else:
			print "Formato desconocido" 
			return
		data_np	= pmt.to_python(blob) 	#numpy.ndarray	
		data_py = data_np.tolist()		#python list
		#print "Paquete",data_py,data_py.__class__
		index = 8
		del data_py[:index]				# FC (1), DesEP(1),Cluster(2),Profile(2),SourEP(1),Counter(1)
		#print "DEPACKED-->",data_py
		
		# Crea un PMT vacio:
		send_pmt = pmt.make_u8vector(len(data_py), ord(' '))
		# Copy all characters to the u8vector:
		for i in range(len(data_py)):
			pmt.u8vector_set(send_pmt, i, data_py[i])
		
		# Send the message:
		self.message_port_pub(pmt.intern('out'), pmt.cons(pmt.PMT_NIL, send_pmt))




