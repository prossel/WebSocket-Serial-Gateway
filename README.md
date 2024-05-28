# WebSocket Serial Gateway

This python script is a gateway between a WebSocket client and a serial port.

Example usage: Easy connection between a web page (any browser) and a serial port (no security warning)

## Installation

- install python 3
- install modules

```shell
pip3 install websockets pyserial
```

## Configuration

Edit gateway.py and configure these values:

```python
# Serial port configuration
ser_port = '/dev/tty.usbmodem101'
ser_baudrate = 115200

# WebSocket configuration
ws_host = 'localhost'
ws_port = 8765
```

## Usage

```shell
python3 gateway.py
```

Or for development:

```shell
nodemon --exec python3 gateway.py
```

## Test

Simple HTTP client with p5.js

https://editor.p5js.org/prossel/sketches/fxODyCmxV

## Improvements

The initial version is enough for the project that initiated it. However it would be nice to further improve it to make it more generic.

- Auto detect last serial port
- Support a list of possible serial port
- Set the configuration from the command line
- Set the configuration from a file
- Serial configuration controlled by the websocket client
- ...

Don't hesitate to send your pull requests.
