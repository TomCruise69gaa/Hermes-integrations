# FRIDAY — PROJECT HANDOFF
Last updated: November 15, 2026

## 1. PROJECT IDENTITY

Project: FRIDAY
AI Platform: Hermes Agent v0.23.1
Purpose: Private, local-first home AI operating system.

IMPORTANT:
The active project is FRIDAY, not Jarvis.
Historical test artifacts may still contain the Jarvis name.
Do not rename or delete those artifacts without approval.

FRIDAY's long-term objectives:
- Personal and household organization
- Home operations and automation
- Research and project management
- Software development assistance
- Specialized AI agents
- Controlled external integrations
- Multi-step task execution with minimal supervision
- Future family-support capabilities

## 2. USER DEVELOPMENT RULES

- Keep explanations concise and use plain language.
- Give one PowerShell command at a time.
- Prefer complete replacement files over patches.
- Avoid unnecessary architecture discussions.
- Do not restart or rebuild completed project components.
- Do not repeat completed diagnostics.
- Do not perform additional Docker security audits unless requested.
- Distinguish verified results from planned capabilities.

Development workflow:
1. Plan feature.
2. Implement feature.
3. Test feature.
4. Git commit.
5. Update documentation.
6. Continue to next milestone.

## 3. INFRASTRUCTURE BASELINE

Operating system:
- Windows 11
- PowerShell
- VS Code
- Git
- Docker Desktop

Hardware:
- MSI Vector GP66 12UHSO
- Intel i9-12900H
- 64 GB DDR5 RAM
- NVIDIA RTX 3080 Ti Laptop GPU, 16 GB VRAM

AI platform:
- Hermes Agent v0.23.1
- Ollama 0.40.16
- Primary configured model: qwen3.5:9b
- Local inference with GPU acceleration

Ollama endpoint:
- Windows host: port 11434
- Docker access: http://host.docker.internal:11434/v1

Other infrastructure:
- Docker sandbox image: nousresearch/hermes-sandbox:desktop
- Dedicated Hermes workspace:
  C:\Users\jaymo\hermes-workspace
- Workspace container mount: /workspace
- n8n: http://localhost:5678
- n8n instance-level MCP configured

The user previously confirmed the dedicated workspace filesystem
isolation and actual Hermes sandbox mount audit.

Do not repeat the Docker security audit unless requested.

## 4. ARCHITECTURE

Windows 11 Host
|
+-- Ollama
|   +-- Local language models
|   +-- GPU inference
|
+-- Hermes Agent
|   +-- Central AI platform
|   +-- Tool routing
|   +-- MCP connections
|   +-- Agent coordination
|
+-- Docker Sandbox
|   +-- Restricted execution
|   +-- Dedicated workspace
|
+-- Controlled Integration Services
|   +-- Google Drive MCP
|   +-- Future external API integrations
|
+-- n8n
    +-- Workflow automation
    +-- Instance-level MCP

Security principles:
- Separate reasoning from execution.
- Keep external credentials outside the sandbox.
- Expose narrow, approved integration actions.
- Validate inputs before external actions.
- Do not give agents unrestricted Windows or account access.
- Use deterministic permission controls beneath AI reasoning.

## 5. GOOGLE DRIVE INTEGRATION — COMPLETED MILESTONE

Date: November 15, 2026

Integration workspace:
C:\Users\jaymo\Hermes-integrations

Current structure:

Hermes-integrations\
    .gitignore
    HANDOFF.md
    credentials\
        client_secret.json
        token.json
    google-drive\
        .venv\
        drive_test.py
        friday_drive_server.py
    logs\

Google Cloud project:
Friday-Home-Integrations

Google account:
Hermes.workspacefriday@gmail.com

Enabled APIs:
- Google Drive API
- Google Docs API

OAuth configuration:
- External audience
- Testing mode
- User added as test user
- OAuth scope: drive.file

Historical OAuth names:
- Jarvis Home Assistant
- Jarvis-Drive-Local

Do not rename existing OAuth resources without approval.

Credentials:
- client_secret.json
- token.json

Credential directory:
C:\Users\jaymo\Hermes-integrations\credentials

Credentials must not be pasted into conversations, prompts,
Git repositories, or the Docker sandbox.

Python environment:
C:\Users\jaymo\Hermes-integrations\google-drive\.venv

Python version:
3.10.6

Installed packages include:
- google-api-python-client
- google-auth-httplib2
- google-auth-oauthlib
- mcp 2.3.0

A Google library emitted a Python 3.10 support warning.
The server nevertheless started and completed the integration test.
Consider a controlled Python upgrade later; do not disrupt the
working environment during this milestone.

## 6. FRIDAY GOOGLE DRIVE MCP SERVER

Server file:
google-drive\friday_drive_server.py

Hermes MCP server name:
friday-google-drive

Registered through Hermes using the dedicated Python executable.

Command registration:

hermes mcp add friday-google-drive --command "C:\Users\jaymo\Hermes-integrations\google-drive\.venv\Scripts\python.exe" --args "C:\Users\jaymo\Hermes-integrations\google-drive\friday_drive_server.py"

MCP tool exposed:
create_google_doc

The server also reports standard MCP capabilities:
- list_prompts
- list_resources
- read_resource
- get_prompt

The intended business action is document creation.

The server:
- Loads the existing Google OAuth token.
- Connects to Google Drive and Google Docs APIs.
- Creates or finds the FRIDAY_TEST folder.
- Creates a Google Docs document.
- Inserts supplied text.
- Returns the document title, ID, and link.

Input limits:
- Title: 150 characters
- Content: 20,000 characters
- Empty title or content is rejected.

The integration is intentionally limited.
It does not provide unrestricted Drive browsing,
file deletion, or Gmail access.

## 7. VERIFIED END-TO-END TEST

Hermes MCP registration:
PASSED

Hermes MCP tool discovery:
PASSED

Actual Hermes tool invocation:
PASSED

Google Docs creation:
PASSED

Test document:
FRIDAY_MCP_Integration_Verification

Document ID:
1pcQfpA_5Xm3-v4FmuMu1neZKFwfPuBbW4mAoROBk8Yk

Document URL:
https://docs.google.com/document/d/1pcQfpA_5Xm3-v4FmuMu1neZKFwfPuBbW4mAoROBk8Yk/edit?usp=drivesdk

This verifies the complete execution path:

User request
  -> Hermes Agent
  -> FRIDAY Google Drive MCP
  -> Google Drive API
  -> Google Docs API
  -> Created document

This is the first verified external action through FRIDAY's
controlled integration architecture.

## 8. CURRENT PROJECT STATUS

Completed or verified:
- Windows and local AI foundation
- Hermes operational
- Ollama local inference
- Docker sandbox operational
- Dedicated workspace isolation
- Controlled workspace path safeguards
- n8n operational
- n8n instance-level MCP
- Google Drive API authentication
- Google Docs API authentication
- Local Google Drive MCP server
- Hermes MCP registration
- Hermes tool discovery
- Successful document creation through Hermes

Not yet completed:
- Git checkpoint for the Google Drive integration
- Full integration failure-handling tests
- Centralized integration logging and monitoring
- Additional external integrations
- Specialized agent configuration and validation
- Full agent delegation workflow

Do not describe planned items as completed.

## 9. NEXT DEVELOPMENT MILESTONE

Preserve and stabilize the working Google Drive integration.

Recommended sequence:

1. Inspect Git status in the integration workspace.
2. Confirm credentials and tokens remain excluded from Git.
3. Review the current MCP server implementation.
4. Test invalid inputs and Google API failure handling.
5. Add safe operational logging.
6. Create a Git commit after tests pass.
7. Update this handoff after the commit.
8. Begin specialized agent configuration.

Planned specialized agents:
- Terminal Agent
- Coding Agent
- Research Agent
- Automation Agent

Future architecture:
Hermes Central Coordinator
  -> Planning and delegation
  -> Specialized agents
  -> Controlled execution
  -> Approved integrations
  -> Results returned to coordinator

## 10. CONTINUATION INSTRUCTIONS

When continuing this project:

1. Read this handoff first.
2. Do not restart the project.
3. Preserve the existing working Google Drive integration.
4. Use the current Hermes-integrations directory.
5. Inspect actual files before modifying them.
6. Continue from the next incomplete milestone.
7. Work one command or implementation step at a time.
8. Test before committing.
9. Never expose credentials.
10. Update this handoff at major milestones.

CURRENT CHECKPOINT:

FRIDAY has successfully completed its first end-to-end
external integration using Hermes MCP and Google Docs.

The next milestone is stabilization, Git preservation,
and controlled expansion of specialized agents.
