# backend/agent.py

from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions, ConversationItemAddedEvent
from livekit.plugins import (
    openai,
    noise_cancellation,
)
from livekit.agents.llm import ImageContent, AudioContent
from openai import AsyncOpenAI
from datetime import datetime
import asyncio
import os
import traceback

load_dotenv()

# Load system prompt
def load_prompt(file_name):
    try:
        with open(os.path.join('prompts', f'{file_name}.txt'), 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        return "You are a helpful voice assistant."

PROMPT_FILE = 'system_prompt_documentation'
SYSTEM_MESSAGE_doc = load_prompt(PROMPT_FILE)

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="You are a helpful voice AI assistant.")


async def entrypoint(ctx: agents.JobContext):
    conversation_log = []

    async def generate_documentation_from_session(conversation_log):
        if not conversation_log:
            return "No conversation detected. Cannot generate documentation."

        print(conversation_log)
        conversation_text = "\n".join(conversation_log)
        try:
            completion = await client.chat.completions.create(
                model="gpt-4o",  ##gpt-3.5-turbo
                messages=[
                    {"role": "system", "content": SYSTEM_MESSAGE_doc},
                    # *conversation_log,
                    {"role": "user", "content": f"Here is a client onboarding conversation:\n\n{conversation_text}\n\nPlease extract all question-and-answer pairs and generate the structured documentation in Markdown format as previously described."}
                ]
            )
            documentation = completion.choices[0].message.content
            filename = f"livekit_transcripts/documentation.txt"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "w", encoding="utf-8") as f:
                f.write(documentation)
            print("[Shutdown] Documentation saved successfully.")

        except Exception as e:
            print("[Shutdown] Failed to generate documentation.")
            print(f"[Error] {type(e).__name__}: {e}")
            traceback.print_exc()  # optional, prints full traceback

    async def my_shutdown_hook():
        await generate_documentation_from_session(conversation_log)
    ctx.add_shutdown_callback(my_shutdown_hook)

    session = AgentSession(
        llm=openai.realtime.RealtimeModel(
            voice="shimmer",
            model="gpt-4o-mini-realtime-preview-2024-12-17"
        )
    )

    @session.on("conversation_item_added")
    def on_conversation_item_added(event: ConversationItemAddedEvent):
        print(f"Conversation item added from {event.item.role}: {event.item.text_content}. interrupted: {event.item.interrupted}")
        # to iterate over all types of content:
        for content in event.item.content:
            if isinstance(content, str):
                print(f" - text: {content}")
                # conversation_log.append({"role": event.item.role, "content": content}) ##this one was added above the original
                conversation_log.append(f"{event.item.role.capitalize()}: {content}")

            elif isinstance(content, ImageContent):
                # image is either a rtc.VideoFrame or URL to the image
                print(f" - image: {content.image}")
            elif isinstance(content, AudioContent):
                # frame is a list[rtc.AudioFrame]
                print(f" - audio: {content.frame}, transcript: {content.transcript}")
    
    # try:
    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            # LiveKit Cloud enhanced noise cancellation
            # - If self-hosting, omit this parameter
            # - For telephony applications, use `BVCTelephony` for best results
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await ctx.connect()
    # await session.generate_reply(
    #     instructions="Greet the user and began to ask them about the most asked questions they got."
    # )
    await asyncio.Event().wait()  # Keep the session alive until Ctrl+C


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
