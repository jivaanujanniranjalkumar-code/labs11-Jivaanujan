import asyncio
import socket


async def gather_doubled(numbers):
    # Outline:
    #   1. Create an async helper that returns n * 2.
    #   2. Use asyncio.gather to run one task per number concurrently in order.
    async def double(n):
        return n * 2

    return list(await asyncio.gather(*(double(n) for n in numbers)))


async def fastest(jobs):
    # Outline:
    #   1. Create a task for each (label, delay) that sleeps and returns label.
    #   2. Use asyncio.as_completed to get and return the first finished label.
    async def run(label, delay):
        await asyncio.sleep(delay)
        return label

    tasks = [asyncio.create_task(run(label, delay)) for label, delay in jobs]
    for task in asyncio.as_completed(tasks):
        result = await task
        for t in tasks:
            t.cancel()
        return result


def echo_once(host, port, message):
    # Outline:
    #   1. Open a TCP socket and connect to (host, port).
    #   2. Send encoded message, receive reply, and return decoded string.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(message.encode())
        return s.recv(4096).decode()


def main():
    print(asyncio.run(gather_doubled([1, 2, 3, 4])))
    print(asyncio.run(fastest([("slow", 0.3), ("fast", 0.05)])))


if __name__ == "__main__":
    main()
