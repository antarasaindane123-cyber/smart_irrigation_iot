@echo off
echo Starting IoT Backend Server...
start python -m uvicorn backend_server:app --reload
timeout /t 3
echo Starting Smart Irrigation Web Dashboard...
python -m streamlit run app.py
pause