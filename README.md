# Smart Task Analyzer

The **Smart Task Analyzer** is a mini-application that intelligently scores and prioritizes tasks based on urgency, importance, effort, and dependency impact.  
This project is built as part of the Software Development Intern Technical Assessment and follows all instructions provided in the assignment document.

Backend is built with **Django**, and the frontend uses **HTML, CSS, and JavaScript**.

---

## 📁 Project Structure

smart-task-analyzer/
├── backend/
│ ├── manage.py
│ ├── task_analyzer/
│ │ ├── settings.py
│ │ ├── urls.py
│ │ └── wsgi.py
│ └── tasks/
│ ├── views.py
│ ├── scoring.py
│ ├── urls.py
│ ├── tests.py
│ └── serializers.py
├── frontend/
│ ├── index.html
│ ├── styles.css
│ └── script.js
├── requirements.txt
└── README.md

yaml
Copy code

---

## 🚀 Setup Instructions

### 1. Clone the repository
git clone <your-repo-url>
cd smart-task-analyzer

shell
Copy code

### 2. Create & activate a virtual environment

**Windows**
python -m venv venv
venv\Scripts\activate

markdown
Copy code

**Mac/Linux**
python3 -m venv venv
source venv/bin/activate

shell
Copy code

### 3. Install dependencies
pip install -r requirements.txt

shell
Copy code

### 4. Run backend
cd backend
python manage.py migrate
python manage.py runserver

sql
Copy code

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/tasks/analyze/` | Returns scored & sorted tasks |
| POST | `/api/tasks/suggest/` | Returns top 3 suggestions with explanations |

### 5. Run frontend
Open:
frontend/index.html

markdown
Copy code
in your browser.

---

# 🧠 Algorithm Explanation (350–450 words)

The Smart Task Analyzer uses a weighted scoring algorithm that calculates a priority score (0–100) for each task. The score is based on four factors: **Urgency**, **Importance**, **Effort**, and **Dependency Impact**. Each factor is normalized and contributes to the final score based on predefined weights.

### **1. Urgency**
Urgency is calculated from the due date:
- Overdue tasks receive maximum urgency with extra weight added for each day overdue.
- Tasks due today have very high urgency.
- Tasks with future due dates gradually decrease in urgency the farther the due date is.

This ensures that urgent, time-sensitive tasks always appear at the top.

### **2. Importance**
Importance is a user-given value (1–10). It is scaled to a 0–100 range.  
This reflects the long-term impact or strategic value of a task.

### **3. Effort**
Effort uses estimated hours:
- ≤1 hour → high score (quick win)  
- 1–3 hours → moderate  
- 3–8 hours → lower  
- >8 hours → minimal  

Lower-effort tasks rise in priority as “quick wins” to improve productivity.

### **4. Dependency Impact**
If many tasks depend on a given task, it is considered a **critical path** item.  
Each dependent task increases the dependency score.  
This reduces workflow bottlenecks.

### **5. Weight Distribution**
Weights used:
- **35% Urgency**
- **35% Importance**
- **15% Effort**
- **15% Dependency Impact**

These weights create a “smart balance” between immediate deadlines and impactful work.

### **6. Edge-Case Handling**
The algorithm gracefully handles:
- Missing due dates → low urgency  
- Invalid effort values → default effort score  
- No importance value → mid-range importance  
- Missing dependencies → empty list  

The algorithm never breaks due to incomplete input.

### **7. Cycle Detection**
The system detects circular dependencies using DFS.  
If a cycle exists, the response sets:
