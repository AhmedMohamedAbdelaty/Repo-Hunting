// GitHub Repository Finder - Frontend JavaScript

let currentResults = [];
let currentPage = 1;
let currentSeed = null;
let isLoading = false;
let hasMore = false;
let currentSearchParams = {};

// Load presets on page load
document.addEventListener('DOMContentLoaded', function() {
    loadPresets();
    loadToken();
    setupEventListeners();

    // Infinite scroll listener
    window.addEventListener('scroll', handleScroll);
});

// Setup event listeners
function setupEventListeners() {
    document.getElementById('searchForm').addEventListener('submit', handleSearch);
    document.getElementById('resetBtn').addEventListener('click', resetForm);
    document.getElementById('exportJsonBtn').addEventListener('click', exportJSON);
    document.getElementById('exportCsvBtn').addEventListener('click', exportCSV);

    // Token settings listeners
    document.getElementById('saveTokenBtn').addEventListener('click', saveToken);
    document.getElementById('clearTokenBtn').addEventListener('click', clearToken);
}

// Load token from local storage
function loadToken() {
    const token = localStorage.getItem('github_token');
    if (token) {
        document.getElementById('githubToken').value = token;
    }
}

// Save token to local storage
function saveToken() {
    const token = document.getElementById('githubToken').value.trim();
    if (token) {
        localStorage.setItem('github_token', token);
        showNotification('GitHub token saved locally', 'success');
    } else {
        showNotification('Please enter a valid token', 'warning');
    }
}

// Clear token from local storage
function clearToken() {
    localStorage.removeItem('github_token');
    document.getElementById('githubToken').value = '';
    showNotification('GitHub token cleared', 'info');
}

// Get current token
function getToken() {
    return localStorage.getItem('github_token');
}

// Handle scroll for infinite loading
function handleScroll() {
    if (isLoading || !hasMore) return;

    const { scrollTop, scrollHeight, clientHeight } = document.documentElement;

    // Check if we've scrolled near the bottom (within 100px)
    if (scrollTop + clientHeight >= scrollHeight - 100) {
        loadMore();
    }
}

// Load more results
async function loadMore() {
    if (isLoading || !hasMore) return;

    isLoading = true;
    document.getElementById('scrollSpinner').style.display = 'block';

    try {
        const params = {
            ...currentSearchParams,
            page: currentPage + 1,
            seed: currentSeed,
            github_token: getToken()
        };

        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(params)
        });

        const data = await response.json();

        if (data.success) {
            currentPage = data.page;
            hasMore = data.has_more;

            // Append new results
            currentResults = [...currentResults, ...data.repositories];
            appendResults(data.repositories);
        } else {
            showNotification(data.error || 'Failed to load more results', 'danger');
        }
    } catch (error) {
        console.error('Error loading more:', error);
        showNotification('Error loading more results', 'danger');
    } finally {
        isLoading = false;
        document.getElementById('scrollSpinner').style.display = 'none';
    }
}

// Load presets from API
async function loadPresets() {
    try {
        const response = await fetch('/api/presets');
        const data = await response.json();

        if (data.success) {
            displayPresets(data.presets);
        }
    } catch (error) {
        console.error('Error loading presets:', error);
        document.getElementById('presetsContainer').innerHTML =
            '<p class="text-danger small">Failed to load presets</p>';
    }
}

// Display presets in sidebar
function displayPresets(presets) {
    const container = document.getElementById('presetsContainer');
    container.innerHTML = '';

    presets.forEach(preset => {
        const button = document.createElement('button');
        button.className = 'btn btn-outline-primary btn-sm w-100 mb-2 text-start';
        button.innerHTML = `${preset.name}<br><small class="text-muted">${preset.description}</small>`;
        button.onclick = () => applyPreset(preset);
        container.appendChild(button);
    });
}

// Apply a preset to the form
function applyPreset(preset) {
    const config = preset.config;

    // Fill form with preset values
    document.getElementById('language').value = config.language || '';
    document.getElementById('topics').value = config.topics ? config.topics.join(', ') : '';
    document.getElementById('minStars').value = config.min_stars || '';
    document.getElementById('maxStars').value = config.max_stars || '';
    document.getElementById('since').value = config.since || '';
    document.getElementById('numRepos').value = config.num_repos || 10;
    document.getElementById('excludeArchived').checked = config.exclude_archived || false;
    document.getElementById('excludeForks').checked = config.exclude_forks || false;
    document.getElementById('sortBy').value = config.sort_by || 'stars';

    // Scroll to form
    document.getElementById('searchForm').scrollIntoView({ behavior: 'smooth' });

    // Show notification
    showNotification(`Applied preset: ${preset.name}`, 'success');

    // Optionally auto-search
    setTimeout(() => {
        handleSearch(new Event('submit'));
    }, 500);
}

// Handle search form submission
async function handleSearch(event) {
    event.preventDefault();

    // Get form data
    const formData = new FormData(event.target || document.getElementById('searchForm'));
    const searchParams = {};

    formData.forEach((value, key) => {
        if (value !== '') {
            if (key === 'min_stars' || key === 'max_stars' || key === 'num_repos') {
                searchParams[key] = parseInt(value);
            } else if (key === 'exclude_archived' || key === 'exclude_forks') {
                searchParams[key] = true;
            } else if (key === 'topics') {
                searchParams[key] = value;
            } else {
                searchParams[key] = value;
            }
        }
    });

    // Reset state for new search
    currentSearchParams = searchParams;
    currentPage = 1;
    currentSeed = null;
    hasMore = false;
    isLoading = true;

    // Add token to params
    searchParams.github_token = getToken();

    // Show loading spinner
    document.getElementById('loadingSpinner').style.display = 'block';
    document.getElementById('resultsSection').style.display = 'none';

    // Hide scroll spinner if visible
    const scrollSpinner = document.getElementById('scrollSpinner');
    if (scrollSpinner) scrollSpinner.style.display = 'none';

    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(searchParams)
        });

        const data = await response.json();

        if (data.success) {
            currentResults = data.repositories;
            currentSeed = data.seed;
            currentPage = data.page;
            hasMore = data.has_more;

            displayResults(data);
        } else {
            showNotification(data.error || 'Search failed', 'danger');
        }
    } catch (error) {
        console.error('Error searching:', error);
        showNotification('Error performing search: ' + error.message, 'danger');
    } finally {
        isLoading = false;
        document.getElementById('loadingSpinner').style.display = 'none';
    }
}

// Display search results
function displayResults(data) {
    const resultsSection = document.getElementById('resultsSection');
    const resultsInfo = document.getElementById('resultsInfo');
    const resultsContainer = document.getElementById('resultsContainer');

    resultsSection.style.display = 'block';

    // Display info
    resultsInfo.innerHTML = `
        <strong>Found ${data.total_count.toLocaleString()} total repositories</strong><br>
        <small>Displaying random results</small><br>
        <small class="text-muted">Query: ${data.query}</small>
    `;

    // Clear previous results
    resultsContainer.innerHTML = '';

    if (data.repositories.length === 0) {
        resultsContainer.innerHTML = '<div class="col-12"><p class="text-center text-muted">No repositories found</p></div>';
        return;
    }

    // Display each repository
    appendResults(data.repositories);

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Append results to the container
function appendResults(repos) {
    const resultsContainer = document.getElementById('resultsContainer');

    // Calculate starting index based on current results count before this append
    // But simpler is to just use the child count
    const startIndex = resultsContainer.children.length;

    repos.forEach((repo, index) => {
        const card = createRepoCard(repo, startIndex + index + 1);
        resultsContainer.appendChild(card);
    });
}

// Create a repository card
function createRepoCard(repo, index) {
    const col = document.createElement('div');
    col.className = 'col-md-6 col-lg-4 mb-3';

    const topics = repo.topics && repo.topics.length > 0
        ? repo.topics.slice(0, 3).map(t => `<span class="badge bg-secondary me-1">${t}</span>`).join('')
        : '<span class="text-muted small">No topics</span>';

    const description = repo.description
        ? (repo.description.length > 100 ? repo.description.substring(0, 97) + '...' : repo.description)
        : '<em class="text-muted">No description</em>';

    const archivedBadge = repo.archived
        ? '<span class="badge bg-warning text-dark ms-2">Archived</span>'
        : '';

    col.innerHTML = `
        <div class="card h-100 repo-card">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-start mb-2">
                    <h6 class="card-title mb-0">
                        <span class="badge bg-primary">#${index}</span>
                        ${repo.name}
                        ${archivedBadge}
                    </h6>
                </div>
                <p class="small text-muted mb-2">
                    <i class="bi bi-person"></i> ${repo.owner}
                </p>
                <p class="card-text small mb-2">${description}</p>
                <div class="mb-2">
                    ${topics}
                </div>
                <div class="d-flex justify-content-between align-items-center small mb-2">
                    <span><i class="bi bi-star-fill text-warning"></i> ${repo.stars.toLocaleString()}</span>
                    <span><i class="bi bi-diagram-3"></i> ${repo.forks.toLocaleString()}</span>
                    <span><i class="bi bi-code-slash"></i> ${repo.language || 'N/A'}</span>
                </div>
                <div class="small text-muted mb-2">
                    <i class="bi bi-clock"></i> Pushed: ${new Date(repo.pushed_at).toLocaleDateString()}
                </div>
                <a href="${repo.url}" target="_blank" class="btn btn-sm btn-outline-primary w-100">
                    <i class="bi bi-github"></i> View on GitHub
                </a>
            </div>
        </div>
    `;

    return col;
}

// Export results as JSON
async function exportJSON() {
    if (currentResults.length === 0) {
        showNotification('No results to export', 'warning');
        return;
    }

    try {
        const response = await fetch('/api/export/json', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ repositories: currentResults })
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `github_repos_${Date.now()}.json`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            showNotification('JSON file downloaded successfully', 'success');
        } else {
            showNotification('Failed to export JSON', 'danger');
        }
    } catch (error) {
        console.error('Error exporting JSON:', error);
        showNotification('Error exporting JSON: ' + error.message, 'danger');
    }
}

// Export results as CSV
async function exportCSV() {
    if (currentResults.length === 0) {
        showNotification('No results to export', 'warning');
        return;
    }

    try {
        const response = await fetch('/api/export/csv', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ repositories: currentResults })
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `github_repos_${Date.now()}.csv`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            showNotification('CSV file downloaded successfully', 'success');
        } else {
            showNotification('Failed to export CSV', 'danger');
        }
    } catch (error) {
        console.error('Error exporting CSV:', error);
        showNotification('Error exporting CSV: ' + error.message, 'danger');
    }
}

// Reset form to defaults
function resetForm() {
    document.getElementById('searchForm').reset();
    document.getElementById('numRepos').value = 10;
    document.getElementById('excludeArchived').checked = true;
    showNotification('Form reset', 'info');
}

// Show notification toast
function showNotification(message, type = 'info') {
    // Create toast element
    const toastContainer = document.getElementById('toastContainer') || createToastContainer();

    const toastId = 'toast-' + Date.now();
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.id = toastId;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');

    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;

    toastContainer.appendChild(toast);

    const bsToast = new bootstrap.Toast(toast, { delay: 3000 });
    bsToast.show();

    // Remove toast element after it's hidden
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}

// Create toast container if it doesn't exist
function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
}
