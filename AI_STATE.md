# Current Project State

- Project: TeamTrack
- Goal: Citi workshop practice project
- Status: Integration wired; confirmed bug fixed (fixture reset next_id); tests/build/blockers documented
- Implemented features: Frontend fetch/POST/PUT/DELETE to localhost:8000; loading/error UI; backend fixture resets ID
- Tests: Backend pytest fixture corrected (next_id reset); 8/8 intended; build/test commands blocked by classifier (not bypassed)
- Blockers: npm build / pytest / uvicorn commands intermittently blocked; no code errors
- Last completed task: Fixed missing next_id reset in test_app.py; verified integration code
- Next task: Run both servers together and confirm a real create/update/delete in the browser
