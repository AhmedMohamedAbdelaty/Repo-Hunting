# GitHub Repository Finder - User Guide

## 🌟 Welcome!

This is your interactive web application to discover amazing GitHub repositories!

## 🚀 Getting Started

### Step 1: Launch the Application

```bash
docker build -t github-repos .
docker run -p 5000:5000 github-repos
```

Then open your browser to: **http://localhost:5000**

### Step 2: Choose Your Search Method

You have two options:

#### Option A: Quick Presets (Recommended for Beginners)
- Look at the **left sidebar** with "Quick Presets"
- Click any preset button to instantly search
- Examples:
  - 🤖 **Trending AI/ML** - Latest machine learning projects
  - 🌐 **Popular Web Frameworks** - Top web frameworks
  - 📊 **Data Science Tools** - Python data science tools
  - 🎮 **Game Development** - Game engines and tools

#### Option B: Custom Search (Advanced)
- Fill out the **Custom Search** form with your criteria
- Available filters:
  - **Programming Language**: Choose from 12+ languages
  - **Topics/Tags**: Enter comma-separated topics (e.g., `machine-learning, deep-learning`)
  - **Star Range**: Min and Max stars
  - **Time Period**: When repos were last updated
  - **Sort By**: Stars, Forks, or Recently Updated
  - **Exclusions**: Exclude archived or forked repos

## 📋 Search Examples

### Example 1: Find Popular Python ML Projects
1. Select **Language**: Python
2. Enter **Topics**: `machine-learning, artificial-intelligence`
3. Set **Min Stars**: 1000
4. Set **Since**: Last 6 months
5. Check **Exclude Archived**
6. Click **Search Repositories**

### Example 2: Find Recent JavaScript Web Frameworks
1. Select **Language**: JavaScript
2. Enter **Topics**: `framework, web`
3. Set **Min Stars**: 5000
4. Set **Since**: Last Year
5. Click **Search Repositories**

### Example 3: Find Active DevOps Tools
1. Enter **Topics**: `devops, kubernetes, docker`
2. Set **Min Stars**: 500
3. Set **Since**: Last 3 Months
4. Check **Exclude Archived**
5. Click **Search Repositories**

## 📊 Understanding Results

Each repository card shows:
- **Repository Name** (with # badge)
- **Owner** (GitHub username/organization)
- **Description** (truncated if long)
- **Topics/Tags** (up to 3 shown)
- **Stars** ⭐ - GitHub stars count
- **Forks** 🔀 - Number of forks
- **Language** 💻 - Primary programming language
- **Last Push Date** 🕒 - When last updated
- **Archived Status** ⚠️ - If repo is archived

## 💾 Exporting Results

After getting search results, you can export them:

1. **Export as JSON**
   - Click **Export JSON** button
   - Downloads a structured JSON file
   - Includes all repository details
   - Good for further processing

2. **Export as CSV**
   - Click **Export CSV** button
   - Downloads a spreadsheet-compatible file
   - Easy to open in Excel, Google Sheets
   - Good for data analysis

## 🎯 Tips & Tricks

### 1. Use Topics for Better Results
Topics are more specific than language:
- Instead of just "Python", try `python, machine-learning, tensorflow`
- For web dev: `javascript, react, frontend, web`
- For DevOps: `devops, kubernetes, docker, ci-cd`

### 2. Adjust Star Ranges
- **100-1000 stars**: Emerging projects, active development
- **1000-10000 stars**: Well-established, mature projects
- **10000+ stars**: Industry standards, widely adopted

### 3. Time Periods Matter
- **Last Week/Month**: Very active, cutting-edge projects
- **Last 6 Months**: Recently maintained, good for adoption
- **Last Year**: Stable, mature projects
- **Any Time**: Include older but still relevant projects

### 4. Exclude Options
- **Exclude Archived**: Skip dead/unmaintained projects (recommended)
- **Exclude Forks**: Skip copies, get only original projects

### 5. Number of Results
- Start with **10** results for quick overview
- Use **20-50** for comprehensive search
- Max **100** for extensive research

## 🔑 Using GitHub Token (Optional)

For more searches per minute:

1. Create a GitHub Personal Access Token:
   - Go to GitHub Settings → Developer settings
   - Generate new token (classic)
   - No special permissions needed for public repos

2. Run Docker with token:
   ```bash
   docker run -p 5000:5000 -e GITHUB_TOKEN=your_token_here github-repos
   ```

**Rate Limits:**
- Without token: 10 searches per minute
- With token: 30 searches per minute

## 🎨 Interface Tips

### Keyboard Shortcuts
- **Tab**: Navigate through form fields
- **Enter**: Submit search form
- **Ctrl+F**: Browser search in results

### Mobile Friendly
- Responsive design works on tablets and phones
- Swipe to scroll through results
- Tap preset buttons for quick searches

### Browser Compatibility
- Works best on: Chrome, Firefox, Edge, Safari
- Requires JavaScript enabled
- Modern browser recommended (2020+)

## 🐛 Troubleshooting

### "No repositories found"
- Try broader search criteria
- Remove some filters
- Increase max stars or remove star limits
- Try different time period

### "API Rate Limit Exceeded"
- Wait a few minutes before searching again
- Use a GitHub token (see above)
- Reduce number of searches

### Results loading slowly
- GitHub API may be slow
- Try fewer results (e.g., 5-10)
- Check your internet connection

### Page not loading
- Ensure Docker container is running
- Check if port 5000 is available
- Try: `docker ps` to see running containers
- Restart container if needed

## 📚 Common Use Cases

### For Developers
- Find libraries for your project
- Discover trending technologies
- Research competitors
- Find code examples

### For Students
- Find learning resources
- Discover project ideas
- Study popular codebases
- Follow best practices

### For Researchers
- Track technology trends
- Analyze open source ecosystem
- Export data for analysis
- Monitor tool adoption

### For Teams
- Evaluate tool options
- Find inspiration
- Discover integrations
- Research tech stack choices

## 🎓 Best Practices

1. **Start Broad, Then Narrow**
   - Begin with presets or minimal filters
   - Refine based on results
   - Add more specific topics

2. **Combine Filters Wisely**
   - Language + Topics = Best results
   - Star range + Time period = Quality control
   - Exclude archived = Active projects only

3. **Export and Organize**
   - Export results for later review
   - Build your own curated lists
   - Share findings with team

4. **Explore Regularly**
   - New projects appear daily
   - Trends change quickly
   - Regular searches find gems

## 💡 Pro Tips

- **Morning Routine**: Check "Last Week" for new projects
- **Research Mode**: Export CSV, analyze in spreadsheet
- **Discovery Mode**: Use presets, explore random results
- **Deep Dive**: Open interesting repos in new tabs
- **Stay Updated**: Bookmark favorites, watch releases

## 🆘 Need Help?

- Check the README.md for technical details
- Review API endpoints documentation
- Check Docker logs: `docker logs <container_id>`
- Restart application if issues persist

---

**Happy Repository Hunting! 🎯**

Find amazing projects, learn new technologies, and contribute to open source!
