import socket
import asyncio
import time

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
            # set expiring time in a tuple only if px is in command
            if 'px' in lst:
                exp_time = time.time() * 1000 + int(lst[10])
                mem[lst[4]] = (lst[6], exp_time)
                print(mem)
                writer.write(b'+OK\r\n')
            else:
                mem[lst[4]] = lst[6]
                writer.write(b'+OK\r\n')

        elif 'get' in lst:
            if lst[4] not in mem:
                # return error to redis client
                writer.write(bytes("-1\r\n", "utf-8"))

            # time exp is set
            elif type(mem[lst[4]]) is tuple:
                print(mem)
                print(lst)
                # if key in mem and exp_time is less than current time, return value
                if lst[4] in mem and time.time() * 1000 <= mem[lst[4]][1]:
                    value = mem[lst[4]][0]
                    writer.write(bytes('+' + value +'\r\n', encoding='utf-8'))
                else:
                    print(mem)
                    print(lst)
                    writer.write(bytes("-1\r\n", "utf-8"))

            # time exp is not set
            elif lst[4] in mem:
                value = mem[lst[4]]
                writer.write(bytes('+' + value +'\r\n', encoding='utf-8'))

                

            

def parse(lst):
    """
    decode b'*3\r\n$3\r\nset\r\n$1\r\na\r\n$1\r\n3\r\n' into list of strings
    """
    decoded_slst = []
    split_list = lst.split()
    for s in split_list:
        s = bytes.decode(s)
        decoded_slst.append(s)
    
    print(decoded_slst)
    return decoded_slst


if __name__ == "__main__":
    asyncio.run(main())
