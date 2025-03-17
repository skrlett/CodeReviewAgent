from client import client
import asyncio
from github_utils import fetch_all_commit_sha_of_pr, fetch_commit_diff, post_issue_comment
from prompts import SUMMARIZE_DIFF_PROMPT, SUMMARIZE_PR_PROMPT


async def review_commit_diff(commit_id: str):

    commit_diff = await fetch_commit_diff(commit_id)

    review = client.chat.completions.create(
        model='gpt-4o',
        messages=[{"role": "system", "content": SUMMARIZE_DIFF_PROMPT}, {
            "role": "user", "content": commit_diff}]
    )

    return review.choices[0].message.content


async def review_all_commits_diff(pr_link: str):
    commit_sha_s = await fetch_all_commit_sha_of_pr(pr_link)

    tasks = [review_commit_diff(sha) for sha in commit_sha_s]
    reviews = await asyncio.gather(*tasks)

    pr_summary = client.chat.completions.create(
        model='gpt-4o',
        messages=[{"role": "system", "content": SUMMARIZE_PR_PROMPT}, {
            "role": "user", "content": str(reviews)}]
    )

    return str(pr_summary.choices[0].message.content)

async def post_summary_comment(issue_comment_link: str, pr_link: str):
    reviews = await review_all_commits_diff(pr_link=pr_link)
    await post_issue_comment(issue_comment_link=issue_comment_link, comment=reviews)

