# GitHub Repository Finder 🔍

An interactive web application to discover random GitHub repositories with advanced filtering capabilities. Search by language, topics, star counts, time periods, and more!

## ✨ Features

- � **Beautiful Web Interface**: Modern, responsive design with Bootstrap
- �🎲 **Random Selection**: Get truly random repositories from search results
- 🏷️ **Topics/Tags Filter**: Filter by GitHub topics like `machine-learning`, `web`, `api`
- 🗣️ **Language Filter**: Filter by programming language
- ⭐ **Star Range**: Set minimum and maximum star counts
- 📅 **Time Periods**: Easy-to-use predefined time periods (1week, 3months, 1year, etc.)
- 🚫 **Exclusions**: Exclude archived or forked repositories
- � **Export Results**: Download results as JSON or CSV
- 🎯 **Quick Presets**: 12+ predefined searches for common use cases
- �🔑 **Token Support**: Optional GitHub token for higher rate limits

## � Quick Start with Docker

### 1. Build the Docker Image

```bash
docker build -t github-repos .
```

### 2. Run the Web Application

```bash
docker run -p 5000:5000 github-repos
```

### 3. Open in Browser

Navigate to: **http://localhost:5000**

### 4. (Optional) Run with GitHub Token

For higher API rate limits, pass a GitHub token:

```bash
docker run -p 5000:5000 -e GITHUB_TOKEN=your_token_here github-repos
```

## 🎯 Predefined Search Presets

The application includes 12 curated search presets:

1. **🤖 Trending AI/ML** - Popular machine learning and AI projects
2. **🌐 Popular Web Frameworks** - Top web development frameworks
3. **🔧 Active DevOps Tools** - Recently updated DevOps and infrastructure tools
4. **📊 Data Science Tools** - Python data science and analytics tools
5. **⭐ Awesome Lists** - Curated lists of awesome resources
6. **🎮 Game Development** - Game engines and development tools
7. **🦀 Trending Rust** - Popular and recent Rust projects
8. **🐹 Go Backend Tools** - Backend and API tools written in Go
9. **🔒 Security Tools** - Cybersecurity and pentesting tools
10. **📱 Mobile Development** - Mobile app development frameworks and tools
11. **⌨️ CLI Tools** - Command-line utilities and tools
12. **⛓️ Blockchain Projects** - Blockchain and cryptocurrency projects

## 🎨 Web Interface Features

### Custom Search
- **Programming Language**: Choose from 12+ popular languages
- **Topics/Tags**: Enter comma-separated topics (e.g., `machine-learning, deep-learning, ai`)
- **Star Range**: Filter by minimum and maximum stars
- **Time Period**: Select from predefined periods or any time
- **Sort Options**: Sort by stars, forks, or recently updated
- **Exclusions**: Toggle to exclude archived or forked repos
- **Results Count**: Choose how many repositories to fetch (1-100)

### Search Results
- **Repository Cards**: Beautiful card layout with key information
- **Details Shown**:
  - Repository name and owner
  - Star count, forks, and language
  - Topics/tags
  - Description
  - Last push date
  - Archived status
- **Direct Links**: Click to view on GitHub
- **Export Options**: Download all results as JSON or CSV

## 📊 Export Formats

### JSON Export
```json
{
  "exported_at": "2025-11-03T12:00:00",
  "count": 10,
  "repositories": [
    {
      "name": "repo-name",
      "owner": "owner-name",
      "stars": 12345,
      "forks": 1234,
      "language": "Python",
      "description": "A brief description...",
      "topics": ["machine-learning", "ai"],
      "url": "https://github.com/owner/repo",
      ...
    }
  ]
}
```

### CSV Export
Includes all fields: name, full_name, owner, stars, forks, language, description, url, topics, created_at, pushed_at, archived, open_issues, watchers, license

## 🔧 API Endpoints

The Flask application exposes several API endpoints:

- `GET /` - Main web interface
- `GET /api/presets` - Get all predefined search presets
- `POST /api/search` - Perform a repository search
- `POST /api/export/json` - Export results as JSON
- `POST /api/export/csv` - Export results as CSV
- `GET /api/time-periods` - Get available time period options

## 🐳 Docker Configuration

The Docker container:
- Exposes port **5000** for the web interface
- Runs Flask in production mode
- Supports environment variables:
  - `GITHUB_TOKEN` - Optional GitHub personal access token
  - `PORT` - Custom port (default: 5000)

### Custom Port Example

```bash
docker run -p 8080:8080 -e PORT=8080 github-repos
```

## 📁 Project Structure

```
.
├── app.py                 # Flask web application
├── github_search.py       # Core search functionality
├── github_repos.py        # Original CLI tool (still available)
├── presets.py            # Predefined search configurations
├── templates/
│   └── index.html        # Web interface template
├── static/
│   ├── css/
│   │   └── style.css     # Custom styles
│   └── js/
│       └── app.js        # Frontend JavaScript
├── Dockerfile            # Docker configuration
└── README.md            # This file
```

## 🔑 GitHub API Rate Limits

- **Without token**: 10 requests per minute
- **With token**: 30 requests per minute (authenticated)

To create a GitHub token:
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token (no special permissions needed for public repo search)
3. Pass it via `GITHUB_TOKEN` environment variable

## 🎯 Usage Examples

### Example 1: Find Trending Python ML Projects
1. Click the "🤖 Trending AI/ML" preset
2. Results show popular Python ML projects from the last 6 months

### Example 2: Custom Search for Go APIs
1. Select **Language**: Go
2. Enter **Topics**: `api, backend, microservices`
3. Set **Min Stars**: 500
4. Set **Since**: Last 6 months
5. Check **Exclude Archived**
6. Click **Search Repositories**

### Example 3: Export Data Science Repos
1. Click "📊 Data Science Tools" preset
2. Wait for results to load
3. Click **Export CSV** to download all results

## 🛠️ CLI Tool (Still Available)

The original command-line interface is still available in `github_repos.py`:

```bash
docker run github-repos python github_repos.py --language python --min-stars 100 --num-repos 5
```

## 🤝 Contributing

Feel free to fork, modify, and use this project as you wish!

## 📝 License

MIT License

---

**Made with ❤️ for the open source community**
