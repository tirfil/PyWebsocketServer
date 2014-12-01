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
- sendPing() : Application send PING
- sendClose() : Application send CLOSE

status:

-   0   Nothing to do
-   1   HandShake OK to network
-   2   HandShake NOK to network
-   3   Data (frame encoded) to network
-   4   Pong (After receiving a Ping) to network
-   5   Close (After receiving close) to network
-   8   Data (frame decoded) to application