from flask import Flask, jsonify, render_template_string
import os
import platform
from datetime import datetime, timezone
app = Flask(__name__)

# Home Page

@app.get("/")
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>Flask CI/CD Application</title>

        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                min-height: 100vh;
                font-family: Arial, Helvetica, sans-serif;
                background:
                    radial-gradient(circle at top left, #1e3a8a, transparent 35%),
                    radial-gradient(circle at bottom right, #581c87, transparent 35%),
                    #020617;
                color: #ffffff;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 30px;
            }

            .container {
                width: 100%;
                max-width: 950px;
            }

            .card {
                background: rgba(15, 23, 42, 0.88);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 24px;
                padding: 50px;
                box-shadow: 0 25px 80px rgba(0, 0, 0, 0.45);
                backdrop-filter: blur(12px);
            }

            .badge {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                padding: 9px 16px;
                border-radius: 999px;
                background: rgba(34, 197, 94, 0.12);
                border: 1px solid rgba(34, 197, 94, 0.25);
                color: #4ade80;
                font-size: 14px;
                font-weight: bold;
                margin-bottom: 25px;
            }

            .dot {
                width: 9px;
                height: 9px;
                background: #22c55e;
                border-radius: 50%;
                box-shadow: 0 0 10px #22c55e;
            }

            h1 {
                font-size: 48px;
                line-height: 1.15;
                margin-bottom: 18px;
            }

            .highlight {
                background: linear-gradient(90deg, #60a5fa, #a78bfa);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            .description {
                color: #94a3b8;
                font-size: 18px;
                line-height: 1.7;
                max-width: 700px;
                margin-bottom: 40px;
            }

            .grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 18px;
            }

            .info-card {
                padding: 24px;
                background: rgba(255, 255, 255, 0.045);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px;
                transition: transform 0.2s ease;
            }

            .info-card:hover {
                transform: translateY(-4px);
            }

            .icon {
                font-size: 28px;
                margin-bottom: 15px;
            }

            .label {
                color: #64748b;
                font-size: 12px;
                font-weight: bold;
                letter-spacing: 1px;
                margin-bottom: 8px;
            }

            .value {
                color: #e2e8f0;
                font-size: 17px;
                font-weight: bold;
            }

            .pipeline {
                margin-top: 30px;
                padding: 24px;
                border-radius: 16px;
                background: rgba(255, 255, 255, 0.035);
                border: 1px solid rgba(255, 255, 255, 0.08);
            }

            .pipeline-title {
                color: #cbd5e1;
                font-size: 14px;
                font-weight: bold;
                margin-bottom: 18px;
            }

            .pipeline-flow {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 10px;
                color: #94a3b8;
                font-size: 14px;
            }

            .stage {
                padding: 10px 14px;
                background: rgba(255, 255, 255, 0.06);
                border-radius: 10px;
                text-align: center;
            }

            .arrow {
                color: #64748b;
            }

            .footer {
                text-align: center;
                margin-top: 30px;
                color: #475569;
                font-size: 13px;
            }

            @media (max-width: 750px) {
                .card {
                    padding: 30px 22px;
                }

                h1 {
                    font-size: 36px;
                }

                .grid {
                    grid-template-columns: 1fr;
                }

                .pipeline-flow {
                    flex-direction: column;
                }

                .arrow {
                    transform: rotate(90deg);
                }
            }
        </style>
    </head>

    <body>

        <div class="container">

            <div class="card">

                <div class="badge">
                    <span class="dot"></span>
                    Application Running
                </div>

                <h1>
                    Flask <span class="highlight">CI/CD</span> Demo
                </h1>

                <p class="description">
                    A Python Flask application containerized with Docker
                    and automated using GitHub Actions. This application
                    demonstrates a simple CI/CD workflow with Docker Hub.
                </p>

                <div class="grid">

                    <div class="info-card">
                        <div class="icon">🐍</div>
                        <div class="label">APPLICATION</div>
                        <div class="value">Python + Flask</div>
                    </div>

                    <div class="info-card">
                        <div class="icon">🐳</div>
                        <div class="label">CONTAINER</div>
                        <div class="value">Docker</div>
                    </div>

                    <div class="info-card">
                        <div class="icon">⚙️</div>
                        <div class="label">AUTOMATION</div>
                        <div class="value">GitHub Actions</div>
                    </div>

                </div>

                <div class="pipeline">

                    <div class="pipeline-title">
                        CI/CD PIPELINE
                    </div>

                    <div class="pipeline-flow">

                        <div class="stage">Git Push</div>

                        <div class="arrow">→</div>

                        <div class="stage">Build</div>

                        <div class="arrow">→</div>

                        <div class="stage">Test</div>

                        <div class="arrow">→</div>

                        <div class="stage">Docker Hub</div>

                        <div class="arrow">→</div>

                        <div class="stage">Deploy</div>

                    </div>

                </div>

                <div class="footer">
                    Flask Application • Docker • GitHub Actions • CI/CD
                </div>

            </div>

        </div>

    </body>
    </html>
    """)

# Health Check Endpoint

@app.get("/health")
def health():

    return jsonify({
        "status": "healthy",
        "application": "Flask CI/CD Demo",
        "framework": "Flask",
        "runtime": "Python",
        "container": "Docker",
        "ci_cd": "GitHub Actions",
        "python_version": platform.python_version(),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200

# Application Startup

if __name__ == "__main__":

    port = int(os.getenv("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )