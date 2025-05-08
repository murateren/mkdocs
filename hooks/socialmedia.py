from textwrap import dedent
import urllib.parse
import re

# Share URL templates
x_intent = "https://x.com/intent/tweet?text={text}&url={url}&hashtags={hashtags}&via={via}"
li_share = "https://www.linkedin.com/shareArticle?mini=true&url={url}&title={title}&summary={summary}"

# Match only certain pages, e.g., blog entries
include = re.compile(r"blog/.*")

def on_page_markdown(markdown, **kwargs):
    page = kwargs["page"]
    config = kwargs["config"]

    if not include.match(page.url):
        return markdown

    # Encode components
    page_url = config.site_url + page.url
    encoded_url = urllib.parse.quote(page_url)
    title = urllib.parse.quote(page.title)
    summary = title
    hashtags = urllib.parse.quote("privacy,security")
    via = "erenm"

    # Final share URLs
    x_url = x_intent.format(text=title, url=encoded_url, hashtags=hashtags, via=via)
    li_url = li_share.format(url=encoded_url, title=title, summary=summary)

    # Append share buttons
    return markdown + dedent(f"""
    ---
    **Share this page:**

    [Share on :simple-x:]({x_url}){{ .md-button }}
    [Share on :material-linkedin:]({li_url}){{ .md-button }}
    """)
