import logging
from fastapi import FastAPI, Request
import asyncio

from reviewer import review_all_commits_diff, review_commit_diff, post_summary_comment
from session import GitHubSession

app = FastAPI()


@app.get("/ping")
def ping():
    return {"status": "alive"}


@app.post("/webhook")
async def github_webhook(request: Request):
    """Handles GitHub webhook events"""
    payload = await request.json()
    pr_link = payload["pull_request"]["url"]
    comments_link = payload["pull_request"]["comments_url"]

    # Log the incoming event
    logging.info(f"Received GitHub Webhook: {payload}")

    # Handle "ping" event (when webhook is created)
    if "hook" in payload:
        return {"message": "Webhook setup successful!"}

    if pr_link:
        asyncio.create_task(post_summary_comment(
            pr_link=pr_link, issue_comment_link=comments_link))
        logging.info(f"pr_link: {pr_link}")
        return {"PR Review": "Processing PR Request"}

    return {"message": "Event received, but no action taken"}

if __name__ == "__main__":
    import uvicorn
    from github_utils import fetch_commit_diff

    uvicorn.run(app, host="0.0.0.0", port=8080)
