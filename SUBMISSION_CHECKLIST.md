# Submission Checklist

- [ ] Push each folder to its own GitHub repo (or a monorepo), and copy the links.
- [ ] Open `frontend-html-css/index.html` and tune typography/spacing/colors to match the Figma precisely (optional polish).
- [ ] Run and test the backend:
      curl -u test:123456 http://localhost:8080/api/hello
      curl -X POST http://localhost:8080/api/login -H "Content-Type: application/json" -d '{"username":"test","password":"123456"}'
- [ ] Run the crawler to generate `blogs.csv`:
      cd crawler-mitadmissions && pip install -r requirements.txt && playwright install && python crawl_mit_blogs.py
- [ ] Run the streaming API:
      cd python-fastapi-streaming && pip install -r requirements.txt && uvicorn app:app --reload
- [ ] Prepare your resume(s) and attach to the email.
- [ ] Paste your GitHub links into `submission_email_en.txt`, then copy/paste into your email client.
- [ ] Send to recruit@d5data.ai
