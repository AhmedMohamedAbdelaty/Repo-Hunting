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
# Mapping from language names (as used in the app) to file extensions
LANGUAGE_EXTENSIONS = {
    "python": "py",
    "javascript": "js",
    "typescript": "ts",
    "java": "java",
    "csharp": "cs",
    "cpp": "cpp",
    "php": "php",
    "ruby": "rb",
    "go": "go",
    "rust": "rs",
    "swift": "swift",
    "kotlin": "kt",
}

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
    sort_by: str = "stars",
    page: int = 1,
    seed: Optional[int] = None
) -> Dict:
    """
    Fetch repositories from GitHub API with randomized pagination.

    Args:
        query: Search query string
        num_repos: Number of repositories to fetch per page
        github_token: Optional GitHub personal access token
        sort_by: Sort criteria (stars, forks, updated)
        page: Current page number (1-based)
        seed: Random seed for consistent page shuffling

    Returns:
        Dictionary with 'success', 'repos', 'error', 'total_count', 'seed'
    """
    base_url = "https://api.github.com/search/repositories"

    headers = {}
    if github_token:
        headers["Authorization"] = f"token {github_token}"

    # GitHub API limits:
    # - Max 100 items per page
    # - Only the first 1000 search results are available
    per_page = min(100, num_repos)
    max_results = 1000
    max_pages = max_results // per_page

    # Determine which actual GitHub page to fetch
    if seed is not None:
        # Create a deterministic shuffle of page numbers
        pages = list(range(1, max_pages + 1))
        rng = random.Random(seed)
        rng.shuffle(pages)

        # If requested page is out of bounds, we're done
        if page > len(pages):
            return {
                "success": True,
                "repos": [],
                "total_count": 0,
                "message": "No more results.",
                "seed": seed
            }

        github_page = pages[page - 1]
    else:
        # Default behavior (no randomization across pages)
        github_page = page

    params = {
        "q": query,
        "sort": sort_by,
        "order": "desc",
        "per_page": per_page,
        "page": github_page
    }

    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=10)

        # Check for API rate limit or unauthorized
        if response.status_code == 403:
            return {
                "success": False,
                "error": "GitHub API rate limit exceeded. Consider using a GitHub token.",
                "repos": [],
                "total_count": 0
            }
        elif response.status_code == 401:
            return {
                "success": False,
                "error": "Invalid GitHub Token. Please check your token and try again.",
                "repos": [],
                "total_count": 0
            }

        response.raise_for_status()
        data = response.json()

        repos = data.get("items", [])
        total_count = data.get("total_count", 0)

        # If we got no repos but total_count > 0, we picked a page beyond actual results.
        # Re-fetch using a page that's within the valid range.
        if not repos and total_count > 0 and seed is not None:
            import math
            actual_max_pages = min(max_pages, math.ceil(total_count / per_page))
            valid_pages = [p for p in pages if p <= actual_max_pages]
            if valid_pages:
                params["page"] = valid_pages[0]
                response = requests.get(base_url, params=params, headers=headers, timeout=10)
                response.raise_for_status()
                data = response.json()
                repos = data.get("items", [])

        if not repos:
            return {
                "success": True,
                "repos": [],
                "total_count": 0,
                "message": "No repositories found matching the criteria.",
                "seed": seed
            }

        # If we are using a seed, we don't need to shuffle the individual page results
        # as much, but a little local shuffle doesn't hurt.
        # By shuffling the PAGES, we pick a random chunk of the 1000 results.
        # To make it feel even more random, we can shuffle the results within the page.
        if seed is not None:
             # Use a derived seed for this specific page to ensure consistency
             # when re-fetching the same page (though we shouldn't need to)
             page_rng = random.Random(seed + github_page)
             page_rng.shuffle(repos)
        else:
             random.shuffle(repos)

        return {
            "success": True,
            "repos": repos,
            "total_count": total_count,
            "query": query,
            "seed": seed,
            "page": page,
            "has_more": page < max_pages and (page * per_page) < total_count
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


def fetch_code_file_count(
    owner: str,
    repo: str,
    language: str,
    github_token: Optional[str] = None,
) -> Dict:
    """
    Count source code files for a given language in a repository using GitHub Search API.

    Args:
        owner: Repository owner login
        repo: Repository name
        language: Language key (e.g. 'python', 'java')
        github_token: Optional GitHub personal access token

    Returns:
        Dict with 'success', 'count', and optional 'error'
    """
    extension = LANGUAGE_EXTENSIONS.get(language.lower())
    if not extension:
        return {"success": False, "count": None, "error": f"Unknown language: {language}"}

    headers = {"Accept": "application/vnd.github+json"}
    if github_token:
        headers["Authorization"] = f"token {github_token}"

    params = {
        "q": f"extension:{extension} repo:{owner}/{repo}",
        "per_page": 1,
    }

    try:
        response = requests.get(
            "https://api.github.com/search/code",
            params=params,
            headers=headers,
            timeout=10,
        )

        if response.status_code == 403:
            return {"success": False, "count": None, "error": "Rate limit exceeded"}
        if response.status_code == 401:
            return {
                "success": False,
                "count": None,
                "error": "GitHub token required" if not github_token else "Invalid token"
            }
        if response.status_code == 422:
            return {"success": False, "count": None, "error": "Search validation error"}

        response.raise_for_status()
        data = response.json()
        return {"success": True, "count": data.get("total_count", 0), "extension": extension}

    except requests.exceptions.RequestException as e:
        return {"success": False, "count": None, "error": str(e)}
