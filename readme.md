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