# Cloud Notes (AWS Project)

A simple web app to write notes and attach documents. Built with Python (Flask) to demonstrate how AWS compute (EC2), cloud storage (S3), and databases work together.

---

## How It Works

- **Frontend:** Simple HTML/CSS page to create, view, and delete notes without refreshing the page.
- **Backend:** Python + Flask handling the routes and API requests.
- **Database:** Uses a local SQLite file (`notes.db`) by default so it works immediately without setup. Can also connect to MySQL or AWS RDS just by updating `.env`.
- **File Uploads:** Uploaded documents go directly to an **Amazon S3** bucket. If AWS credentials aren't configured yet, it automatically saves them locally in the `uploads/` folder.
- **Hosting:** Runs on an **AWS EC2** Ubuntu server.

---

## Project Structure

```text
aws-cloud-notes-project/
├── app/
│   ├── __init__.py       # Sets up the Flask app
│   ├── routes.py         # App routes (home, add note, delete note)
│   ├── database.py       # Handles saving notes (SQLite / MySQL)
│   ├── s3_service.py     # Uploads files to S3 (or local folder)
│   └── templates/
│       └── index.html    # The user interface
│
├── scripts/
│   ├── setup_aws.py      # Quick script to create the S3 bucket
│   └── deploy_ec2.sh     # Setup script to run the app on EC2
│
├── uploads/              # Local folder for files (if not using S3)
├── run.py                # Starts the app
├── requirements.txt      # Python packages needed
├── .env.example          # Sample environment settings
└── README.md
```

---

## How to Run Locally

### 1. Set up virtual environment
```powershell
# On Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# On Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Install requirements
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
python run.py
```
Open **[http://localhost:5000](http://localhost:5000)** in your browser.

> You don't need AWS credentials to test locally. The app will work right away using local SQLite and the local `uploads/` folder.

---

## Connecting AWS Services (Optional)

If you want to use real AWS S3 or MySQL:

1. Copy `.env.example` to `.env`:
   ```powershell
   copy .env.example .env
   ```
2. Fill in your details:
   - **For S3:** Add `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `S3_BUCKET`.
   - **For MySQL / RDS:** Fill in `DB_HOST`, `DB_USER`, and `DB_PASSWORD`.
3. Restart `python run.py`.

---

## Deploying to AWS EC2

1. Launch an **Ubuntu 24.04** `t2.micro` instance on EC2.
2. In the Security Group, open:
   - Port 22 (SSH)
   - Port 5000 (Custom TCP, anywhere `0.0.0.0/0`)
3. Connect to your instance via SSH:
   ```bash
   ssh -i your-key.pem ubuntu@<EC2-PUBLIC-IP>
   ```
4. Clone this repo and run the deployment script:
   ```bash
   git clone <YOUR_GIT_REPO_URL> aws-cloud-notes-project
   cd aws-cloud-notes-project
   chmod +x scripts/deploy_ec2.sh
   ./scripts/deploy_ec2.sh
   ```
5. Open `http://<EC2-PUBLIC-IP>:5000` in your browser.
