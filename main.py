from flask import Flask, render_template, request
import openai
import os
import markdown2
from dotenv import load_dotenv
from markupsafe import Markup  # Import Markup from markupsafe
from urllib.parse import unquote
import csv
from io import StringIO

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def main():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[{"role": "system", "content": "You are a creative writer."},
                  {"role": "user", "content": "Create a list separated by new lines of 5 interesting article titles about different topics for a blog website. Do not put numbers before the aritcle titles, quotes, or any other unnecessary formatting aside from the new lines between titles. These can be top 10 lists, informational articles, etc."}]
    )

    csv_data = response.choices[0].message["content"]
    articles_list = [item for item in csv_data.splitlines()]

    print(articles_list)

    return render_template('main.html', articles_list=articles_list)

@app.route('/search/')
def search():
    query = unquote(request.args.get('query', ''))

    print(query)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[{"role": "system", "content": "You are a creative writer."},
                  {"role": "user", "content": f"Create a list separated by new lines of 5 interesting article titles about the topic '{query}'. The titles must be about that topic. Nothing else. Do not put numbers before the aritcle titles, quotes, or any other unnecessary formatting aside from the new lines between titles. These can be top 10 lists, informational articles, etc."}]
    )

    csv_data = response.choices[0].message["content"]
    articles_list = [item.strip('"') for item in csv_data.splitlines()]

    print(articles_list)

    return render_template('search.html', search=query, articles_list=articles_list)

@app.route('/blog/<article_title>')
def blog(article_title):
    # Replace dashes with spaces and capitalize for prompt
    formatted_title = unquote(article_title).title()

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
    return render_template('blog_template.html', title=formatted_title, image=image_url, content=safe_html_content)

if __name__ == '__main__':
    app.run(debug=True)
