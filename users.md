# Steps to Make users.html Pull User Accounts from the Database

## 1. Add a FastAPI API Endpoint to Return Users as JSON

In your FastAPI settings router (e.g., `app/routers/settings.py`), add:

```python
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User

router = APIRouter()

@router.get("/settings/users/api")
async def get_users_api(db: Session = Depends(get_db)):
    users = db.query(User).all()
    users_data = []
    for user in users:
        users_data.append({
            "id": user.id,
            "name": user.name,
            "type": user.type,
            "email": user.email,
            "company": user.company
        })
    return {"users": users_data}
```

- This endpoint returns a JSON object with a `users` list containing user details.
- Adjust field names as needed to match your User model.

## 2. Ensure users.html JavaScript Fetches from the API

Your `users.html` already contains:
```javascript
fetch('/settings/users/api')
```
- This will call the above endpoint and populate the table with user data.

## 3. Confirm User Model Fields

Make sure your `User` model includes the fields you want to display:
- `id`, `name`, `type`, `email`, `company`

## 4. Test the Page

- Start your FastAPI server.
- Visit `/settings/users` in your browser.
- The users table should populate with accounts from the database.

## 5. (Optional) Add Authentication/Authorization

- If you want to restrict access to the API, add authentication dependencies to the route.

---

**Summary:**
- Add a GET API endpoint that returns users as JSON in `app/routers/settings.py`.
- Ensure your frontend fetches from this endpoint and renders the data.
- Test to confirm users are displayed.
