Librerias para implementar comunicacion de módulos Xbee S2 & S2 PRO en GNU Radio 3.7.

El trabajo se basa en la libreria _gr-ieee802-15-4_ administrada por Bastian Bloessl.
Las librerias implementan bloques independientes para Tx y para RX para capa PHY O-QPSK, MAC, Network, Application, definidas en el estandar 802.15.4 y ZigBee2006.

Antes de utilizar, se debe instalar las librerias _gr-ieee802-15-4_ y _gr-foo_ que se encuentran respectivamente en:
https://github.com/bastibl/gr-ieee802-15-4
https://github.com/bastibl/gr-foo

==== Instalación ====

git clone git://github.com/EsperanzaSegura/gr-WSN.git
cd gr-WSN
mkdir build
cd build
cmake ..
make
sudo make install
sudo ldconfig


En la Carpeta Ejemplos se encuentran los flujogramas para transmisión y recepción. Previamiente deben ejecutarse los flujogramas que crean los bloques jerárquico
Rx_Phy_OQPSK.grc
Tx_Phy_OQPSK.grc
