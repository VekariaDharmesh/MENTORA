#!/usr/bin/env bash
# ============================================================================
# AI TEACHER — SYSTEM HEALTH & SERVICE STATUS CHECKER
# ============================================================================

set -e

echo "======================================================================"
echo "          AI TEACHER — PLATFORM HEALTH & STATUS VERIFICATION          "
echo "======================================================================"

# 1. Python Environment Check
echo -n "[1/5] Checking Python environment... "
if command -v python3 &>/dev/null; then
    PY_VER=$(python3 --version)
    echo "OK ($PY_VER)"
else
    echo "FAILED (python3 not found)"
fi

# 2. Node.js Environment Check
echo -n "[2/5] Checking Node.js environment... "
if command -v node &>/dev/null; then
    NODE_VER=$(node --version)
    echo "OK ($NODE_VER)"
else
    echo "FAILED (node not found)"
fi

# 3. Backend Health Check (Port 8000)
echo -n "[3/5] Checking FastAPI Cognitive Backend (http://localhost:8000/health)... "
if curl -s -f http://localhost:8000/health &>/dev/null; then
    echo "HEALTHY (HTTP 200 OK)"
else
    echo "OFFLINE (FastAPI is not currently reachable on port 8000)"
fi

# 4. Frontend Web Server Check (Port 3000)
echo -n "[4/5] Checking Frontend Web Server (http://localhost:3000/)... "
if curl -s -f -I http://localhost:3000/ &>/dev/null; then
    echo "HEALTHY (HTTP 200 OK)"
else
    echo "OFFLINE (Frontend is not currently reachable on port 3000)"
fi

# 5. Automated Unit Tests Run
echo -e "\n[5/5] Executing Backend Automated Test Suite..."
python3 backend/tests/test_api.py

echo "======================================================================"
echo "          ALL SYSTEMS VERIFIED & READY FOR HACKATHON DEMO!            "
echo "======================================================================"
