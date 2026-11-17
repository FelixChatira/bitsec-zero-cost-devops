# BitSec – Local Web Application & DevOps Deployment

![Project Status](https://img.shields.io/badge/Project-Active-brightgreen)
![Platform](https://img.shields.io/badge/Platform-Ubuntu%20WSL2-orange)
![Backend](https://img.shields.io/badge/Backend-Python%20%7C%20Flask-blue)
![Database](https://img.shields.io/badge/Database-PostgreSQL-336791)
![Web Server](https://img.shields.io/badge/Web%20Server-Nginx-green)
![Deployment](https://img.shields.io/badge/Deployment-Cloudflare-orange)

**BitSec** is a locally hosted web application deployment project designed to demonstrate practical DevOps engineering using open-source technologies.

The project demonstrates how to build, configure, deploy, expose, and manage a web application using a local Linux environment without depending on paid cloud infrastructure.

The application runs on Ubuntu through Windows Subsystem for Linux (WSL2), uses PostgreSQL for database management, Nginx for web serving, Gunicorn for the Python backend, and Cloudflare Tunnel for public internet access.

---

## 1. Project Overview

The primary objective of BitSec is to demonstrate a practical, low-cost DevOps deployment architecture.

Instead of deploying application infrastructure to platforms such as AWS, Azure, or Google Cloud, this project uses locally managed infrastructure and publicly accessible networking through Cloudflare.

### Key objectives

- Develop and host a web application locally.
- Configure a Python Flask backend.
- Integrate PostgreSQL for persistent data storage.
- Configure Nginx as the web server.
- Deploy the backend using Gunicorn.
- Automate application services using systemd.
- Publish the application using Cloudflare Tunnel.
- Maintain application source code using Git and GitHub.
- Establish an automated startup workflow using Windows Task Scheduler and WSL.

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| Ubuntu WSL2 | Local Linux environment |
| Python | Backend programming |
| Flask | REST API framework |
| Gunicorn | Python application server |
| PostgreSQL | Relational database |
| Nginx | Web server and reverse proxy |
| Cloudflare Tunnel | Public application access |
| systemd | Service management and automation |
| Git | Version control |
| GitHub | Source code hosting |
| Windows Task Scheduler | Automatic WSL startup |

## 3. System Architecture

The BitSec deployment follows this architecture:

```text
              INTERNET
                  |
                  |
          CLOUDFLARE NETWORK
                  |
                  |
          CLOUDFLARE TUNNEL
                  |
                  |
           LOCAL UBUNTU WSL2
                  |
                  |
                NGINX
             Port 80
                  |
          +-------+-------+
          |               |
          |               |
       FRONTEND        API ROUTING
          |               |
     HTML/CSS/JS       GUNICORN
                          |
                       FLASK API
                       Port 5000
                          |
                          |
                      POSTGRESQL
                       DATABASE
```

### Architecture explanation

**Frontend**

The frontend consists of HTML, CSS, and JavaScript files served by Nginx.

**Backend**

The Python Flask application provides the backend API functionality.

Gunicorn manages the Flask application processes and listens locally on port 5000.

**Database**

PostgreSQL provides persistent relational database storage.

**Web server**

Nginx serves the frontend and handles incoming HTTP requests. It also provides the reverse-proxy layer for API requests where configured.

**Public access**

Cloudflare Tunnel securely connects the locally hosted web server to the Cloudflare network without requiring direct inbound port forwarding on the home router.

## 4. Repository Structure

The repository is organised as follows:

```text
bitsec-zero-cost-devops/
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── .env.example
│
├── index.html
├── styles.css
├── app.js
├── .gitignore
└── README.md
```

### File descriptions

| File | Description |
|---|---|
| `index.html` | Main frontend page |
| `styles.css` | Frontend styling |
| `app.js` | Frontend JavaScript |
| `backend/app.py` | Flask backend application |
| `backend/requirements.txt` | Python dependencies |
| `backend/.env.example` | Environment configuration template |
| `.gitignore` | Excludes unnecessary and sensitive files |
| `README.md` | Project documentation |

## 5. Infrastructure Requirements

The following software and infrastructure are required:

- Windows computer.
- Windows Subsystem for Linux 2 (WSL2).
- Ubuntu Linux distribution.
- Python 3.
- PostgreSQL.
- Nginx.
- Git.
- Gunicorn.
- Cloudflared.

A Cloudflare account is required to establish the Quick Tunnel.

A purchased domain name is not required for Quick Tunnel deployment.

## 6. Installation and Setup

### Step 1: Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/bitsec-zero-cost-devops.git
```

Navigate into the project directory:

```bash
cd bitsec-zero-cost-devops
```

### Step 2: Prepare the Python environment

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r backend/requirements.txt
```

### Step 3: Configure environment variables

Use the supplied example configuration:

```bash
cp backend/.env.example backend/.env
```

Configure the required environment variables using your own database credentials and application settings.

Never commit real credentials, passwords, API keys, or private configuration files to GitHub.

**Note:** The production deployment uses a separate environment configuration at `/etc/bitsec/bitsec.env`.

### Step 4: Configure PostgreSQL

Install PostgreSQL if it is not already installed:

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

Enable PostgreSQL:

```bash
sudo systemctl enable postgresql
sudo systemctl start postgresql
```

Configure the database, database user, and connection settings according to the application's environment configuration.

### Step 5: Configure Nginx

Install Nginx:

```bash
sudo apt install nginx
```

Enable automatic startup:

```bash
sudo systemctl enable nginx
sudo systemctl start nginx
```

Configure the Nginx virtual host to serve the frontend and route API requests to the backend where required.

Validate the configuration:

```bash
sudo nginx -t
```

### Step 6: Configure Gunicorn

Gunicorn is used to serve the Flask backend application.

The production application is configured to run using:

```bash
/opt/bitsec-api/venv/bin/gunicorn \
--workers 2 \
--bind 127.0.0.1:5000 \
app:app
```

The backend runs under a dedicated Linux service account named `bitsec`.

### Step 7: Configure Cloudflare Tunnel

Install Cloudflared and authenticate or configure the Quick Tunnel as required.

Start a Quick Tunnel manually with:

```bash
cloudflared tunnel --url http://127.0.0.1:80
```

Cloudflare generates a temporary public URL ending in:

```text
.trycloudflare.com
```

The URL may change when the tunnel is restarted.

## 7. Automatic Service Management

One of the main objectives of this project is to eliminate the need to manually launch each application component.

The production deployment uses systemd services.

### Configured services

| Service | systemd unit |
|---|---|
| PostgreSQL | `postgresql.service` |
| Nginx | `nginx.service` |
| BitSec API | `bitsec-api.service` |
| Cloudflare Tunnel | `cloudflared-quick.service` |

### Enable automatic startup

```bash
sudo systemctl enable postgresql
sudo systemctl enable nginx
sudo systemctl enable bitsec-api
sudo systemctl enable cloudflared-quick
```

### Check service status

```bash
systemctl status postgresql
systemctl status nginx
systemctl status bitsec-api
systemctl status cloudflared-quick
```

### Restart the application services

```bash
sudo systemctl restart bitsec-api
sudo systemctl restart nginx
sudo systemctl restart cloudflared-quick
```

### View application logs

```bash
sudo journalctl -u bitsec-api -f
```

Cloudflare logs:

```bash
sudo journalctl -u cloudflared-quick -f
```

## 8. Windows and WSL Automatic Startup

The deployment uses Windows Task Scheduler to launch the Ubuntu WSL environment automatically when Windows starts or the configured user logs in.

Once WSL starts, systemd manages the application services.

The startup sequence is:

1. Windows starts.
2. Windows Task Scheduler launches Ubuntu WSL.
3. systemd starts the enabled services.
4. PostgreSQL becomes available.
5. Nginx starts serving the frontend.
6. Gunicorn starts the Flask API.
7. Cloudflare Tunnel establishes the public connection.

This approach provides a largely automated local hosting environment.

## 9. Testing and Verification

The following commands can be used to verify the deployment.

### Check application services

```bash
systemctl is-active postgresql nginx bitsec-api cloudflared-quick
```

### Check automatic startup

```bash
systemctl is-enabled postgresql nginx bitsec-api cloudflared-quick
```

### Test Nginx

```bash
curl -I http://127.0.0.1
```

### Test Flask API

```bash
curl -i http://127.0.0.1:5000/health
```

### Test API through Nginx

```bash
curl -i http://127.0.0.1/api/health
```

### Check PostgreSQL

```bash
pg_lsclusters
```

### Test public application access

```bash
curl -I https://YOUR-QUICK-TUNNEL-URL.trycloudflare.com
```

Replace the example hostname with the current Cloudflare-generated URL.

## 10. Project Deployment Results

The deployment work has established the following functionality:

- Local Ubuntu WSL2 hosting environment.
- PostgreSQL installation and database connectivity.
- Database tables and record creation.
- Application storage directory.
- Flask backend API.
- Gunicorn application serving.
- Nginx frontend hosting.
- Cloudflare Quick Tunnel public access.
- systemd service management.
- Automatic service startup configuration.
- Windows Task Scheduler integration.
- GitHub source code management.

The application and its configured services have been tested in the local deployment environment.

## 11. Security Considerations

Security improvements remain an important part of the project's ongoing development.

Recommended practices include:

- Keep credentials outside the Git repository.
- Use strong database passwords.
- Avoid exposing PostgreSQL directly to the public internet.
- Run application processes under dedicated service accounts.
- Keep Ubuntu packages and Python dependencies updated.
- Review Nginx and Flask security configurations.
- Restrict access to sensitive application endpoints.
- Use Cloudflare Access or other authentication controls where appropriate.
- Maintain regular database backups.

**Cloudflare Quick Tunnel notice:** Quick Tunnels are intended for development and testing. They do not provide a permanent hostname or guaranteed production availability. A public tunnel should not be treated as an authentication or access-control mechanism.

## 12. Future Improvements

Potential future development areas include:

- Application security hardening.
- Centralised logging and monitoring.
- Automated database backups.
- Automated testing with CI/CD.
- GitHub Actions integration.
- Application health monitoring.
- Improved API authentication and authorisation.
- Persistent Cloudflare Named Tunnel deployment.
- Containerisation using Docker.
- Automated deployment pipelines.

## 13. Learning Outcomes

This project demonstrates practical experience with:

- Linux server administration.
- Python backend development.
- REST API deployment.
- PostgreSQL database administration.
- Nginx configuration.
- Gunicorn process management.
- systemd service automation.
- WSL2 infrastructure management.
- Cloudflare networking and tunnelling.
- Git and GitHub workflows.
- Local infrastructure deployment and troubleshooting.

## 14. Author and Repository

**Project:** BitSec – Local Web Application & DevOps Deployment

**GitHub Repository:** `bitsec-zero-cost-devops`

**Repository URL:**

`https://github.com/YOUR_USERNAME/bitsec-zero-cost-devops`

**Deployment Environment:** Ubuntu WSL2 on Windows

---

*BitSec demonstrates that a practical web application infrastructure can be developed, deployed, managed, and published using locally hosted open-source technologies without requiring a paid cloud hosting platform.*
