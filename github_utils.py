from config import setup_logging
from session import GitHubSession
from constants import GITHUB_API_KEY, GITHUB_BASE_URL, GITHUB_USER_AGENT, GITHUB_ACCEPT_JSON_HEADER, GITHUB_ACCEPT_DIFF_HEADER

logger = setup_logging(__name__)


async def fetch_all_commit_sha_of_pr(pr_link: str) -> list[str]:
    """Fetch all commit IDs from a given pull request link.

    Args:
        pr_link (str): The link to the pull request.

    Returns:
        list[str]: A list of https commit SHAs.
    """
    headers = {
        "Authorization": f"Bearer {GITHUB_API_KEY}",
        "Accept": GITHUB_ACCEPT_JSON_HEADER,
        "User-Agent": GITHUB_USER_AGENT
    }

    logger.info(f"Getting all commit SHA for {pr_link}")

    session = await GitHubSession.get_session(headers=headers)

    commits_link = f"{pr_link}/commits"
    async with session.get(commits_link) as response:
        commits = await response.json()

    commit_sha_s = [commit["sha"] for commit in commits]

    logger.info(f"Got all commit SHAs from PR {pr_link}")

    return commit_sha_s


async def fetch_commit_diff(commit_id_sha: str) -> str:
    """
    Fetch diff for the given commit_id_sha

    Args: 
        commit_id_sha (str): commit SHA

    Returns:
        str: The diff of the commit
    """

    headers = {
        "Authorization": f"Bearer {GITHUB_API_KEY}",
        "Accept": GITHUB_ACCEPT_DIFF_HEADER,
        "User-Agent": GITHUB_USER_AGENT
    }

    logger.info(f"Fetching diff of commit {commit_id_sha}")
    session = await GitHubSession.get_session(headers=headers)

    commit_link = f"{GITHUB_BASE_URL}/repos/skrlett/test/commits/{commit_id_sha}"

    async with session.get(commit_link) as response:
        commit_diff = await response.read()

    logger.info(f"Fetched diff of commit {commit_id_sha}")

    return str(commit_diff)

async def post_issue_comment(issue_comment_link: str, comment: str):
    """
    Make a POST request to the PR issue like

    Args:
        issue_link (str): PR issue comments link
    
        Returns:
            None
    """

    headers = {
        "Authorization": f"Bearer {GITHUB_API_KEY}",
        "Accept": GITHUB_ACCEPT_JSON_HEADER,
        "User-Agent": GITHUB_USER_AGENT
    }

    session = await GitHubSession.get_session(headers=headers)

    logger.info(f"Posting comment {comment}")

    try:
        payload = {"body": comment}
        response = await session.post(issue_comment_link, json=payload)
        logger.info("Posted the comment")
    except:
        logger.error(f"Failed to post comment to {issue_comment_link}", exc_info=True)
