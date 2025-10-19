generate_blog_titles = """I want you to act as a professional blog titles generator. 
Think of titles that are seo optimized and attention-grabbing at the same time,
and will encourage people to click and read the blog post.
They should also be creative and clever.
Try to come up with titles that are unexpected and surprising.
Do not use titles that are too generic, or titles that have been used too many times before. 
I want to generate 10 titles maximum.
My blog post is about {topic}
                                 
IMPORTANT: The output should be json array of 10 titles without field names. just the titles! Make Sure the JSON is valid.
                                                  
Example Output:
[
    "Title 1",
    "Title 2",
    "Title 3",
    "Title 4",
    "Title 5",
    "Title 6",
    "Title 7",
    "Title 8",
    "Title 9",
    "Title 10"
]"""



# NEW: Add second prompt
generate_blog_post_ideas = """As an expert blog writer, Please generate a list of 10 creative and engaging blog post ideas for a {blog_post_idea} that will attract young readers.
The ideas should focus on latest industry trends, innovative technology solutions, startup culture, and success stories.
Each idea should have a brief description explaining the angle and potential content that could be covered.
Ensure the topics are current, relevant, and have the potential to capture the audience's interest and drive engagement.
The tone and writing style should be {tone} tone.

IMPORTANT: Output should be valid JSON format like this:
{{
    "titles_with_descriptions": [
        {{
            "title": "Blog Post Title Here",
            "description": "Brief description of the blog post idea"
        }}
    ]
}}
"""