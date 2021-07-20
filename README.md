

![server](https://github.com/cnrkaya/socket-programming-python/blob/main/server_flow.jpg)

**Start:** First of all, socket() object is created and binded host and port values to run server. Host is a Ipv4 value assigned by hamachi server and port is a any unreserved port number. With the Listen function, a thread queue that can respond to 5 requests is created.

**Thread:** Requests from the client are accepted as long as there is an empty thread in the thread queue. If more than 5 requests come to the server at the same time, new requests are discarded until an empty thread is formed in the queue.

**Decode:** The request sent by the client is parsed in ascii format and assigned to a string.

**Proccess Request:** The request must be in a suitable format in order to be processed. If the format is not suitable, an error message will be sent. An example format that defines the temperature of greenhouse number 1 is “SERA1 TEMP 26”. The received information is transferred to the firebase cloud storage. At the same time, it is learned from the cloud storage whether there is a temperature update for that greenhouse.

**Encoding:** Error message if the request was negative; If it is positive, the confirmation message and the desired greenhouse temperature, are encoded in ascii format.
