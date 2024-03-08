from flask import Flask, render_template
import openai
import os
import markdown2
from dotenv import load_dotenv
from markupsafe import Markup  # Import Markup from markupsafe

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

@app.route('/blog/<article_title>')
def blog(article_title):
    # Replace dashes with spaces and capitalize for prompt
    formatted_title = article_title.replace('-', ' ').title()

    # Set OpenAI API key from environment variable
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Generate content in Markdown using OpenAI GPT-3.5 Turbo
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[{"role": "system", "content": "You are a creative writer who writes in Markdown format."},
                  {"role": "user", "content": f"Write a blog article in Markdown about {formatted_title}."}]
    )
    markdown_content = response.choices[0].message["content"]

    # Convert Markdown to HTML
    html_content = markdown2.markdown(markdown_content)

    # Mark the HTML content as safe
    safe_html_content = Markup(html_content)

    # Render the template with the title and safe HTML content
    return render_template('blog_template.html', title=formatted_title, content=safe_html_content)

if __name__ == '__main__':
    app.run(debug=True)
