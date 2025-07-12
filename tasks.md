# Steps to Make tasks.html Pull Task Records from the Database

## 1. Add a FastAPI API Endpoint to Return Tasks as JSON

In your FastAPI tasks router (e.g., `app/routers/tasks.py`), add:

```python
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_
from app.database import get_db
from app.models.task import Task
from app.auth import get_current_admin_user  # Assuming you have auth middleware
import logging

router = APIRouter()

@router.get("/tasks/api")
async def get_tasks_api(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user),  # Require admin access
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(100, ge=1, le=1000, description="Items per page"),
    search: str = Query(None, description="Search tasks by title or description")
):
    """
    Get paginated list of tasks for the admin interface.
    Requires administrator privileges.
    """
    try:
        offset = (page - 1) * limit
        tasks_query = db.query(Task)
        if search:
            search_term = f"%{search}%"
            tasks_query = tasks_query.filter(
                or_(
                    Task.title.ilike(search_term),
                    Task.description.ilike(search_term)
                )
            )
        tasks = tasks_query.offset(offset).limit(limit).all()
        total_tasks = db.query(Task).count()
        tasks_data = []
        for task in tasks:
            tasks_data.append({
                "id": task.id,
                "title": task.title,
                "description": task.description if task.description else None,
                "status": task.status,  # e.g., 'open', 'in_progress', 'completed'
                "assigned_to": task.assigned_to,  # user id or name
                "due_date": str(task.due_date) if task.due_date else None
            })
        return {
            "tasks": tasks_data,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total_tasks,
                "total_pages": (total_tasks + limit - 1) // limit
            }
        }
    except SQLAlchemyError as e:
        logging.error(f"Database error in get_tasks_api: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logging.error(f"Unexpected error in get_tasks_api: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
```

## 2. Update tasks.html JavaScript for Error Handling and Consistency

Update the JavaScript in `tasks.html` to handle task status and errors consistently:

```javascript
// In the renderTasksTable function, update the task status logic:
let statusHtml = '';
if (task.status === 'completed') {
    statusHtml = `
        <span class="text-success font-weight-bold">
            <i class="fas fa-check-circle"></i> Completed
        </span>
    `;
} else if (task.status === 'in_progress') {
    statusHtml = `
        <span class="text-warning font-weight-bold">
            <i class="fas fa-spinner"></i> In Progress
        </span>
    `;
} else {
    statusHtml = `
        <span class="text-secondary font-weight-bold">
            <i class="fas fa-hourglass-start"></i> Open
        </span>
    `;
}
```

Also, update the `loadTasks` function to handle pagination and better error messages:

```javascript
async function loadTasks(page = 1) {
    try {
        const response = await fetch(`/tasks/api?page=${page}&limit=100`);
        if (!response.ok) {
            if (response.status === 401) {
                throw new Error('Authentication required');
            } else if (response.status === 403) {
                throw new Error('Admin access required');
            } else {
                throw new Error(`Server error: ${response.status}`);
            }
        }
        const data = await response.json();
        tasks = data.tasks || [];
        if (data.pagination) {
            console.log(`Loaded ${tasks.length} tasks (page ${data.pagination.page} of ${data.pagination.total_pages})`);
        }
        renderTasksTable();
    } catch (error) {
        console.error('Error loading tasks:', error);
        const tbody = document.getElementById('tasksTable');
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center text-danger py-4">
                    <i class="fas fa-exclamation-triangle"></i> 
                    Error loading tasks: ${error.message}
                    <br>
                    <button class="btn btn-sm btn-outline-primary mt-2" onclick="loadTasks()">
                        <i class="fas fa-refresh"></i> Retry
                    </button>
                </td>
            </tr>
        `;
    }
}
```

## 3. Confirm Task Model Fields

Make sure your `Task` model includes the required fields:

```python
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default='open')
    assigned_to = Column(Integer, nullable=True)  # user id
    due_date = Column(Date, nullable=True)
    # ... other fields ...
```

## 4. Add Authentication Dependency

Use the same authentication middleware as for users:

```python
# app/auth.py
# ...existing code...
```

## 5. Test the Implementation

1. **Start your FastAPI server:**
   ```bash
   uvicorn app.main:app --reload
   ```
2. **Test the API endpoint directly:**
   ```bash
   curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/tasks/api
   ```
3. **Visit the page:**
   - Navigate to `/tasks` in your browser
   - Verify tasks load correctly
   - Test error scenarios (invalid auth, server errors)
4. **Test pagination (if you have many tasks):**
   ```bash
   curl -H "Authorization: Bearer YOUR_TOKEN" "http://localhost:8000/tasks/api?page=2&limit=10"
   ```

## 6. Additional Enhancements (Optional)

### Add Search Functionality

Already included in the API endpoint above. You can search by task title or description.

### Add Logging

```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.get("/tasks/api")
async def get_tasks_api(...):
    logger.info(f"Admin user {current_user.email} requested tasks list")
    # ... rest of the code ...
```

---

## Summary

The updated implementation includes:

1. **Consistent task status handling** - Backend returns string `status` field
2. **Comprehensive error handling** - Both database errors and authentication errors
3. **Null value handling** - Explicit handling of null description and due date fields
4. **Authentication/Authorization** - Admin-only access to the endpoint
5. **Pagination support** - For better performance with large task lists
6. **Enhanced error messages** - User-friendly error display in the frontend
7. **Logging** - For debugging and monitoring
8. **Optional search functionality** - For better user experience

This implementation is production-ready and handles edge cases while maintaining security best practices.
