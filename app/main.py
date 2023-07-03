import socket
import asyncio

PORT = 6379
HOST = "localhost"

async def main():
    print("Logs from your program will appear here!")

    # use asyncio to start a socket server
    # then call an async function to return PONG
    server = await asyncio.start_server(handler, "localhost", 6379, limit=4096, reuse_port=True)

    async with server:
        await server.serve_forever()

# this handler needs the while loop to keep opening for requests
async def handler(reader, writer):
    while True:    
        print("new connection accepted ! ")    
        data = await reader.read(100)
        # checks data stream so server doesn't crash and wait for data finish sending
        if not data:
            break

        lst = data.split()
        # cheating PING command with this case
        if data == b'*1\r\n$4\r\nping\r\n':
            writer.write(b'+PONG\r\n')
        else:
            echo_idx = lst.index(b'echo')
            return_lst = lst[(echo_idx+1):]
            parsed_str = parse(return_lst)
            writer.write(bytes(parsed_str, encoding='utf-8'))

def parse(lst):
    """"
    parse input list of bytes to a byte string that echo returns, in redis protocol
    """
    length = 0
    return_s = ""

    for byte_s in lst:
        return_s+=bytes.decode(byte_s)+'\r\n'
        if bytes.decode(byte_s)[0] != "$":
            length += 1
    
    return "*" + str(length) + '\r\n' + return_s

if __name__ == "__main__":
    asyncio.run(main())
