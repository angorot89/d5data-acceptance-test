# D5 Data – Acceptance Test Sample Answers

This repository contains **sample** implementations for the four tasks (frontend, backend, crawler, Python streaming API). You can push each folder to your own GitHub as separate repos or a monorepo.

## 1) Frontend – Implement Figma
- Folder: `frontend-html-css`
- Tech: pure HTML/CSS (Inter font), responsive layout scaffold
- To run: open `index.html` in a browser
- What to customize:
  - **Typography**: sizes/weights from the Figma
  - **Spacing**: match padding and grid gaps
  - **Colors**: set CSS variables in `:root`
  - **Assets**: replace the `.media-placeholder` with real images or SVGs from Figma

> If you prefer React/Tailwind, you can copy this structure into a Vite project and convert sections into components.

## 2) Backend – Spring Boot 3.2.0 + Spring Security
- Folder: `backend-springboot-3.2.0`
- Endpoints:
  - `POST /api/login` (public): accepts JSON body `{ "username": "test", "password": "123456" }` and returns a demo success JSON.
  - `GET /api/hello` (protected): requires HTTP Basic auth. Use `test` / `123456`.
- How to run:
  ```bash
  cd backend-springboot-3.2.0
  ./mvnw spring-boot:run   # or: mvn spring-boot:run
  ```
- Notes: Uses in-memory user with BCrypt-hashed password, Basic auth for simplicity as required.

## 3) Crawler – Playwright + DrissionPage
- Folder: `crawler-mitadmissions`
- Output: `blogs.csv` with headers: `Title | Author | Comment Count | Time | Article Content | Images In Article`
- How to run:
  ```bash
  cd crawler-mitadmissions
  pip install -r requirements.txt
  playwright install
  python crawl_mit_blogs.py
  ```
  This uses both Playwright and DrissionPage to fetch articles, then merges results and writes a CSV.

## 4) Python – Streaming API with FastAPI
- Folder: `python-fastapi-streaming`
- Endpoints:
  - `GET /stream` returns a streaming text/plain response
  - `GET /sse` returns Server-Sent Events (SSE) with JSON-like payloads
- How to run:
  ```bash
  cd python-fastapi-streaming
  pip install -r requirements.txt
  uvicorn app:app --reload
  ```

---

## Submission
- Push each folder to GitHub and include links in your email.
- Include your resume as attachments and add the following fields:
  - **Name**: YOUR NAME
  - **Role Preference**: Frontend / Backend / Crawler / Python (you can list multiple)
  - **School**: YOUR SCHOOL
  - **Degree**: YOUR DEGREE
  - **Earliest Start Date**: YYYY-MM-DD


---

## Candidate Info (Ready for Submission)

- **Name**: Amine Amraoui
- **Intended Position(s)**: Frontend / Backend / Crawler / Python
- **School**: Zhejiang University of Science and Technology
- **Degree**: Bachelor’s degree
- **Earliest Start Date**: This month

