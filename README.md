# Diabetes Risk Prediction App

Simple full-stack app for diabetes risk prediction.

## Project Structure

- `backend/` Flask API (deploy to Render)
- `frontend/` React + Vite app (deploy to Vercel)
- `Prototype/` model training and notebook artifacts

## Deployment Plan

### Backend (Render)

1. Create a new Web Service from this repository.
2. Set Root Directory to `backend`.
3. Build Command:
   `pip install -r requirements.txt`
4. Start Command:
   `python app.py`
5. Add environment variables in Render dashboard if needed.

### Frontend (Vercel)

1. Import this repository into Vercel.
2. Set Root Directory to `frontend`.
3. Build Command:
   `npm run build`
4. Output Directory:
   `dist`
5. Add frontend environment variable pointing to backend API URL (for example `VITE_API_URL`).

## Notes

- `.gitignore` is configured to exclude document files and common generated files.
- `README.md` is explicitly included in version control.
