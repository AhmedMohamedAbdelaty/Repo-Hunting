#!/usr/bin/env python3
"""
GitHub Repository Search Tool
Fetch random GitHub repositories with advanced filtering options.
"""

import os
import sys
import requests
import argparse
import random
from datetime import datetime, timedelta
from typing import Optional, List, Dict

# Time period mappings
TIME_PERIODS = {
    "1week": 7,
    "2weeks": 14,
    "1month": 30,
    "3months": 90,
    "6months": 180,
    "1year": 365,
    "2years": 730,
    "5years": 1825,
}


def parse_time_period(period_str: str) -> Optional[str]:
    """
    Convert time period string to ISO date format.

    Args:
        period_str: Either a predefined period (e.g., "3months") or date (YYYY-MM-DD)

    Returns:
        ISO formatted date string or None if invalid
    """
    if not period_str:
        return None

    # Check if it's a predefined period
    if period_str.lower() in TIME_PERIODS:
        days_ago = TIME_PERIODS[period_str.lower()]
        target_date = datetime.now() - timedelta(days=days_ago)
        return target_date.strftime("%Y-%m-%d")

    # Try to parse as exact date
    try:
        datetime.strptime(period_str, "%Y-%m-%d")
        return period_str
    except ValueError:
        print(f"Error: Invalid date format '{period_str}'. Use YYYY-MM-DD or predefined periods.")
        return None


def build_search_query(
    language: Optional[str] = None,
    min_stars: Optional[int] = None,
    max_stars: Optional[int] = None,
    since_date: Optional[str] = None,
    exclude_archived: bool = False,
    exclude_forks: bool = False,
) -> str:
    """
    Build GitHub search query string.

    Args:
        language: Programming language filter
        min_stars: Minimum star count
        max_stars: Maximum star count
        since_date: Last push date filter (ISO format)
        exclude_archived: Whether to exclude archived repositories
        exclude_forks: Whether to exclude forked repositories

    Returns:
        Formatted query string for GitHub API
    """
    query_parts = []

    if language:
        query_parts.append(f"language:{language}")

    # Build stars range
    if min_stars is not None and max_stars is not None:
        query_parts.append(f"stars:{min_stars}..{max_stars}")
    elif min_stars is not None:
        query_parts.append(f"stars:>={min_stars}")
    elif max_stars is not None:
        query_parts.append(f"stars:<={max_stars}")

    if since_date:
        query_parts.append(f"pushed:>={since_date}")

    if exclude_archived:
        query_parts.append("archived:false")

    if exclude_forks:
        query_parts.append("fork:false")

    return " ".join(query_parts)


def fetch_repositories(
    query: str,
    num_repos: int,
    github_token: Optional[str] = None,
    sort_by: str = "stars"
) -> List[Dict]:
    """
    Fetch repositories from GitHub API.

    Args:
        query: Search query string
        num_repos: Number of repositories to fetch
        github_token: Optional GitHub personal access token
        sort_by: Sort criteria (stars, forks, updated)

    Returns:
        List of repository dictionaries
    """
    base_url = "https://api.github.com/search/repositories"

    headers = {}
    if github_token:
        headers["Authorization"] = f"token {github_token}"

    params = {
        "q": query,
        "sort": sort_by,
        "order": "desc",
        "per_page": 100  # Max per page
    }

    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Check for API rate limit
        if response.status_code == 403:
            print("Error: GitHub API rate limit exceeded.")
            print("Consider using a GitHub token with --github-token")
            sys.exit(1)

        repos = data.get("items", [])

        if not repos:
            print("No repositories found matching the criteria.")
            return []

        if len(repos) < num_repos:
            print(f"Note: Only {len(repos)} repositories found (requested {num_repos})")

        # Shuffle for randomness and select requested number
        random.shuffle(repos)
        return repos[:num_repos]

    except requests.exceptions.RequestException as e:
        print(f"Error fetching repositories: {e}")
        sys.exit(1)


def display_repository(repo: Dict, index: int) -> None:
    """
    Display repository information in a formatted way.

    Args:
        repo: Repository dictionary from GitHub API
        index: Repository index for display
    """
    print(f"\n{'='*60}")
    print(f"Repository #{index}")
    print(f"{'='*60}")
    print(f"Name:         {repo['name']}")
    print(f"Owner:        {repo['owner']['login']}")
    print(f"Stars:        {repo['stargazers_count']:,}")
    print(f"Forks:        {repo['forks_count']:,}")
    print(f"Language:     {repo.get('language', 'N/A')}")
    print(f"Last Push:    {repo['pushed_at']}")
    print(f"Created:      {repo['created_at']}")
    print(f"Archived:     {'Yes' if repo.get('archived', False) else 'No'}")

    # Display description if available
    description = repo.get('description', '')
    if description:
        # Truncate long descriptions
        if len(description) > 100:
            description = description[:97] + "..."
        print(f"Description:  {description}")

    print(f"URL:          {repo['html_url']}")
    print(f"{'='*60}")


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Get random GitHub repositories with advanced filtering.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Time Period Options:
  {', '.join(TIME_PERIODS.keys())}
  Or use exact date: YYYY-MM-DD

Examples:
  %(prog)s --language python --min-stars 100 --num-repos 5
  %(prog)s --language javascript --since 3months --exclude-archived
  %(prog)s --min-stars 500 --max-stars 4000 --since 1year --num-repos 20
        """
    )

    parser.add_argument(
        "--language",
        help="Programming language filter (e.g., python, javascript, go)"
    )
    parser.add_argument(
        "--min-stars",
        type=int,
        help="Minimum number of stars"
    )
    parser.add_argument(
        "--max-stars",
        type=int,
        help="Maximum number of stars"
    )
    parser.add_argument(
        "--since",
        help=f"Last push since period or date. Options: {', '.join(TIME_PERIODS.keys())} or YYYY-MM-DD"
    )
    parser.add_argument(
        "--num-repos",
        type=int,
        default=5,
        help="Number of repositories to retrieve (default: 5)"
    )
    parser.add_argument(
        "--exclude-archived",
        action="store_true",
        help="Exclude archived repositories"
    )
    parser.add_argument(
        "--exclude-forks",
        action="store_true",
        help="Exclude forked repositories"
    )
    parser.add_argument(
        "--sort-by",
        choices=["stars", "forks", "updated"],
        default="stars",
        help="Sort repositories by (default: stars)"
    )
    parser.add_argument(
        "--github-token",
        help="GitHub personal access token (or set GITHUB_TOKEN env var)"
    )

    args = parser.parse_args()

    # Validate inputs
    if args.min_stars and args.max_stars and args.min_stars > args.max_stars:
        print("Error: min-stars cannot be greater than max-stars")
        sys.exit(1)

    if args.num_repos <= 0:
        print("Error: num-repos must be greater than 0")
        sys.exit(1)

    # Parse time period
    since_date = parse_time_period(args.since) if args.since else None
    if args.since and since_date is None:
        sys.exit(1)

    # Get GitHub token from args or environment
    github_token = args.github_token or os.environ.get("GITHUB_TOKEN")

    # Build search query
    query = build_search_query(
        language=args.language,
        min_stars=args.min_stars,
        max_stars=args.max_stars,
        since_date=since_date,
        exclude_archived=args.exclude_archived,
        exclude_forks=args.exclude_forks,
    )

    if not query:
        print("Error: At least one filter must be specified")
        parser.print_help()
        sys.exit(1)

    print(f"Searching GitHub with query: {query}")
    print(f"Fetching {args.num_repos} random repositories...\n")

    # Fetch repositories
    repos = fetch_repositories(
        query=query,
        num_repos=args.num_repos,
        github_token=github_token,
        sort_by=args.sort_by
    )

    # Display results
    if repos:
        for idx, repo in enumerate(repos, 1):
            display_repository(repo, idx)

        print(f"\n✓ Successfully retrieved {len(repos)} repositories")
    else:
        print("No repositories found matching your criteria.")


if __name__ == "__main__":
    main()
