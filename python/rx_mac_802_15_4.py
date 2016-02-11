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


# Variable Global
pack_tot = 0.0
pack_err = 0.0
PER = 0.0

class rx_mac_802_15_4(gr.sync_block):
	"""
	docstring for block rx_mac_802_15_4
	"""
	def __init__(self, SrcAddR):
		#Variables externas Parametros
		self.SrcAddR = SrcAddR
		gr.sync_block.__init__(self,
			name="rx_mac_802_15_4",
			in_sig=[],
			out_sig=[])
		self.message_port_register_in(pmt.intern("in"))
		self.message_port_register_out(pmt.intern("out"))
		self.set_msg_handler(pmt.intern("in"), self.deframe_NPDU)  #Funcion 


	def reflect(self,crc, bitnum):
		# Refleja el LSB 'bitnum' del 'crc'
		j=1
		crcout=0
		for b in range(bitnum):
			i=1<<(bitnum-1-b)
			if crc & i:
				crcout |= j
			j <<= 1
		return crcout


	def crc16(self,p): #string
		crc = 0
		for i in range(len(p)):
			c = p[i]
			c = self.reflect(ord(c), 8)
			j=0x80
			for b in range(16):
				bit = crc & 0x8000
				crc <<= 1
				crc &=0xFFFF
				if c & j:
					crc |= 1
				if bit:
					crc ^= 0x1021
				j>>=1
				if j == 0:
					break
		for i in range(16):
			bit = crc & 0x8000
			crc <<= 1
			if bit:
				crc ^= 0x1021
		crc = self.reflect(crc, 16)
		return crc


	def deframe_NPDU(self,msg_pmt):
		global pack_err
		global pack_tot
		global PER
		# veficcación del formato PMT
		if pmt.is_blob(msg_pmt):
			blob = msg_pmt
			#print "is blob"
		elif pmt.is_pair(msg_pmt):
			blob = pmt.cdr(msg_pmt)
			#print "is pair"
		else:
			print "Formato desconocido" 
			return
		data_len = pmt.blob_length(blob)
		if(data_len < 11):
			print "MAC: muy corta!"
			pack_err = pack_err+1.0
			return;
		data_np	= pmt.to_python(blob) 	#numpy.ndarray	
		data_py = data_np.tolist()		#python list
		#print "Paquete",data_py,data_py.__class__
		#print "Dir Gateway",self.SrcAddR," Dir Nodo",data_py[7:9]
		if len(set(self.SrcAddR).intersection(data_py)) < 2 :		#Validación TX de la misma dirección
			
			# Valodacion FCS y cuenta PER
			rec_FCS = [data_py[-2],data_py[-1]] #FCS recibido
			del data_py[-2],data_py[-1]			#quita FCS
			s_to_fcs = struct.pack('B'*len(data_py), *data_py)  # Convierte List a String
			a = self.crc16(s_to_fcs)		#Calcula FCS
			FCS= [a & 0xFF,(a>>8)&0xFF] 

			if FCS == rec_FCS:		# paquete correcto
				index = 9
				del data_py[:index]				# FC(2),Sec_N(1),PanID(2),Dst_Add(2),Src_Add(2)
				# Crea un PMT vacio:
				send_pmt = pmt.make_u8vector(len(data_py), ord(' '))
				# Copy all characters to the u8vector:
				for i in range(len(data_py)):
					pmt.u8vector_set(send_pmt, i, data_py[i])
				# Send the message:
				self.message_port_pub(pmt.intern('out'), pmt.cons(pmt.PMT_NIL, send_pmt))
			else:
				pack_err = pack_err+1.0
		
			pack_tot = pack_tot +1.0
			PER =pack_err/pack_tot*100.0
			print ",",pack_tot,",",pack_err,",",PER,"%"




