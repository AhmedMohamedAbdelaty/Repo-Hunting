# API Documentation

## Base URL
```
http://localhost:5000
```

## Endpoints

### 1. Get Presets
Retrieve all predefined search configurations.

**Endpoint:** `GET /api/presets`

**Response:**
```json
{
  "success": true,
  "presets": [
    {
      "id": "trending-ai-ml",
      "name": "🤖 Trending AI/ML",
      "description": "Popular machine learning and AI projects",
      "config": {
        "language": "python",
        "topics": ["machine-learning", "artificial-intelligence"],
        "min_stars": 1000,
        "since": "6months",
        "exclude_archived": true,
        "num_repos": 10
      }
    }
  ]
}
```

### 2. Search Repositories
Search for GitHub repositories based on criteria.

**Endpoint:** `POST /api/search`

**Request Body:**
```json
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
```

**Response:**
```json
{
  "success": true,
  "query": "language:python topic:machine-learning topic:ai stars:100..5000 pushed:>=2025-08-03 archived:false",
  "total_count": 1234,
  "returned_count": 10,
  "repositories": [
    {
      "name": "awesome-ml",
      "full_name": "owner/awesome-ml",
      "owner": "owner",
      "stars": 12345,
      "forks": 1234,
      "language": "Python",
      "description": "An awesome ML library",
      "url": "https://github.com/owner/awesome-ml",
      "homepage": "https://example.com",
      "topics": ["machine-learning", "ai", "deep-learning"],
      "created_at": "2020-01-01T00:00:00Z",
      "updated_at": "2025-11-03T00:00:00Z",
      "pushed_at": "2025-11-03T00:00:00Z",
      "archived": false,
      "open_issues": 42,
      "watchers": 5678,
      "license": "MIT"
    }
  ]
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Error message here"
}
```

### 3. Export as JSON
Export search results as a JSON file.

**Endpoint:** `POST /api/export/json`

**Request Body:**
```json
{
  "repositories": [
    // Array of repository objects from search results
  ]
}
```

**Response:**
- **Content-Type:** `application/json`
- **File Download:** `github_repos_YYYYMMDD_HHMMSS.json`

### 4. Export as CSV
Export search results as a CSV file.

**Endpoint:** `POST /api/export/csv`

**Request Body:**
```json
{
  "repositories": [
    // Array of repository objects from search results
  ]
}
```

**Response:**
- **Content-Type:** `text/csv`
- **File Download:** `github_repos_YYYYMMDD_HHMMSS.csv`

**CSV Columns:**
- name
- full_name
- owner
- stars
- forks
- language
- description
- url
- topics (comma-separated)
- created_at
- pushed_at
- archived
- open_issues
- watchers
- license

### 5. Get Time Periods
Get available time period options.

**Endpoint:** `GET /api/time-periods`

**Response:**
```json
{
  "success": true,
  "time_periods": [
    "1week",
    "2weeks",
    "1month",
    "3months",
    "6months",
    "1year",
    "2years",
    "5years"
  ]
}
```

## Search Parameters

### language (string, optional)
Programming language to filter by.

**Examples:** `python`, `javascript`, `go`, `rust`, `java`

### topics (array or string, optional)
GitHub topics/tags to filter by. Can be array or comma-separated string.

**Array format:** `["machine-learning", "ai"]`
**String format:** `"machine-learning, ai"`

### min_stars (integer, optional)
Minimum number of stars.

**Example:** `100`

### max_stars (integer, optional)
Maximum number of stars.

**Example:** `10000`

### since (string, optional)
Time period for last push date.

**Predefined periods:**
- `1week` - Last 7 days
- `2weeks` - Last 14 days
- `1month` - Last 30 days
- `3months` - Last 90 days
- `6months` - Last 180 days
- `1year` - Last 365 days
- `2years` - Last 730 days
- `5years` - Last 1825 days

**Or exact date:** `2025-01-01` (YYYY-MM-DD format)

### exclude_archived (boolean, optional)
Exclude archived repositories.

**Default:** `false`

### exclude_forks (boolean, optional)
Exclude forked repositories.

**Default:** `false`

### sort_by (string, optional)
Sort criteria for results.

**Options:**
- `stars` (default)
- `forks`
- `updated`

### num_repos (integer, optional)
Number of repositories to return.

**Range:** 1-100
**Default:** 10

## Example Usage with cURL

### Search Request
```bash
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "topics": ["machine-learning"],
    "min_stars": 1000,
    "since": "6months",
    "exclude_archived": true,
    "num_repos": 5
  }'
```

### Get Presets
```bash
curl http://localhost:5000/api/presets
```

### Export JSON
```bash
curl -X POST http://localhost:5000/api/export/json \
  -H "Content-Type: application/json" \
  -d '{"repositories": [...]}' \
  --output results.json
```

## Example Usage with Python

```python
import requests

# Search for repositories
response = requests.post(
    'http://localhost:5000/api/search',
    json={
        'language': 'python',
        'topics': ['machine-learning', 'ai'],
        'min_stars': 1000,
        'since': '6months',
        'exclude_archived': True,
        'num_repos': 10
    }
)

data = response.json()
if data['success']:
    for repo in data['repositories']:
        print(f"{repo['name']}: {repo['stars']} stars")
```

## Example Usage with JavaScript

```javascript
// Search for repositories
fetch('http://localhost:5000/api/search', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    language: 'javascript',
    topics: ['react', 'frontend'],
    min_stars: 5000,
    since: '1year',
    exclude_archived: true,
    num_repos: 10
  })
})
.then(response => response.json())
.then(data => {
  if (data.success) {
    data.repositories.forEach(repo => {
      console.log(`${repo.name}: ${repo.stars} stars`);
    });
  }
});
```

## Error Handling

All endpoints return standard error format:

```json
{
  "success": false,
  "error": "Error description"
}
```

**Common HTTP Status Codes:**
- `200` - Success
- `400` - Bad Request (invalid parameters)
- `500` - Internal Server Error

## Rate Limiting

The application uses GitHub's Search API which has rate limits:

- **Without GitHub token:** 10 requests/minute
- **With GitHub token:** 30 requests/minute

To use a token, set the `GITHUB_TOKEN` environment variable:

```bash
docker run -p 5000:5000 -e GITHUB_TOKEN=your_token github-repos
```

## CORS

CORS is not enabled by default. To enable for cross-origin requests, modify `app.py`:

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
```

## Health Check

Check if the application is running:

```bash
curl http://localhost:5000/
```

Should return the HTML interface (status 200).

## Notes

- All timestamps are in ISO 8601 format
- Topics are always returned as arrays
- Star and fork counts are integers
- Results are randomly shuffled before returning
- Maximum 100 results per search (GitHub API limitation)
