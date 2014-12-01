Websocket Server module
=======================

Based on RFC6455

                     -------------------
    dataRecv() ---->|                   |<----- status()
    state() ------->|                   |<----- result()
                    |                   |<----- dataSend()
                     -------------------
                     
- dataRecv() : data received from network (handshake or data frame)
- status() : what to do with result after processing (i.e send to network, send to application ...)
- result() : result after processing
- dataSend() : data to be encoded before sent to network
- state() : state of connection (readyState see websocket API)
TODO:
-----
- sendPing()
- sendClose()