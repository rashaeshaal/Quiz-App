# Quiz App API Documentation

## **Introduction**
The Quiz App API provides endpoints for **Admin** and **User** roles to manage and participate in quizzes. Admins can create, edit, and delete quizzes and questions, while users can register, attempt quizzes, and view their scores.

---
## **Authentication**
All endpoints (except registration and login) require authentication via **JWT tokens**.

### **Register Admin**
**URL:** `POST /quiz/register/`

**Request:**
```json
{
    "email": "admin@example.com",
    "name": "Admin User",
    "password": "admin123",
    "is_admin": true
}
```

**Response:**
```json
{
    "email": "admin@example.com",
    "name": "Admin User",
    "is_admin": true,
    "is_superuser": true
}
```

### **Login Admin**
**URL:** `POST /quiz/login/`

**Request:**
```json
{
    "email": "admin@example.com",
    "password": "admin123"
}
```

**Response:**
```json
{
    "refresh": "<refresh_token>",
    "access": "<access_token>",
    "user": {
        "email": "user@example.com",
        "name": "User Name",
        "is_admin": false
    }
}
```

---
## **Admin APIs**

### **Create Category**
**URL:** `POST /quiz/categories/`

**Request:**
```json
{
    "name": "General Knowledge"
}
```

**Response:**
```json
{
    "id": 1,
    "name": "General Knowledge"
}
```

### **Edit Category**
**URL:** `PUT /quiz/categories/{id}/`

**Request:**
```json
{
    "name": "Updated Category Name"
}
```

**Response:**
```json
{
    "id": 1,
    "name": "Updated Category Name"
}
```

### **Create Quiz**
**URL:** `POST /quiz/quizzes/`

**Request:**
```json
{
    "title": "GK Quiz",
    "category": 1,
    "is_active": true
}
```

**Response:**
```json
{
    "id": 1,
    "title": "GK Quiz",
    "category": 1,
    "is_active": true
}
```

### **Edit Quiz**
**URL:** `PUT /quiz/quizzes/{id}/`

**Request:**
```json
{
    "title": "Updated Quiz Title",
    "is_active": false
}
```

**Response:**
```json
{
    "id": 1,
    "title": "Updated Quiz Title",
    "category": 1,
    "is_active": false
}
```

### **Create Question**
**URL:** `POST /quiz/questions/`

**Request:**
```json
{
    "quiz": 1,
    "text": "What is 10+3?",
    "option_1": "2",
    "option_2": "13",
    "option_3": "9",
    "option_4": "5",
    "correct_answer": "13"
}
```

**Response:**
```json
{
    "id": 1,
    "quiz": 1,
    "text": "What is 10+3?",
    "option_1": "2",
    "option_2": "13",
    "option_3": "9",
    "option_4": "5",
    "correct_answer": "13"
}
```

### **Edit Question**
**URL:** `PUT /quiz/questions/{id}/`

**Request:**
```json
{
    "text": "Updated Question Text",
    "option_1": "1",
    "option_2": "5",
    "option_3": "10",
    "option_4": "15",
    "correct_answer": "15"
}
```

**Response:**
```json
{
    "id": 1,
    "quiz": 1,
    "text": "Updated Question Text",
    "option_1": "1",
    "option_2": "5",
    "option_3": "10",
    "option_4": "15",
    "correct_answer": "15"
}
```

### **View User Submissions**
**URL:** `GET /quiz/submissions/`
**Headers:** `Authorization: Bearer <access_token>`

**Response:**
```json
[
    {
        "id": 1,
        "user": 5,
        "quiz_id": 1,
        "quiz_title": "GK Quiz",
        "score": 1,
        "submitted_at": "2025-04-05T09:16:56.614Z",
        "answers": [
            {
                "question_id": 1,
                "selected_option": "4",
                "correct_answer": "10"
            }
        ]
    }
]


---
## **User APIs**
### **Register User**
**URL:** POST /users/register/

**Request:**
json
{
    "email": "test@example.com",
    "name": "Test User",
    "password": "user123"
}


**Response:**
json
{
    "email": "test@example.com",
    "name": "Test User",
    "is_admin": false
}

### **Login User**
**URL:** `POST /users/handlelogin/`

**Request:**
```json
{
    "email": "test@example.com",
    "password": "user123"
}
```

**Response:**
```json
{
    "refresh": "<refresh_token>",
    "access": "<access_token>",
    "user": {
        "email": "user@example.com",
        "name": "User Name",
        "is_admin": false
    }
}
```



### **View Active Quizzes**
**URL:** `GET /users/quizzes/active/`

**Response:**
```json
[
    {
        "id": 1,
        "title": "GK Quiz",
        "category": 1,
        "is_active": true
    }
]
```

### **Submit Quiz**
**URL:** `POST /users/submissions/`

**Request:**
```json
{
    "quiz_id": 1,
    "answers": [
        {
            "question_id": 1,
            "selected_option": "4"
        }
    ]
}
```

**Response:**
```json
{
    "id": 1,
    "user": {
        "email": "test@example.com",
        "name": "Test User"
    },
    "quiz_id": 1,
    "quiz_title": "GK Quiz",
    "score": 0,
    "submitted_at": "2025-04-05T14:36:29.556Z",
    "answers": []
}
```

### **View Submission History**
**URL:** `GET /users/past-submissions/`

**Response:**
```json
{
    "user": {
        "email": "test@example.com",
        "name": "Test User"
    },
    "submissions": [
        {
            "id": 23,
            "quiz_id": 1,
            "quiz_title": "GK Quiz",
            "score": 0,
            "submitted_at": "2025-04-05T15:42:55.127Z",
            "answers": [
                {
                    "question_id": 1,
                    "selected_option": "13",
                    "correct_answer": "9"
                }
            ]
        }
    ]
}
```
---
## **Conclusion**
This documentation provides detailed API specifications for the **Quiz App**.

