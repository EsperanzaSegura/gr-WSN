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
Seq_Num = [0]
class tx_nwk_zigbee(gr.sync_block):
    """
    docstring for block tx_nwk_zigbee
    """
    def __init__(self, SrcAddN,SrcIeeeN):
        #Variables externas Parametros
        self.SrcAddN = SrcAddN
        self.SrcIeeeN = SrcIeeeN
        
        gr.sync_block.__init__(self,
            name="tx_nwk_zigbee",
            in_sig=[],
            out_sig=[])
        self.message_port_register_in(pmt.intern("in"))
        self.message_port_register_out(pmt.intern("out"))
        self.set_msg_handler(pmt.intern("in"), self.make_NPDU)  #Funcion

    def make_NPDU(self,msg_pmt):
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
        apdu = data_np.tolist()			#python list
        
        Src_Ieee = self.SrcIeeeN	# la dir del USRP de 64 bit puede ser cualquiera
        
        global Seq_Num
        Seq_Num[0] =  Seq_Num[0] +1
        if Seq_Num[0] > 254: Seq_Num[0] = 0
        
        Radio = [0x1E] 	 			# Saltos Max del mensaje
        Src_Add = self.SrcAddN		# Puede ser cualquiera
        Dst_Add = [0xFF,0xFF]	 	# Coordinador 00 00 / #broadcast FF FF
        FC_N = [0x08,0x10] 			# Frame Control LSB-MSB 
        
        NPDU = FC_N + Dst_Add + Src_Add + Radio + Seq_Num + Src_Ieee  + apdu 
        
        # Crea PMT vacio
        send_pmt = pmt.make_u8vector(len(NPDU), ord(' '))
        # Copia Caracteres a u8vector:
        for i in range(len(NPDU)):
            pmt.u8vector_set(send_pmt, i, NPDU[i])
        
        # Envia mensaje:
        self.message_port_pub(pmt.intern('out'), pmt.cons(pmt.PMT_NIL, send_pmt))


