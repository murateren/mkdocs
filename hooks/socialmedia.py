from textwrap import dedent
import urllib.parse
import re
import os

x_intent = "https://x.com/intent/tweet?text={text}&url={url}&hashtags={hashtags}&via={via}"
li_share = "https://www.linkedin.com/shareArticle?mini=true&url={url}&title={title}&summary={summary}"

include = re.compile(r"blog/.+/.+")

def on_page_markdown(markdown, **kwargs):
    page = kwargs["page"]
    config = kwargs["config"]

    if not include.match(page.url):
        return markdown

    page_url = config.site_url + page.url
    encoded_url = urllib.parse.quote(page_url)
    title = urllib.parse.quote(page.title)
    summary = urllib.parse.quote(page.meta.get('description', page.title))

    tags = page.meta.get('tags', [])
    hashtags = urllib.parse.quote(",".join([tag.replace(" ", "") for tag in tags]))

    x_url = x_intent.format(
        text=title,
        url=encoded_url,
        hashtags=hashtags,
        via=config.extra.get("x_via", "erenm")
    )

    li_url = li_share.format(
        url=encoded_url,
        title=title,
        summary=summary
    )

    # === ADD THIS BLOCK ===
    # Automatically assign social image if not defined
    if "image" not in page.meta:
        filename = os.path.splitext(os.path.basename(page.file.src_path))[0]
        page.meta["image"] = f"/assets/images/social/{filename}.png"

    return markdown + dedent(f"""
    ---
    **Share this page:**  
    [Share on :simple-x:]({x_url}){{ .md-button style="margin-right: 1em;" }}
    [Share on :material-linkedin:]({li_url}){{ .md-button }}
    """)
