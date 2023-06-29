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
        data = await reader.read(100)
        # checks data stream so server doesn't crash and wait for data finish sending
        if not data:
            break
        print("new connection accepted ! ")
        writer.write(b"+PONG\r\n")


if __name__ == "__main__":
    asyncio.run(main())
