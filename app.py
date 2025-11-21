#!/usr/bin/env python3
"""
GitHub Repository Finder - Web Application
Flask-based web interface for searching GitHub repositories
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import csv
import json
import io
import random
from datetime import datetime

import github_search
import presets

app = Flask(__name__)

# Get GitHub token from environment
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")


@app.route('/')
def index():
    """Serve the main web interface."""
    return render_template('index.html')


@app.route('/api/presets', methods=['GET'])
def get_presets():
    """Get all predefined search presets."""
    return jsonify({
        "success": True,
        "presets": presets.get_all_presets()
    })


@app.route('/api/search', methods=['POST'])
def search_repositories():
    """
    Search for repositories based on provided criteria.

    Expected JSON body:
    {
        "language": "python",
        "topics": ["machine-learning", "ai"],
        "min_stars": 100,
        "max_stars": 5000,
        "since": "3months",
        "exclude_archived": true,
        "exclude_forks": false,
        "sort_by": "stars",
        "num_repos": 10
    }
    """
    try:
        data = request.get_json()

        # Parse topics (can be comma-separated string or list)
        topics = data.get('topics', [])
        if isinstance(topics, str):
            topics = [t.strip() for t in topics.split(',') if t.strip()]

        # Parse time period
        since = data.get('since')
        since_date = github_search.parse_time_period(since) if since else None

        # Build search query
        query = github_search.build_search_query(
            language=data.get('language'),
            topics=topics,
            min_stars=data.get('min_stars'),
            max_stars=data.get('max_stars'),
            since_date=since_date,
            exclude_archived=data.get('exclude_archived', False),
            exclude_forks=data.get('exclude_forks', False)
        )

        if not query:
            return jsonify({
                "success": False,
                "error": "At least one search criterion must be specified"
            }), 400

        # Fetch repositories
        num_repos = data.get('num_repos', 10)
        sort_by = data.get('sort_by', 'stars')
        page = data.get('page', 1)
        seed = data.get('seed')

        # Use token from request if provided, otherwise fall back to env var
        client_token = data.get('github_token')
        token_to_use = client_token if client_token else GITHUB_TOKEN

        # Generate a new seed if not provided and it's the first page
        if seed is None and page == 1:
            seed = random.randint(0, 1000000)

        result = github_search.fetch_repositories(
            query=query,
            num_repos=num_repos,
            github_token=token_to_use,
            sort_by=sort_by,
            page=page,
            seed=seed
        )

        if not result['success']:
            return jsonify(result), 500

        # Format repositories
        formatted_repos = [
            github_search.format_repository(repo)
            for repo in result['repos']
        ]

        return jsonify({
            "success": True,
            "query": query,
            "total_count": result['total_count'],
            "returned_count": len(formatted_repos),
            "repositories": formatted_repos,
            "seed": result.get('seed'),
            "page": result.get('page', 1),
            "has_more": result.get('has_more', False)
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/export/json', methods=['POST'])
def export_json():
    """Export search results as JSON file."""
    try:
        data = request.get_json()
        repositories = data.get('repositories', [])

        # Create JSON file
        json_data = json.dumps({
            "exported_at": datetime.now().isoformat(),
            "count": len(repositories),
            "repositories": repositories
        }, indent=2)

        # Create in-memory file
        buffer = io.BytesIO()
        buffer.write(json_data.encode('utf-8'))
        buffer.seek(0)

        return send_file(
            buffer,
            mimetype='application/json',
            as_attachment=True,
            download_name=f'github_repos_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        )

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/export/csv', methods=['POST'])
def export_csv():
    """Export search results as CSV file."""
    try:
        data = request.get_json()
        repositories = data.get('repositories', [])

        # Create CSV in memory
        output = io.StringIO()

        if repositories:
            # Define CSV headers
            headers = [
                'name', 'full_name', 'owner', 'stars', 'forks', 'language',
                'description', 'url', 'topics', 'created_at', 'pushed_at',
                'archived', 'open_issues', 'watchers', 'license'
            ]

            writer = csv.DictWriter(output, fieldnames=headers, extrasaction='ignore')
            writer.writeheader()

            # Write data
            for repo in repositories:
                # Convert topics list to comma-separated string
                repo_copy = repo.copy()
                repo_copy['topics'] = ', '.join(repo.get('topics', []))
                writer.writerow(repo_copy)

        # Create bytes buffer from string
        buffer = io.BytesIO()
        buffer.write(output.getvalue().encode('utf-8'))
        buffer.seek(0)

        return send_file(
            buffer,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'github_repos_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/time-periods', methods=['GET'])
def get_time_periods():
    """Get available time period options."""
    return jsonify({
        "success": True,
        "time_periods": list(github_search.TIME_PERIODS.keys())
    })


if __name__ == '__main__':
    # Run Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
