#!/bin/bash
# Script to test Docker build locally before deploying to Railway

echo "🐳 Building Docker image..."
docker build -t goalbuddy21:test .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
    echo ""
    echo "To run the container locally:"
    echo "docker run --env-file .env -v $(pwd)/credentials:/app/credentials goalbuddy21:test"
else
    echo "❌ Docker build failed!"
    exit 1
fi

