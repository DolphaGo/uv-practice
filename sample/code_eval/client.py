# base dir: samples/python
# target dir: my_client/
# A2A client

import asyncio
import json
from uuid import uuid4

from common.client import A2ACardResolver, A2AClient
from common.types import Task

a2a_server = "http://localhost:10004"
card_resolver = A2ACardResolver(a2a_server)
card = card_resolver.get_agent_card()

print("======= Agent Card ========")
print(json.loads(card.model_dump_json()))
is_streaming = card.capabilities.streaming
print('is_streaming: ', is_streaming)

a2a_client = A2AClient(card)

task_id = uuid4().hex
user_input = "perform a sum function with python code"
payload = {
    "id": task_id,
    "message": {
        "role": "user",
        "parts": [{"type": "text", "text": user_input}],
    },
}


async def send_stream_task():
    response_stream = a2a_client.send_task_streaming(payload)

    async for result in response_stream:
        print(f"Received Agent Event on 'send stream task'")
        parse_stream_result(result)

    print("Agent stream finished.")


async def send_task():
    response = await a2a_client.send_task(payload)
    print(f"Received Agent Event on 'send task'")
    parse_task_result(response)
    print('Agent task finished.')


def parse_task_result(task_result: Task):
    print('parse_task_result')
    finish_Data = json.loads(task_result.model_dump_json(exclude_none=True))
    print(f"Task result: {finish_Data}")

    print('state: ', task_result.result.status.state)
    print('role: ', task_result.result.status.message.role)
    print('message: ', task_result.result.status.message.parts[0].text)


def parse_stream_result(stream_result):
    print('parse_stream_result')
    finish_Data = json.loads(stream_result.model_dump_json(exclude_none=True))

    if finish_Data.get('result').get('artifact'):
        print('artifact: ', finish_Data.get('result').get('artifact').get("parts", [])[0].get("text"))


if __name__ == "__main__":
    print('========= Send Task ========')
    asyncio.run(send_task())

    print()

    print('========= Send Stream Task ========')
    asyncio.run(send_stream_task())