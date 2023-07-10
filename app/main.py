import socket
import asyncio

PORT = 6379
HOST = "localhost"
mem = {}

async def main():
    print("Logs from your program will appear here!")

    # use asyncio to start a socket server
    # then call an async function to return PONG
    server = await asyncio.start_server(handler, "localhost", 6379, limit=4096, reuse_port=True)

    async with server:
        await server.serve_forever()

# this handler needs the while loop to keep opening for requests
# takes socket data in redis protocol, and set/get if needed, and 
# writes response
async def handler(reader, writer):
    while True:    
        print("new connection accepted ! ")    
        data = await reader.read(100)
        # checks data stream so server doesn't crash and wait for data finish sending
        if not data:
            break

        lst = parse(data)
        # cheating PING command with this case
        if data == b'*1\r\n$4\r\nping\r\n':
            writer.write(b'+PONG\r\n')
        elif 'echo' in lst:
            print(lst)
            writer.write(bytes('+' + lst[4] + '\r\n', encoding='utf-8'))
        elif 'set' in lst:
            mem[lst[4]] = lst[6]
            print(mem)
            writer.write(b'+OK\r\n')
        elif 'get' in lst:
            if lst[4] in mem:
                value = mem[lst[4]]
                writer.write(bytes('+' + value +'\r\n', encoding='utf-8'))
            else:
                writer.write(bytes("-1\r\n", "utf-8"))

            

# decode b'*3\r\n$3\r\nset\r\n$1\r\na\r\n$1\r\n3\r\n' into list of strings
def parse(lst):
    """"
    parse input list of bytes to a byte string that echo returns, in redis protocol
    """
    decoded_slst = []
    split_list = lst.split()
    for s in split_list:
        s = bytes.decode(s)
        decoded_slst.append(s)
    
    print(decoded_slst)
    return decoded_slst

def parse_simple_string(lst):
    """
    return the single full string of echo command
    """
    s = bytes.decode(lst[1])
    return "+" + s + "\r\n"


if __name__ == "__main__":
    asyncio.run(main())
