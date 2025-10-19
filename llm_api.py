# app/services/llm_api.py

import os
import json
from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic import BaseModel
from typing import Type

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

# Use AsyncOpenAI client directly
client = AsyncOpenAI(api_key=openai_api_key)


async def generate_with_response_model(
    prompt: str,
    temperature: float,
    response_model: Type[BaseModel]
) -> BaseModel:
    """
    Generate response with structured output using OpenAI.
    Now with proper max_tokens to avoid truncation!
    """
    
    try:
        # Call OpenAI with JSON mode and sufficient tokens
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that outputs only valid JSON. Always complete your JSON responses fully."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=temperature,
            max_tokens=2000,  # 🔥 CRITICAL: Increase token limit
            response_format={"type": "json_object"}  # 🔥 Forces valid JSON
        )
        
        # Get the response text
        response_text = response.choices[0].message.content
        
        # Parse JSON
        json_data = json.loads(response_text)
        
        # Handle list responses
        if isinstance(json_data, list):
            json_data = {"titles": json_data}
        
        # Validate with Pydantic
        validated_data = response_model(**json_data)
        
        return validated_data
        
    except json.JSONDecodeError as e:
        raise Exception(
            f"Failed to parse JSON response: {e}\n"
            f"Response was: {response_text[:500]}"
        )
    except Exception as e:
        raise Exception(f"Error generating response: {e}")


async def is_text_flagged(input_text: str) -> bool:
    """Check if text contains inappropriate content using OpenAI moderation"""
    
    try:
        # Use synchronous client for moderation
        from openai import OpenAI
        sync_client = OpenAI(api_key=openai_api_key)
        
        moderation_result = sync_client.moderations.create(input=input_text)
        
        return moderation_result.results[0].flagged
        
    except Exception as e:
        print(f"Moderation check failed: {e}")
        return False