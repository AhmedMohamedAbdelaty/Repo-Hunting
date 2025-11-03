FROM python:3.9-slim

WORKDIR /app

# Copy all application files
COPY github_search.py .
COPY presets.py .
COPY app.py .
COPY github_repos.py .
COPY templates/ templates/
COPY static/ static/

# Install dependencies
RUN pip install --no-cache-dir flask requests

# Expose port 5000 for the web interface
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Run the Flask app
CMD ["python", "app.py"]
