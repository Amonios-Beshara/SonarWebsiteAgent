# backend/agent.py

from livekit.api.access_token import AccessToken, VideoGrants
import os
from openai import OpenAI

client = OpenAI()

def create_livekit_token(room_name: str):
    api_key = os.getenv("LIVEKIT_API_KEY")
    api_secret = os.getenv("LIVEKIT_API_SECRET")

    grant = VideoGrants(room=room_name, room_join=True)
    at = AccessToken(api_key, api_secret)
    at.with_identity("client_user")
    at.with_grants(grant)

    return at.to_jwt()

async def handle_transcript_to_faq(transcript: str) -> str:
    system_prompt = """
    You are an expert at creating FAQ documentation.
    You receive a conversation transcript in Egyptian Arabic.
    Extract clear Q&A pairs from the conversation.
    Return them as:
    Q: ...
    A: ...
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": transcript}
        ]
    )
    return response.choices[0].message.content.strip()
