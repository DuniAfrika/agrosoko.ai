#!/bin/bash

# AgroGhala Server Startup Script

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}AgroGhala Server Startup${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}Error: Virtual environment not found!${NC}"
    echo "Please run: python -m venv venv"
    exit 1
fi

# Activate virtual environment
echo -e "${GREEN}Activating virtual environment...${NC}"
source venv/bin/activate

# Get host and port from environment or use defaults
HOST=${API_HOST:-0.0.0.0}
PORT=${API_PORT:-8000}

# Check if port is already in use
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${RED}Port ${PORT} is already in use!${NC}"
    echo ""
    echo "Options:"
    echo "1. Kill the existing process: kill \$(lsof -ti:$PORT)"
    echo "2. Use a different port: API_PORT=8001 ./run.sh"
    echo ""
    read -p "Try port 8001 instead? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        PORT=8001
        echo -e "${GREEN}Switching to port ${PORT}${NC}"
    else
        exit 1
    fi
fi

echo -e "${GREEN}Starting server...${NC}"
echo -e "Host: ${BLUE}${HOST}${NC}"
echo -e "Port: ${BLUE}${PORT}${NC}"
echo ""
echo -e "${GREEN}Server will be available at:${NC}"
echo -e "  ${BLUE}http://localhost:${PORT}${NC}"
echo ""
echo -e "${GREEN}Press Ctrl+C to stop${NC}"
echo ""

# Run the server with auto-reload for development
uvicorn app.main:app --host $HOST --port $PORT --reload

