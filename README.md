🧾 Project Title:
A digital bookkeeping web app to help small businesses track services and generate downloadable invoices.

🚀 Features:
1. Add services and customers
2. Generate and download PDF invoices
3. Filter/search for service history
4. Soft delete with confirmation prompt
5. Responsive UI

🎯 Why I Built This:
I built this app to support a real small business owner who was struggling with manual bookkeeping. Their record-keeping process was paper-based and time-consuming, making it difficult to track services or prepare accurate reports for their external accountant.

This app makes it easier for them to log, manage, and access service records — saving time and reducing errors. Over time, it can also help them lower the fees they pay to their accountant, as the system organizes and presents exactly what’s needed without extra effort.

Beyond solving a real-world problem, I used this project to challenge myself. I designed my own database models, implemented full CRUD functionality, and learned how to generate downloadable PDFs using xhtml2pdf.

The business is not tech-savvy, so I also wanted to show them how technology can simplify their operations and be something they can rely on, even with limited experience.

📦 Setup Instructions:
1. Clone the Repository
  1.1 git clone <your-repo-link>
  1.2 cd <your-project-folder>

2. Install Dependencies
  2.1 pip install Django
  2.2 pip install djangorestframework
  2.3 pip install xhtml2pdf

 3.Run Migrations
  3.1 python manage.py makemigrations
  3.2 python manage.py migrate

4. Start Development Server
   4.1 python manage.py runserver
✅ Done! You're ready to use the app.







