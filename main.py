import praw
import utils
import re
import traceback

comment_template_single = "Non-AMP Link: {links}\n\n" \
                          "I'm a bot. [Why?](https://reddit.com/user/NoGoogleAMPBot/comments/lbz2sg/faq/) " \
                          "| [Code](https://github.com/laurinneff/no-google-amp-bot) " \
                          "| [Report issues](https://github.com/laurinneff/no-google-amp-bot/issues)"
comment_template_multi = "Non-AMP Links:\n\n" \
                         "{links}\n\n" \
                         "I'm a bot. [Why?](https://reddit.com/user/NoGoogleAMPBot/comments/lbz2sg/faq/) " \
                         "| [Code](https://github.com/laurinneff/no-google-amp-bot) " \
                         "| [Report issues](https://github.com/laurinneff/no-google-amp-bot/issues)"

link_regex = r'\[([^\[\]\(\)]+)\]\((https?:\/\/[\w\d./?=#%+&-]+)\)'
implicit_link_regex = r'(?<!\()https?:\/\/[\w\d./?=#%+&-]+(?!\))'

reddit = praw.Reddit('anti-amp')

subreddit = reddit.subreddit("all")


def process_comments(comment):
    # Shouldn't reply to own comments, since these links are already fixed
    if comment.author == reddit.user.me().name:
        return

    links = re.findall(link_regex, comment.body)

    fixed_arr = []

    if links:
        for link in links:
            fixed = process_link(link)
            if fixed:
                fixed_arr.append(fixed)
    links = re.findall(implicit_link_regex, comment.body)
    if links:
        for link in links:
            fixed = process_link(link, True)  # Implicit links show the URL as text
            if fixed:
                fixed_arr.append(fixed)

    out = '- ' if len(fixed_arr) > 1 else ""
    if fixed_arr:
        out += '\n- '.join(fixed_arr) if len(fixed_arr) > 1 else fixed_arr[0]
        print(f'Comment by {comment.author} with ID {comment.id} (https://reddit.com{comment.permalink})')
        reply_body = comment_template_multi.format(links=out) if len(fixed_arr) > 1 else comment_template_single.format(links=out)
        print(reply_body)
        reply = comment.reply(reply_body)
        print(f'Reply: https://reddit.com{reply.permalink}')


def process_link(link, implicit=False):
    if not implicit:
        text = link[0]
        url = link[1]
    else:
        text = link
        url = link
    if utils.is_amp(url):
        fixed = utils.amp_to_normal(url)
        # Sometimes, amp_to_normal returns Google redirects (https://www.google.com/url?q=...)
        if utils.is_google_redirect(fixed):
            fixed = utils.follow_google_redirect(fixed)
        if implicit:
            text = fixed
        return "[{text}]({fixed})".format(text=text, fixed=fixed)


print("Anti AMP Bot is running!")
for comment in subreddit.stream.comments():
    try:
        process_comments(comment)
    except Exception as e:
        print('Error:', e, f'Comment: https://reddit.com{comment.permalink}')
        traceback.print_tb(e.__traceback__)
