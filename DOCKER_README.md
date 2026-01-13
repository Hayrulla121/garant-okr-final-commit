# Docker Deployment Guide for OKR Tracker

## Quick Start with Docker Compose

The easiest way to run the application:

```bash
docker-compose up -d
```

Access the application at `http://localhost:8501`

To stop the application:

```bash
docker-compose down
```

## Manual Docker Commands

### Build the Docker image

```bash
docker build -t okr-tracker .
```

### Run the container

```bash
docker run -d \
  --name okr-app \
  -p 8501:8501 \
  -v $(pwd)/okr_data.json:/app/okr_data.json \
  okr-tracker
```

### View logs

```bash
docker logs -f okr-app
```

### Stop and remove the container

```bash
docker stop okr-app
docker rm okr-app
```

## Configuration

The application runs on port 8501 by default. You can change this by modifying:
- `docker-compose.yml`: Change the port mapping (e.g., `"8080:8501"`)
- Or use the `-p` flag with docker run: `docker run -p 8080:8501 okr-tracker`

## Data Persistence

The `okr_data.json` file is mounted as a volume, so your data persists across container restarts.

## Troubleshooting

If you encounter issues:

1. Check if port 8501 is already in use:
   ```bash
   lsof -i :8501
   ```

2. View container logs:
   ```bash
   docker logs okr-app
   ```

3. Rebuild the image (if you made changes):
   ```bash
   docker-compose up --build
   ```
