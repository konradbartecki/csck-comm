# csck-comm

Simple client-server communication app with encryption written in Python.

## Architecture Decision Log

### `ADL-1` - Basic concepts

We expect the code to share a great portion of logic in between server and client, so because of that, ideally this app should behave like a single executable with ability to configure whether to run the app in the `client` or `server` mode.

For testing `pytest` should be used.
This repository was already configured with GitHub workflows to run tests on each commit.

For encryption, we could try to use [age](https://github.com/FiloSottile/age) which is a modern version of public-private key encryption inspired by PGP.

Settings should be stored in a `.json` file which should be a key-value dictionary.

App requirements:
 - Ability to listen and accept for TCP/IP connections
 - Ability to connect to servers listening to TCP/IP connections
 - Ability to send generated data over TCP/IP
 - Ability to send files over TCP/IP
 - Support error handling
 - Support for optional encryption
 - Support for data types
   - Plain text
   - XML
   - JSON
   - Binary
 - Ability for the app to be configured through settings file
 - No hard-coding within the app.
 - Command line arguments would be a good-to-have feature, but it is not required.

### `ADL-2` Message standard

In this project we are using TCP/IP thus everything that we send will be converted to bytes first, then sent over TCP/IP.
We have to do this for all of the formats that we have to support, meaning `plain_text, xml, json, binary`.
Because of that I think it makes sense to implement a very small subset of HTTP 1.1 protocol.

We would support POST request only.

Message format would look like follows:
```http
POST\n
HeaderName: value\n
Content-Type: application/xml\n
Content-Length: 1234 (length in bytes)\n
Content-Encoding: utf-8\n
\n
\n 
(raw content of length 1234 bytes)
```

Meaning that the first lines would be reserved for headers.
Each header would be separated by a new line `\n` character.
Then the actual content of the message will follow after a double whitespace character combination `\n\n`.

So for example:
```http request
CSCK-COMM/v1 POST
Content-Type: application/json
Content-Length: 1234


{
  "Mode" : "Client",
  "TransferDataType": "PlainText",
  "WorkingDirectory" : "./tmp",
  "TargetAddress" : "127.0.0.1",
  "TargetPort" : "9545",
  "ListenAddress" : "0.0.0.0",
  "ListenPort" : "9545"
}
```

This would allow us to send metadata/headers along with the actual content of the message easily which would be useful for example to indicate that attached content is encrypted or not.