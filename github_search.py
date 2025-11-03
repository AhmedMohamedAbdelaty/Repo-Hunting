#!/usr/bin/env python3
"""
GitHub Repository Search Module
Core search functionality for GitHub API
"""

import os
import sys
import requests
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
        return None


def build_search_query(
    language: Optional[str] = None,
    topics: Optional[List[str]] = None,
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
        topics: List of topics/tags to filter by
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

    # Add topics
    if topics:
        for topic in topics:
            if topic.strip():
                query_parts.append(f"topic:{topic.strip()}")

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
) -> Dict:
    """
    Fetch repositories from GitHub API.

    Args:
        query: Search query string
        num_repos: Number of repositories to fetch
        github_token: Optional GitHub personal access token
        sort_by: Sort criteria (stars, forks, updated)

    Returns:
        Dictionary with 'success', 'repos', 'error', 'total_count'
    """
    base_url = "https://api.github.com/search/repositories"

    headers = {}
    if github_token:
        headers["Authorization"] = f"token {github_token}"

    params = {
        "q": query,
        "sort": sort_by,
        "order": "desc",
        "per_page": min(100, num_repos)  # Max per page is 100
    }

    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=10)

        # Check for API rate limit
        if response.status_code == 403:
            return {
                "success": False,
                "error": "GitHub API rate limit exceeded. Consider using a GitHub token.",
                "repos": [],
                "total_count": 0
            }

        response.raise_for_status()
        data = response.json()

        repos = data.get("items", [])
        total_count = data.get("total_count", 0)

        if not repos:
            return {
                "success": True,
                "repos": [],
                "total_count": 0,
                "message": "No repositories found matching the criteria."
            }

        # Shuffle for randomness and select requested number
        random.shuffle(repos)
        selected_repos = repos[:num_repos]

        return {
            "success": True,
            "repos": selected_repos,
            "total_count": total_count,
            "query": query
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Error fetching repositories: {str(e)}",
            "repos": [],
            "total_count": 0
        }


def format_repository(repo: Dict) -> Dict:
    """
    Format repository data for display/export.

    Args:
        repo: Repository dictionary from GitHub API

    Returns:
        Formatted repository dictionary
    """
    return {
        "name": repo['name'],
        "full_name": repo['full_name'],
        "owner": repo['owner']['login'],
        "stars": repo['stargazers_count'],
        "forks": repo['forks_count'],
        "language": repo.get('language', 'N/A'),
        "description": repo.get('description', ''),
        "url": repo['html_url'],
        "homepage": repo.get('homepage', ''),
        "topics": repo.get('topics', []),
        "created_at": repo['created_at'],
        "updated_at": repo['updated_at'],
        "pushed_at": repo['pushed_at'],
        "archived": repo.get('archived', False),
        "open_issues": repo.get('open_issues_count', 0),
        "watchers": repo.get('watchers_count', 0),
        "license": repo.get('license', {}).get('name', 'N/A') if repo.get('license') else 'N/A'
    }
