import praw
import utils
import re
import traceback

comment_template = "I found some Google AMP links in your comment. Here are the normal links:\n\n " \
                   "{links}\n\n " \
                   "Beep Boop, I'm a bot. If I made an error or if you have any questions, my " \
                   "[creator](https://reddit.com/u/6b86b3ac03c167320d93) might check my messages.  \n " \
                   "[Source Code](https://github.com/laurinneff/no-google-amp-bot) | [Issues](" \
                   "https://github.com/laurinneff/no-google-amp-bot/issues) "
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

    out = '- '
    if fixed_arr:
        out += '\n- '.join(fixed_arr)
        print(f'Comment by {comment.author} with ID {comment.id} (https://reddit.com{comment.permalink})')
        reply_body = comment_template.format(links=out)
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
