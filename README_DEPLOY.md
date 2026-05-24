# Free deployment option: Hugging Face Spaces

This backend is too memory-heavy for 512 MB free web services because the model file is large and the ML dependencies load a lot of native code.

Recommended free backend host:

- Hugging Face Spaces
- Space SDK: Docker
- Free hardware: CPU Basic
- App port: 7860

## Deploy steps

1. Create a new Space on Hugging Face.
2. Choose `Docker` as the Space SDK.
3. Push this repository to the Space repo.
4. If Git rejects the model file, install Git LFS and track:

   ```bash
   git lfs track "backend/model/*.joblib"
   git add .gitattributes backend/model/*.joblib
   git commit -m "Track model artifacts with Git LFS"
   ```

5. Set these environment variables in the Space settings:

   ```text
   SECRET_KEY=<any long random string>
   SESSION_COOKIE_SECURE=True
   CORS_ORIGINS=<your frontend URL>
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=<your password>
   ```

6. After it builds, test:

   ```text
   https://<username>-<space-name>.hf.space/api/health
   ```

For the frontend, deploy it separately on Vercel or Netlify free tier and point its API URL to the Hugging Face backend URL.
