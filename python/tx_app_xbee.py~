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
count_app = [0]

class tx_app_xbee(gr.sync_block):
    """
    docstring for block tx_app_xbee
    """
    def __init__(self):
        gr.sync_block.__init__(self,
            name="tx_app_xbee",
            in_sig=[],
            out_sig=[])
        self.message_port_register_in(pmt.intern("in"))
        self.message_port_register_out(pmt.intern("out"))
        self.set_msg_handler(pmt.intern("in"), self.make_APDU)  #Funcion make_APDU

    def make_APDU(self,msg_pmt):
        # Toma Pmt Symbol a String y luego a list
        msg_pmt = pmt.symbol_to_string(msg_pmt)
        msg = [ord(c) for c in msg_pmt]
        global count_app
        count_app[0] =  count_app[0] +1
        if count_app[0] > 254: count_app[0] = 0
        Src_EP = [0xE8]			# Source endpoint
        Profile = [0x05,0xC1]   # Profile ID  LSB-MSB
        Cluster = [0x11,0x00]   # Cluster ID  LSB-MSB
        Dst_EP = [0xE8]			# Destination endpoint
        FC_A = [0x08]  			# Frame Control APP
        APDU = FC_A + Dst_EP + Cluster + Profile + Src_EP + count_app + msg
        
        # Crea PMT vacio
        send_pmt = pmt.make_u8vector(len(APDU), ord(' '))
        # Copia Caracteres a u8vector:
        for i in range(len(APDU)):
            pmt.u8vector_set(send_pmt, i, APDU[i])
        
        # Envia mensaje:
        self.message_port_pub(pmt.intern('out'), pmt.cons(pmt.PMT_NIL, send_pmt))


