#!/bin/bash

###############################################################################
# AgroGhala Health Check Script
# Run this script to verify your deployment is working correctly
###############################################################################

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
APP_DIR="/var/www/agrosoko.ai"
API_URL="http://localhost:8000"
DOMAIN="your-domain.com"  # Change this

echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   AgroGhala Health Check${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}\n"

# Function to check status
check_status() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ PASS${NC}"
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}"
        return 1
    fi
}

TOTAL_CHECKS=0
PASSED_CHECKS=0

# Check 1: Systemd Service
echo -n "1. Systemd Service Status: "
TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
sudo systemctl is-active --quiet agrosoko
check_status && PASSED_CHECKS=$((PASSED_CHECKS + 1))

# Check 2: Process Running
echo -n "2. Application Process: "
TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
pgrep -f "uvicorn app.main:app" > /dev/null
check_status && PASSED_CHECKS=$((PASSED_CHECKS + 1))

# Check 3: Port Listening
echo -n "3. Port 8000 Listening: "
TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
sudo netstat -tlnp | grep ":8000" > /dev/null 2>&1 || sudo ss -tlnp | grep ":8000" > /dev/null 2>&1
check_status && PASSED_CHECKS=$((PASSED_CHECKS + 1))

# Check 4: API Root Endpoint
echo -n "4. API Root Endpoint: "
TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
response=$(curl -s -o /dev/null -w "%{http_code}" $API_URL)
if [ "$response" = "200" ]; then
    echo -e "${GREEN}✓ PASS${NC} (HTTP $response)"
    PASSED_CHECKS=$((PASSED_CHECKS + 1))
else
    echo -e "${RED}✗ FAIL${NC} (HTTP $response)"
fi

# Check 5: API Counties Endpoint
echo -n "5. Counties Endpoint: "
TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
response=$(curl -s -o /dev/null -w "%{http_code}" $API_URL/api/counties)
if [ "$response" = "200" ]; then
    echo -e "${GREEN}✓ PASS${NC} (HTTP $response)"
    PASSED_CHECKS=$((PASSED_CHECKS + 1))
else
    echo -e "${RED}✗ FAIL${NC} (HTTP $response)"
fi

# Check 6: API Weather Endpoint
echo -n "6. Weather Endpoint: "
TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
response=$(curl -s -o /dev/null -w "%{http_code}" $API_URL/api/weather/Nairobi)
if [ "$response" = "200" ]; then
    echo -e "${GREEN}✓ PASS${NC} (HTTP $response)"
    PASSED_CHECKS=$((PASSED_CHECKS + 1))
else
    echo -e "${RED}✗ FAIL${NC} (HTTP $response)"
fi

# Check 7: API Prices Endpoint
echo -n "7. Prices Endpoint: "
TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
response=$(curl -s -o /dev/null -w "%{http_code}" $API_URL/api/prices)
if [ "$response" = "200" ]; then
    echo -e "${GREEN}✓ PASS${NC} (HTTP $response)"
    PASSED_CHECKS=$((PASSED_CHECKS + 1))
else
    echo -e "${RED}✗ FAIL${NC} (HTTP $response)"
fi

# Check 8: Nginx Running
echo -n "8. Nginx Service: "
TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
sudo systemctl is-active --quiet nginx
check_status && PASSED_CHECKS=$((PASSED_CHECKS + 1))

# Check 9: Nginx Configuration
echo -n "9. Nginx Configuration: "
TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
sudo nginx -t > /dev/null 2>&1
check_status && PASSED_CHECKS=$((PASSED_CHECKS + 1))

# Check 10: Application Directory
echo -n "10. Application Directory: "
TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
[ -d "$APP_DIR" ]
check_status && PASSED_CHECKS=$((PASSED_CHECKS + 1))

# Check 11: Virtual Environment
echo -n "11. Virtual Environment: "
TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
[ -f "$APP_DIR/venv/bin/python" ]
check_status && PASSED_CHECKS=$((PASSED_CHECKS + 1))

# Check 12: Environment File
echo -n "12. Environment File: "
TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
[ -f "$APP_DIR/.env" ]
check_status && PASSED_CHECKS=$((PASSED_CHECKS + 1))

# Check 13: Log Directory
echo -n "13. Log Directory: "
TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
[ -d "/var/log/agrosoko" ]
check_status && PASSED_CHECKS=$((PASSED_CHECKS + 1))

# Check 14: Data Directory
echo -n "14. Data Directory: "
TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
[ -d "$APP_DIR/data" ]
check_status && PASSED_CHECKS=$((PASSED_CHECKS + 1))

# Check 15: Firewall Status
echo -n "15. Firewall (UFW): "
TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
sudo ufw status | grep -q "Status: active"
check_status && PASSED_CHECKS=$((PASSED_CHECKS + 1))

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"

# Calculate percentage
PERCENTAGE=$((PASSED_CHECKS * 100 / TOTAL_CHECKS))

if [ $PASSED_CHECKS -eq $TOTAL_CHECKS ]; then
    echo -e "${GREEN}✓ ALL CHECKS PASSED${NC} ($PASSED_CHECKS/$TOTAL_CHECKS)"
    echo -e "${GREEN}Your deployment is healthy! 🚀${NC}"
    EXIT_CODE=0
elif [ $PERCENTAGE -ge 80 ]; then
    echo -e "${YELLOW}⚠ MOSTLY HEALTHY${NC} ($PASSED_CHECKS/$TOTAL_CHECKS passed - $PERCENTAGE%)"
    echo -e "${YELLOW}Some non-critical issues detected${NC}"
    EXIT_CODE=0
else
    echo -e "${RED}✗ ISSUES DETECTED${NC} ($PASSED_CHECKS/$TOTAL_CHECKS passed - $PERCENTAGE%)"
    echo -e "${RED}Please review failed checks${NC}"
    EXIT_CODE=1
fi

echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""

# Additional Information
echo -e "${YELLOW}Additional Information:${NC}"
echo ""

# Service Status
echo -e "${BLUE}Service Status:${NC}"
sudo systemctl status agrosoko --no-pager -l | head -5

echo ""
echo -e "${BLUE}Recent Logs (last 5 lines):${NC}"
sudo journalctl -u agrosoko -n 5 --no-pager

echo ""
echo -e "${BLUE}Disk Usage:${NC}"
df -h $APP_DIR | tail -1

echo ""
echo -e "${BLUE}Memory Usage:${NC}"
free -h | grep Mem

echo ""
echo -e "${BLUE}Process Info:${NC}"
ps aux | grep uvicorn | grep -v grep | head -2

echo ""
echo -e "${YELLOW}Quick Commands:${NC}"
echo "  View logs:    sudo journalctl -u agrosoko -f"
echo "  Restart:      sudo systemctl restart agrosoko"
echo "  Check nginx:  sudo nginx -t"
echo "  API docs:     curl $API_URL/docs"

exit $EXIT_CODE

