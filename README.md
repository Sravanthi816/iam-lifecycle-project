IAM Lifecycle Automation Project

Overview

This project is a hands-on Identity and Access Management (IAM) automation learning project built using Python, Microsoft Entra ID, Microsoft Graph API, GitHub, and GitHub Actions.

The goal of this project is to simulate how enterprise IAM platforms automate Joiner, Mover, and Leaver (JML) processes using Infrastructure as Code and CI/CD practices.

Current implementation focuses on:

* Defining IAM access models using YAML
* Authenticating to Microsoft Entra ID using App Registration
* Accessing Microsoft Graph API using Python
* Managing secrets securely using environment variables
* Running automation through GitHub Actions CI/CD pipelines

Project Architecture

access-model.yaml
        ↓
Python Script
        ↓
Microsoft Entra App Registration
        ↓
Access Token
        ↓
Microsoft Graph API
        ↓
Microsoft Entra ID

Project Structure

iam-lifecycle-project/
│
├── .github/
│   └── workflows/
│       └── iam-pipeline.yml
│
├── access-model.yaml
├── employees.csv
├── test_connection.py
├── requirements.txt
├── .gitignore
└── README.md

Access Model

The access model is defined in:access-model.yaml
This file acts as the IAM policy catalog.

groups:
  - name: "SG-Engineering-Vancouver"
    description: "Security group for Engineering in Vancouver"
    type: "security-group"
    membership_rule:
      department: "Engineering"
      location: "Vancouver"

The YAML file contains:

* Group names
* Group descriptions
* Group types
* Membership rules

The purpose is to keep IAM configuration separate from Python code.

Benefits:

* Easier maintenance
* Version control support
* Infrastructure as Code
* CI/CD friendly

⸻

Microsoft Entra App Registration

An App Registration was created in Microsoft Entra ID.

Purpose:

* Provides an identity for the automation
* Allows Python to authenticate securely
* Enables access to Microsoft Graph API

The following values were generated:

* Tenant ID
* Client ID
* Client Secret

These credentials are used by Python to obtain an access token.

⸻

Environment Variables

Sensitive information is stored in:.env

TENANT_ID=<tenant-id>
CLIENT_ID=<client-id>
CLIENT_SECRET=<client-secret>
The .env file is excluded from source control through .gitignore.

Purpose:

* Prevent secrets from being committed to GitHub
* Follow security best practices

test_connection.py

Purpose:

Verify two things before building IAM automation:

1. YAML configuration can be read successfully.
2. Authentication to Microsoft Graph API works.

Step 1 - Read YAML
access-model.yaml

and prints the group definitions.

Purpose:

* Validate YAML syntax
* Verify configuration can be parsed

Step 2 - Load Environment Variables

The script loads:load_dotenv()
This reads values from the .env file and makes them available to Python.

Step 3 - Authenticate

The script creates an MSAL client:msal.ConfidentialClientApplication()

using:

* Tenant ID
* Client ID
* Client Secret

Step 4 - Request Access Token

The script requests a Microsoft Graph access token: app.acquire_token_for_client()

Purpose:

* Verify App Registration configuration
* Verify Graph permissions
* Verify secrets are correct

Successful Result

Expected output:
Groups loaded from access-model.yaml:
...
Successfully authenticated with Microsoft Graph API.

GitHub Repository

Source code is stored in GitHub.

main
 └── Production / Stable

feature/*
 └── Development Branches

 Examples:
feature/read-groups
feature/group-creation
feature/jml-workflow

Development work is performed in feature branches and merged into main using Pull Requests.

GitHub Actions CI/CD

Workflow file:.github/workflows/iam-pipeline.yml

Purpose:

Automatically validate IAM automation whenever code is pushed.

Pipeline steps:

1. Checkout repository
2. Setup Python
3. Install dependencies
4. Load GitHub Secrets
5. Run IAM validation script

Workflow result:
Git Push
    ↓
GitHub Actions
    ↓
Run test_connection.py
    ↓
Authenticate to Microsoft Graph

GitHub Secrets

The following secrets are stored in GitHub:

* TENANT_ID
* CLIENT_ID
* CLIENT_SECRET

Purpose:

* Secure secret management
* Avoid storing credentials in source code
* Support CI/CD automation

⸻

Current Project Status

Completed:

* YAML access model
* Microsoft Entra App Registration
* Python authentication
* Microsoft Graph connectivity
* GitHub repository setup
* GitHub Actions pipeline
* Secure secret management

Next Steps:

* Read existing Entra groups using Graph API
* Compare Entra state with YAML configuration
* Create missing groups
* Implement Joiner workflow
* Implement Mover workflow
* Implement Leaver workflow
* Integrate AWS role mappings
* Extend CI/CD deployment process

⸻

Learning Objectives

This project is intended to provide hands-on experience with:

* Identity and Access Management (IAM)
* Microsoft Entra ID
* Microsoft Graph API
* OAuth 2.0 Client Credentials Flow
* YAML-based configuration
* Infrastructure as Code concepts
* CI/CD pipelines
* GitHub Actions
* Joiner, Mover, Leaver lifecycle automation
* Enterprise IAM architecture