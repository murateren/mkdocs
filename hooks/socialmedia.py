from textwrap import dedent
import urllib.parse
import re

x_intent = "https://x.com/intent/tweet?text={text}&url={url}&hashtags={hashtags}&via={via}"
li_sharer = (
    "https://www.linkedin.com/shareArticle?mini=true"
    "&url={url}"
    "&title={title}"
    "&summary={summary}"
)

include = re.compile(r"blog/[1-9].*")

def on_page_markdown(markdown, **kwargs):
    page = kwargs['page']
    config = kwargs['config']
    if not include.match(page.url):
        return markdown

    page_url = config.site_url + page.url
    page_title = urllib.parse.quote(page.title + '\n')  # Page title
    summary = urllib.parse.quote(page.summary if hasattr(page, 'summary') else page.title)  # Summary (use title if no summary available)
    hashtags = urllib.parse.quote("privacy,protocol")  # Example hashtags
    via = "YourXHandle"  # Your X/Twitter handle

    # Format share URL for X (Twitter)
    share_url = x_intent.format(text=page_title, url=page_url, hashtags=hashtags, via=via)

    # Format share URL for LinkedIn
    linkedin_url = li_sharer.format(url=page_url, title=page_title, summary=summary)

    return markdown + dedent(f"""
    [Share on :simple-x:]({share_url}){{ .md-button }}
    [Share on :material-linkedin:]({linkedin_url}){{ .md-button }}
    """)
