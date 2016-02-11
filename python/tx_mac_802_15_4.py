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
Seq_M = [0]
class tx_mac_802_15_4(gr.sync_block):
    """
    docstring for block tx_mac_802_15_4
    """
    def __init__(self, PanId,SrcAddM):
        #Variables externas Parametros
        self.SrcAddM = SrcAddM
        self.PanId = PanId
        gr.sync_block.__init__(self,
            name="tx_mac_802_15_4",
            in_sig=[],
            out_sig=[])
        self.message_port_register_in(pmt.intern("in"))
        self.message_port_register_out(pmt.intern("out"))
        self.set_msg_handler(pmt.intern("in"), self.make_MPDU)  #Funcion 
        
    """ Metodo actualizar variable necestia agregar callback en xml"""
    def set_PanId(self,new_val):
        self.PanId = new_val

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

    def make_MPDU(self,msg_pmt):
        if pmt.is_blob(msg_pmt):
            blob = msg_pmt
            #print "is blob"
        elif pmt.is_pair(msg_pmt):
            blob = pmt.cdr(msg_pmt)
            #print "is pair"
        else:
            print "Formato desconocido" 
            return
        # Toma Pmt pair a numpyarray y luego a list
        data_np	= pmt.to_python(blob) 	#numpy.ndarray	
        npdu = data_np.tolist()			#python list


        Src_Add = self.SrcAddM	 	# Dir 16 bit id de la red
        Dst_Add = [0xFF,0xFF]	 	# Coordinador 00 00 / #broadcast FF FF
        Pan_Id = self.PanId			# PanID que estabece el coordinador LSB -MSB
        global Seq_M
        Seq_M[0] =  Seq_M[0] +1
        if Seq_M[0] > 254: Seq_M[0] = 0
        FC_M = [0x41,0x88] 			#Frame control Mac LSB-MSB 
        
        to_fcs = FC_M + Seq_M + Pan_Id + Dst_Add + Src_Add + npdu
        s_to_fcs = struct.pack('B'*len(to_fcs), *to_fcs)  # Convierte List a String
        a = self.crc16(s_to_fcs)		#Calcula FCS
        FCS= [a & 0xFF,(a>>8)&0xFF] 
        
        MPDU = FC_M + Seq_M + Pan_Id + Dst_Add + Src_Add + npdu + FCS
        
        send_pmt = pmt.make_u8vector(len(MPDU), ord(' '))  	# Crea PMT vacio
        for i in range(len(MPDU)):
            pmt.u8vector_set(send_pmt, i, MPDU[i])			# Copia Caracteres a u8vector:
        # Envia mensaje:
        self.message_port_pub(pmt.intern('out'), pmt.cons(pmt.PMT_NIL, send_pmt))



