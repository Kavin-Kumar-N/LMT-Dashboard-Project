📊 LMT-Dashboard-Project

A modular, scalable, and interactive Streamlit dashboard application for uploading, managing, filtering, and visualizing CSV and Excel datasets.
The project follows a clean, parameterized, function-based architecture, making it easy to maintain, extend, and reuse in real-world analytics scenarios.

🚀 Features

📁 Upload CSV and Excel files

💾 Persist uploaded files locally for reuse

📂 Select and manage saved datasets

🗑️ Safe file deletion with confirmation

📅 Automatic date-based filtering

🔢 Numeric range filtering

🏷️ Categorical filtering

📊 Interactive visualizations:

Line Chart

Bar Chart

Area Chart

Scatter Plot

Pie Chart

🧭 Tab-based chart navigation

📄 Expandable raw and filtered data views

🧠 Clean separation of UI, logic, and configuration

🏗️ Project Structure
LMT-Dashboard-Project/
│
├── app.py                  # Main Streamlit application
├── uploaded_files/          # Local storage for uploaded datasets
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation

⚙️ Installation
1️⃣ Clone the repository
git clone https://github.com/<your-username>/LMT-Dashboard-Project.git
cd LMT-Dashboard-Project

2️⃣ Create and activate a virtual environment (recommended)
python -m venv venv


Windows

venv\Scripts\activate


macOS / Linux

source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

▶️ Running the Application
streamlit run app.py


The dashboard will open automatically in your browser.

🧩 Technologies Used

Python

Streamlit – Web application framework

Pandas – Data processing and filtering

Altair – Interactive scatter plots

Plotly – Pie charts and interactive visuals

🧠 Design Philosophy

Parameterized Functions
All core functionalities are implemented using parameterized functions to avoid hidden dependencies and improve reusability.

Modular Architecture
Each responsibility (uploading, filtering, visualization, file management) is encapsulated in its own function.

Scalability
The codebase is structured to support future enhancements such as authentication, multi-page navigation, caching, and database integration.

📌 Use Cases

Data analysis dashboards

Internal reporting tools

Learning and teaching Streamlit

Rapid analytics prototyping

Portfolio projects for data analysts

🔒 Data Handling

Uploaded files are stored locally in the uploaded_files/ directory.

No external data is transmitted.

Files can be safely removed using a confirmation-based delete mechanism.
