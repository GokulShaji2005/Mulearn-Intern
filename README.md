# Job Portal Backend API

A robust Django REST Framework-based backend system for managing job postings with role-based access control (RBAC). The system supports three user roles: Admin, Company, and Public users, each with specific permissions and capabilities.

## 🚀 Features

### User Management
- **Custom User Model** with email-based authentication
- **Role-Based Access Control** (Admin, Company)
- **JWT Authentication** using SimpleJWT
- User registration, login, logout, and profile management
- Token refresh mechanism

### Job Management
- **Company Features:**
  - Create job postings (pending approval by default)
  - View their own job listings
  - Update and delete their job postings
  - Multi-skill assignment for jobs

- **Admin Features:**
  - View all job listings with filtering
  - Approve or reject job postings
  - Filter jobs by status and company
  - Full oversight of the platform

- **Public Features:**
  - Browse approved job listings
  - Filter by job type, location, and skills
  - No authentication required for viewing

### API Documentation
- **Swagger UI** (`/api/docs/`)
- **ReDoc** (`/api/redoc/`)
- Auto-generated OpenAPI schema

## 🛠️ Technology Stack

### Core Framework
- **Django 4.2.7** - High-level Python web framework
- **Django REST Framework** - Powerful toolkit for building Web APIs
- **Python 3.x** - Programming language

### Authentication & Security
- **djangorestframework-simplejwt** - JSON Web Token authentication
- **django-decouple** - Configuration management

### Database
- **SQLite** - Default database (development)
- Easily switchable to PostgreSQL, MySQL, etc.

### API Documentation
- **drf-spectacular** - OpenAPI 3.0 schema generation
- Swagger UI and ReDoc integration

### Additional Packages
- **django-filter** - Advanced query filtering
- Built-in pagination support

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd "Backend Intern"
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install django djangorestframework djangorestframework-simplejwt
pip install drf-spectacular django-filter python-decouple
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory (optional):
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

### 5. Run Migrations
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Admin)
```bash
python manage.py createsuperuser
# Enter email, password (role will be set to 'admin' automatically)
```

### 7. Run Development Server
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## 📚 API Endpoints

### Authentication Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/register/` | Register new company user | No |
| POST | `/api/login/` | Login and get JWT tokens | No |
| POST | `/api/logout/` | Logout (blacklist token) | Yes |
| POST | `/api/token/refresh/` | Refresh access token | Yes |
| GET | `/api/profile/` | Get user profile | Yes |
| PUT/PATCH | `/api/profile/` | Update user profile | Yes |

### Company Endpoints
| Method | Endpoint | Description | Auth Required | Role |
|--------|----------|-------------|---------------|------|
| GET | `/api/company/jobs/` | List company's own jobs | Yes | Company |
| POST | `/api/company/jobs/create/` | Create new job posting | Yes | Company |
| GET | `/api/company/jobs/<id>/` | Get specific job details | Yes | Company (Owner) |
| PUT/PATCH | `/api/company/jobs/<id>/` | Update job posting | Yes | Company (Owner) |
| DELETE | `/api/company/jobs/<id>/` | Delete job posting | Yes | Company (Owner) |
| PUT/PATCH | `/api/job/<id>/update/` | Alternative update endpoint | Yes | Company (Owner) |
| DELETE | `/api/job/<id>/delete/` | Alternative delete endpoint | Yes | Company (Owner) |

### Admin Endpoints
| Method | Endpoint | Description | Auth Required | Role |
|--------|----------|-------------|---------------|------|
| GET | `/api/admin/jobs/` | List all jobs with filters | Yes | Admin |
| PATCH | `/api/admin/jobs/<id>/verify/` | Approve/reject job posting | Yes | Admin |

**Admin Job Filters:**
- `?status=pending` - Filter by status (pending/approved/rejected)
- `?company=email@example.com` - Filter by company email

**Admin Verify Payload:**
```json
{
  "action": "approve"  // or "reject"
}
```

### Public Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/jobs/` | List all approved jobs | No |

**Public Job Filters:**
- `?job_type=full_time` - Filter by job type (full_time/part_time/internship)
- `?location=bangalore` - Filter by location (case-insensitive)
- `?skill=python` - Filter by skill name (case-insensitive)

### Documentation Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/schema/` | OpenAPI schema (JSON) |
| GET | `/api/docs/` | Swagger UI |
| GET | `/api/redoc/` | ReDoc UI |

## 🔐 Authentication

### JWT Token Flow
1. **Register/Login:** Get `access` and `refresh` tokens
2. **Authenticate:** Include token in header: `Authorization: Bearer <access_token>`
3. **Refresh:** Use refresh token to get new access token when expired
4. **Logout:** Blacklist refresh token

### Example Request
```bash
# Login
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "company@example.com",
    "password": "password123"
  }'

# Use token in subsequent requests
curl -X GET http://127.0.0.1:8000/api/company/jobs/ \
  -H "Authorization: Bearer <your_access_token>"
```

## 📊 Database Models

### User Model (`accounts.User`)
```python
- email (EmailField, unique, primary)
- full_name (CharField)
- role (CharField: 'admin' | 'company')
- is_active (BooleanField)
- is_staff (BooleanField)
- date_joined (DateTimeField)
- password (hashed)
```

### Job Model (`jobs.Job`)
```python
- title (CharField)
- company (ForeignKey → User)
- job_type (CharField: 'full_time' | 'part_time' | 'internship')
- location (CharField)
- skills (ManyToManyField → Skill)
- status (CharField: 'pending' | 'approved' | 'rejected')
- created_at (DateTimeField)
```

### Skill Model (`jobs.Skill`)
```python
- name (CharField, unique)
```

## 🔒 Permission Classes

### Built-in Permissions
- `IsAuthenticated` - User must be logged in
- `AllowAny` - No authentication required

### Custom Permissions (`jobs.permission`)
- **`IsAdminUserRole`** - User must be authenticated, have role='admin', and is_staff=True
- **`IsCompany`** - User must be authenticated and have role='company'
- **`IsOwnerCompany`** - User must be the company that created the job (object-level permission)

## 📝 Request/Response Examples

### Register Company User
```json
POST /api/register/
{
  "email": "company@example.com",
  "full_name": "Tech Solutions Inc",
  "password": "securepassword123",
  "role": "company"
}

Response (201):
{
  "email": "company@example.com",
  "full_name": "Tech Solutions Inc",
  "role": "company"
}
```

### Create Job Posting
```json
POST /api/company/jobs/create/
Authorization: Bearer <token>

{
  "title": "Senior Python Developer",
  "job_type": "full_time",
  "location": "Bangalore, India",
  "skills": ["Python", "Django", "REST API", "PostgreSQL"]
}

Response (201):
{
  "id": 1,
  "title": "Senior Python Developer",
  "job_type": "full_time",
  "location": "Bangalore, India",
  "skills": ["Python", "Django", "REST API", "PostgreSQL"],
  "status": "pending",
  "created_at": "2026-01-15T10:30:00Z"
}
```

### Admin Approve Job
```json
PATCH /api/admin/jobs/1/verify/
Authorization: Bearer <admin_token>

{
  "action": "approve"
}

Response (200):
{
  "message": "Job approved successfully",
  "status": "approved"
}
```

### Public Job Listing
```json
GET /api/jobs/?job_type=full_time&location=bangalore

Response (200):
{
  "count": 15,
  "next": "http://127.0.0.1:8000/api/jobs/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Senior Python Developer",
      "company_name": "Tech Solutions Inc",
      "job_type": "full_time",
      "location": "Bangalore, India",
      "skills": ["Python", "Django", "REST API"],
      "created_at": "2026-01-15T10:30:00Z"
    }
  ]
}
```

## 🏗️ Project Structure

```
Backend Intern/
│
├── backend/
│   ├── manage.py                    # Django management script
│   ├── db.sqlite3                   # Database file
│   │
│   ├── core/                        # Project configuration
│   │   ├── __init__.py
│   │   ├── settings.py              # Django settings
│   │   ├── urls.py                  # Root URL configuration
│   │   ├── asgi.py                  # ASGI config
│   │   └── wsgi.py                  # WSGI config
│   │
│   ├── accounts/                    # User authentication app
│   │   ├── models.py                # User model
│   │   ├── serializers.py           # User serializers
│   │   ├── views.py                 # Auth views
│   │   ├── urls.py                  # Auth routes
│   │   ├── admin.py                 # Admin configuration
│   │   └── migrations/
│   │
│   └── jobs/                        # Job management app
│       ├── models.py                # Job & Skill models
│       ├── serializers.py           # Job serializers
│       ├── views.py                 # Job views
│       ├── urls.py                  # Job routes
│       ├── permission.py            # Custom permissions
│       ├── admin.py                 # Admin configuration
│       └── migrations/
│
└── README.md                        # This file
```

## 🎯 Key Design Decisions

### 1. Role-Based Access Control
- **Separation of Concerns:** Admin and Company roles have distinct responsibilities
- **Object-Level Permissions:** Companies can only modify their own jobs
- **Security First:** Default status is 'pending' to prevent spam

### 2. Email-Based Authentication
- More professional for B2B platform
- Unique identifier across the system
- JWT tokens for stateless authentication

### 3. Skill System
- ManyToMany relationship allows flexible skill tagging
- Auto-creation of skills prevents duplicates
- Enables powerful filtering for job seekers

### 4. API Design
- RESTful principles
- Consistent naming conventions
- Proper HTTP status codes
- Pagination for large datasets

## 🧪 Testing the API

### Using Swagger UI (Recommended)
1. Navigate to `http://127.0.0.1:8000/api/docs/`
2. Register a company user
3. Login to get JWT token
4. Click "Authorize" and enter: `Bearer <your_token>`
5. Test all endpoints interactively

### Using cURL
```bash
# Register
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@company.com","full_name":"Test Company","password":"pass123","role":"company"}'

# Login
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@company.com","password":"pass123"}'

# Create Job (use token from login)
curl -X POST http://127.0.0.1:8000/api/company/jobs/create/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Developer","job_type":"full_time","location":"Remote","skills":["Python"]}'
```

## 🐛 Troubleshooting

### Common Issues

**1. Import Error: '.permissions' could not be resolved**
- Ensure `permission.py` exists in `jobs/` directory
- Check imports in `views.py` match filename (`.permission` not `.permissions`)

**2. Token Authentication Failed**
- Verify token format: `Authorization: Bearer <token>`
- Check if token is expired (use refresh endpoint)
- Ensure user account is active

**3. Permission Denied**
- Verify user role matches endpoint requirements
- Check if user owns the resource (for update/delete)
- Confirm user is authenticated

**4. Database Errors**
- Run migrations: `python manage.py migrate`
- Delete `db.sqlite3` and re-run migrations if needed

## 🔄 Future Enhancements

- [ ] Job application system for candidates
- [ ] Email notifications for job status changes
- [ ] Advanced search with Elasticsearch
- [ ] File upload for company logos and resumes
- [ ] PostgreSQL integration for production
- [ ] Docker containerization
- [ ] CI/CD pipeline setup
- [ ] Comprehensive test suite
- [ ] Rate limiting and throttling
- [ ] Caching with Redis

## 📄 License

This project is part of a Backend Internship assignment.

## 👥 User Roles Summary

| Role | Can Register | Create Jobs | View Own Jobs | Modify Own Jobs | View All Jobs | Approve Jobs |
|------|-------------|-------------|---------------|-----------------|---------------|--------------|
| **Admin** | Via createsuperuser | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Company** | ✅ (API) | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Public** | ❌ | ❌ | ❌ | ❌ | ✅ (Approved only) | ❌ |

## 📞 Support

For issues or questions, please refer to the API documentation at `/api/docs/` or check the Django admin panel at `/admin/`.

---

**Built with ❤️ using Django REST Framework**
