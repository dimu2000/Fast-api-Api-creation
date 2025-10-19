# app/routes/blog_tools.py

import json
import logging
import time
from fastapi import APIRouter, Request
from pydantic import ValidationError

# Import our custom modules
from ..models.blog_models import BlogTitles, BlogTitlesWithDescriptions
from ..services import llm_api as llm
from ..services import prompts as pr

# Create a logger to track errors
logger = logging.getLogger("AppLogger")

# Create router (this groups related endpoints)
router = APIRouter()


@router.get("/blog/generate-titles")
async def generate_blog_titles(user_topic: str, request: Request):
    """
    Generate 10 SEO-optimized blog titles for a given topic.
    
    Args:
        user_topic: The blog topic (e.g., "AI Tools for Writers")
        request: FastAPI request object (automatically provided)
    
    Returns:
        JSON response with success status and list of titles
    """
    
    # Start tracking how long this takes
    start_time = time.time()
    
    # Maximum number of retry attempts
    max_retries = 5
    
    # Try up to 5 times (in case of temporary failures)
    for retry_count in range(max_retries):
        try:
            # STEP 1: Check if input contains inappropriate content
            if await llm.is_text_flagged(user_topic):
                return {
                    "success": False,
                    "message": "Input Not Allowed",
                    "result": None
                }
            
            # STEP 2: Format the prompt with user's topic
            prompt = pr.generate_blog_titles.format(topic=user_topic)
            
            # STEP 3: Send to OpenAI and get validated response
            result: BlogTitles = await llm.generate_with_response_model(
                prompt=prompt,
                temperature=1,  # High creativity
                response_model=BlogTitles
            )
            
            # STEP 4: Return success response
            return {
                "success": True,
                "message": "Generated Titles Successfully",
                "result": result.titles
            }
        
        # Handle specific error types
        except (json.JSONDecodeError, ValidationError) as e:
            # JSON parsing failed or data validation failed
            logger.warning(
                f"Failed during JSON decoding or validation. "
                f"Retry count: {retry_count + 1}."
            )
        
        except KeyError as e:
            # Missing expected key in response
            logger.warning(f"Missing key in JSON: {e}")
        
        except Exception as e:
            # Any other unexpected error
            logger.error(e)
            continue
        
        finally:
            # Calculate how long this attempt took
            elapsed_time = time.time() - start_time
            # You could log this or track metrics here
    
    # If all retries failed, return failure response
    return {
        "success": False,
        "message": f"Failed to generate titles after {max_retries} attempts",
        "result": None
    }


@router.get("/blog/generate-blog-ideas")
async def generate_blog_ideas(blog_post_idea: str, tone: str, request: Request):
    """
    Generate 10 blog post ideas with descriptions.
    
    Args:
        blog_post_idea: Topic category (e.g., "Technology Startups")
        tone: Writing tone (e.g., "professional", "casual", "friendly")
    """
    start_time = time.time()
    max_retries = 5

    for retry_count in range(max_retries):
        try:
            # Check for inappropriate content
            if await llm.is_text_flagged(blog_post_idea):
                return {
                    "success": False,
                    "message": "Input Not Allowed",
                    "result": None
                }

            # Format prompt with BOTH parameters
            prompt = pr.generate_blog_post_ideas.format(
                blog_post_idea=blog_post_idea,
                tone=tone
            )
            
            # Call LLM with NEW model
            result: BlogTitlesWithDescriptions = await llm.generate_with_response_model(
                prompt=prompt,
                temperature=1,
                response_model=BlogTitlesWithDescriptions
            )
            
            return {
                "success": True,
                "message": "Generated Blog Ideas Successfully",
                "result": result.titles_with_descriptions
            }

        except (json.JSONDecodeError, ValidationError) as e:
            logger.warning(
                f"Failed during JSON decoding or validation. "
                f"Retry count: {retry_count + 1}."
            )
            
        except KeyError as e:
            logger.warning(f"Missing key in JSON: {e}")
            
        except Exception as e:
            logger.error(e)
            continue
            
        finally:
            elapsed_time = time.time() - start_time

    return {
        "success": False,
        "message": f"Failed to generate blog ideas",
        "result": None
    }