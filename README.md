# WebSocket Serial Gateway

![alt text](<images/websocket serial port gateway illustration.jpeg>)

This python script is a gateway between a WebSocket client and a serial port.

Example usage: Easy connection between a web page (any browser) and a serial port (no security warning)

## Installation

- install python 3
- install modules

```shell
pip3 install websockets pyserial
```

## Configuration

You may edit gateway.py and configure the default values, however, it is recommended to pass the configuration as parameters on the command line or in the path when opening the WebSocket.

### Command line

Serial port, serial baudrate, WebSocket host and port are optional parameters on the command line.

See Usage section below for examples

### WebSocket path

The serial port and baud rate can be given in the path when creating the WebSocket. If provided, the values will override default values and command line parameters.

```js
socket = new WebSocket("ws://localhost:8765/[device][@baudrate]");
```

To automatically use the last serial port available, use /last for the device name.

```js
socket = new WebSocket("ws://localhost:8765/last@9600");
```

To get the list of available serial ports, use /list for the device name. The server will send the list of devices and close the connection.

```js
socket = new WebSocket("ws://localhost:8765/list");
```

### Edit gateway.py (not recommended)

```python
# Serial port configuration
ser_port = '/dev/tty.usbmodem101'
ser_baudrate = 115200

# WebSocket configuration
ws_host = 'localhost'
ws_port = 8765
```

## Usage

### Start the gateway

Basic, will use default value for serial port, baudrate, host and port

```shell
python3 gateway.py
```

With parameters to override default values for serial port, baudrate, host and port

```shell
python3 gateway.py [device] [baudrate] [host] [port]
python3 gateway.py /dev/cu.usbmodem101 9600 localhost 8765
```

Special device values

/list
: Server sends the list of available serial port devices and closes the connection

/last
: Use the last available serial port device. Usually it's the lastly connected.

### Development

Use nodemon to restart the server when the script is modified.

```shell
nodemon --exec python3 gateway.py
```

## Test

Simple HTTP client with p5.js

https://editor.p5js.org/prossel/sketches/fxODyCmxV

WebSocket Serial Monitor with p5.js

https://editor.p5js.org/prossel/sketches/zTU-rAJM6

## Improvements

The initial version is enough for the project that initiated it. However it would be nice to further improve it to make it more generic.

- [x] Auto detect last serial port
- [ ] Support a list of possible serial port or wildcard or regexp
- [x] Set the configuration from the command line
- [ ] Set the configuration from an external file (gitignored)
- [x] Serial configuration controlled by the WebSocket client
- [x] Get the list of available serial ports through WebSocket
- [ ] ...

Don't hesitate to send your pull requests.
