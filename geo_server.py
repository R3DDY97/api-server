#!/usr/bin/env python3
'''simple and light api server'''

import os
import asyncio
from geo_app import  (load_database, create_response_body)

def parse_request_header(req_header_stream):
    req_line, *header_lines = req_header_stream.split("\r\n")
    req_header = dict(zip(["method", "path", "version"], req_line.split()))
    req_header["header"] = dict([hdr.split(": ") for hdr in header_lines if ":" in hdr])
    query = req_header["path"].strip("/")
    print(req_line, query)
    if query:
        return query
    return None

def create_response(req_query):
    response_body = create_response_body(req_query).encode()
    print(response_body)
    response_hdr = b"HTTP/1.1 200 OK\r\n\r\n"
    response = response_hdr + response_body
    return response

async def http_server(reader, writer):
    req_header_stream = await reader.readuntil(b"\r\n\r\n")
    req_header_stream = req_header_stream.decode()
    req_query = parse_request_header(req_header_stream)
    response = create_response(req_query)
    writer.write(response)
    await writer.drain()
    writer.close()

def run_server(host="0.0.0.0", port=8000, loop=None):

    loop = asyncio.get_event_loop()
    single_request = asyncio.start_server(http_server, host, port)
    api_server = loop.run_until_complete(single_request)
    print("\n started API server and listening on \n")
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("\nShutting down api server\n")
    # except IncompleteReadError:
    #     pass
    api_server.close()
    loop.run_until_complete(api_server.wait_closed())
    loop.close()



if __name__ == '__main__':
    os.system("clear||cls")
    GEO_DICT = load_database()
    run_server()
