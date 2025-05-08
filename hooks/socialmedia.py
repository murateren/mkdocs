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

    # Fetch tags from YAML metadata
    tags = page.meta.get('tags', [])  # Extract tags from YAML metadata
    # Join tags with commas and URL-encode, handling multi-word tags
    hashtags = urllib.parse.quote(",".join([tag.replace(" ", "%20") for tag in tags]))

    via = "erenm"

    # Final share URLs
    x_url = x_intent.format(text=title, url=encoded_url, hashtags=hashtags, via=via)
    li_url = li_share.format(url=encoded_url, title=title, summary=summary)

    # Meta tags for Open Graph and Twitter
    description = page.meta.get('description', page.title)  # Use description from YAML or fallback to title
    meta_tags = dedent(f"""
    <meta property="og:title" content="{page.title}">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="{config.site_url}{page.url}">
    <meta property="og:type" content="article">
    <meta property="og:image" content="{config.site_url}/assets/images/privacy-pass/cover.webp">
    
    <meta name="twitter:title" content="{page.title}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="{config.site_url}/assets/images/privacy-pass/cover.webp">
    <meta name="twitter:card" content="summary_large_image">
    """)

    # Append meta tags and share buttons
    return markdown + meta_tags + dedent(f"""
    ---
    **Share this page:**

    [Share on :simple-x:]({x_url}){{ .md-button }}
    [Share on :material-linkedin:]({li_url}){{ .md-button }}
    """)
