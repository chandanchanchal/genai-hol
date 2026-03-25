import asyncio
import time
from agents import Agent, Runner, function_tool


ALLOWED_CHANNELS = ["email", "slack", "sms"]


@function_tool
def add_numbers(a: int, b: int) -> str:
    """
    Add two numbers.

    Args:
        a: First number
        b: Second number
    """
    return f"The sum of {a} and {b} is {a + b}"


@function_tool
def get_server_status(server_name: str) -> str:
    """
    Get the current status of a server.

    Args:
        server_name: Name of the server
    """
    mock_status = {
        "web-server-1": "healthy",
        "db-server-1": "critical",
        "cache-server-1": "healthy"
    }

    return mock_status.get(server_name.lower(), "unknown")


@function_tool
def send_alert(channel: str, message: str) -> str:
    """
    Send an operational alert.

    Args:
        channel: Notification channel such as email, slack, or sms
        message: Alert content
    """
    if channel.lower() not in ALLOWED_CHANNELS:
        return f"Alert blocked. Unsupported channel: {channel}"

    if len(message.strip()) == 0:
        return "Alert blocked. Message cannot be empty."

    return f"ALERT SENT via {channel}: {message}"


agent = Agent(
    name="OperationsAssistant",
    instructions=(
        "You are an operations and support assistant.\n"
        "Use tools whenever appropriate.\n"
        "For arithmetic, use the add tool.\n"
        "For server health questions, use the server status tool.\n"
        "For notification requests, use the alert tool.\n"
        "If you do not know the answer, say so clearly.\n"
        "Do not invent unsupported data."
    ),
    tools=[add_numbers, get_server_status, send_alert]
)


async def chat():
    history = []

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() == "exit":
            print("Session ended.")
            break

        history.append({"role": "user", "content": user_input})

        start_time = time.perf_counter()

        result = await Runner.run(agent, history)

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        output = result.final_output
        usage = result.context_wrapper.usage

        print("\nAgent:", output)

        print("\n--- Metrics ---")
        print("Requests made :", usage.requests)
        print("Input tokens  :", usage.input_tokens)
        print("Output tokens :", usage.output_tokens)
        print("Total tokens  :", usage.total_tokens)
        print(f"Time taken    : {elapsed_time:.2f} sec")

        history.append({"role": "assistant", "content": output})


asyncio.run(chat())
