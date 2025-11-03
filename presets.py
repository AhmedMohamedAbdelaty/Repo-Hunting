"""
Predefined search presets for quick access
"""

PRESETS = [
    {
        "id": "trending-ai-ml",
        "name": "🤖 Trending AI/ML",
        "description": "Popular machine learning and AI projects",
        "config": {
            "language": "python",
            "topics": ["machine-learning", "artificial-intelligence", "deep-learning"],
            "min_stars": 1000,
            "since": "6months",
            "exclude_archived": True,
            "num_repos": 10
        }
    },
    {
        "id": "web-frameworks",
        "name": "🌐 Popular Web Frameworks",
        "description": "Top web development frameworks",
        "config": {
            "topics": ["framework", "web", "frontend"],
            "min_stars": 5000,
            "exclude_archived": True,
            "num_repos": 10
        }
    },
    {
        "id": "devops-tools",
        "name": "🔧 Active DevOps Tools",
        "description": "Recently updated DevOps and infrastructure tools",
        "config": {
            "topics": ["devops", "kubernetes", "docker", "infrastructure"],
            "min_stars": 500,
            "since": "3months",
            "exclude_archived": True,
            "num_repos": 15
        }
    },
    {
        "id": "data-science",
        "name": "📊 Data Science Tools",
        "description": "Python data science and analytics tools",
        "config": {
            "language": "python",
            "topics": ["data-science", "data-analysis", "analytics"],
            "min_stars": 1000,
            "exclude_archived": True,
            "num_repos": 10
        }
    },
    {
        "id": "awesome-lists",
        "name": "⭐ Awesome Lists",
        "description": "Curated lists of awesome resources",
        "config": {
            "topics": ["awesome", "awesome-list", "resources"],
            "min_stars": 1000,
            "since": "1year",
            "exclude_archived": True,
            "num_repos": 12
        }
    },
    {
        "id": "game-dev",
        "name": "🎮 Game Development",
        "description": "Game engines and development tools",
        "config": {
            "topics": ["game", "gamedev", "game-engine"],
            "min_stars": 100,
            "since": "1year",
            "exclude_archived": True,
            "num_repos": 10
        }
    },
    {
        "id": "rust-projects",
        "name": "🦀 Trending Rust",
        "description": "Popular and recent Rust projects",
        "config": {
            "language": "rust",
            "min_stars": 500,
            "since": "6months",
            "exclude_archived": True,
            "num_repos": 10
        }
    },
    {
        "id": "go-backend",
        "name": "🐹 Go Backend Tools",
        "description": "Backend and API tools written in Go",
        "config": {
            "language": "go",
            "topics": ["api", "backend", "microservices"],
            "min_stars": 500,
            "since": "6months",
            "exclude_archived": True,
            "num_repos": 10
        }
    },
    {
        "id": "security-tools",
        "name": "🔒 Security Tools",
        "description": "Cybersecurity and pentesting tools",
        "config": {
            "topics": ["security", "cybersecurity", "pentesting", "hacking"],
            "min_stars": 300,
            "since": "1year",
            "exclude_archived": True,
            "num_repos": 15
        }
    },
    {
        "id": "mobile-apps",
        "name": "📱 Mobile Development",
        "description": "Mobile app development frameworks and tools",
        "config": {
            "topics": ["mobile", "android", "ios", "react-native", "flutter"],
            "min_stars": 1000,
            "exclude_archived": True,
            "num_repos": 10
        }
    },
    {
        "id": "cli-tools",
        "name": "⌨️ CLI Tools",
        "description": "Command-line utilities and tools",
        "config": {
            "topics": ["cli", "terminal", "command-line"],
            "min_stars": 500,
            "since": "1year",
            "exclude_archived": True,
            "num_repos": 12
        }
    },
    {
        "id": "blockchain",
        "name": "⛓️ Blockchain Projects",
        "description": "Blockchain and cryptocurrency projects",
        "config": {
            "topics": ["blockchain", "cryptocurrency", "web3"],
            "min_stars": 500,
            "since": "1year",
            "exclude_archived": True,
            "num_repos": 10
        }
    }
]


def get_preset_by_id(preset_id: str):
    """Get preset configuration by ID."""
    for preset in PRESETS:
        if preset["id"] == preset_id:
            return preset
    return None


def get_all_presets():
    """Get all available presets."""
    return PRESETS
