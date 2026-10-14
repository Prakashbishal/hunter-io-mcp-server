# Hunter.io MCP Server

A Python-based **Model Context Protocol (MCP) server** that integrates the Hunter.io REST API with MCP-compatible AI clients, enabling AI assistants to discover professional email addresses, find individual contacts, and verify email deliverability.

Built using Python, the official MCP Python SDK, HTTPX, Pydantic, and Hunter.io API v2.

## Overview

AI assistants cannot directly interact with external services unless appropriate tools or integrations are available.

This project bridges that gap by exposing Hunter.io's contact discovery capabilities as structured MCP tools.

The server acts as an intermediary between an MCP-compatible AI client and Hunter.io, handling API authentication, input validation, HTTP requests, response processing, and common API errors.

## Features

- **Domain Search:** Discover professional email addresses associated with a company domain.
- **Email Finder:** Find a person's professional email using their first name, last name, and company domain.
- **Email Verifier:** Check an email address using Hunter.io's verification service.
- **Input Validation:** Validate email formats, domain names, and personal names using Pydantic.
- **Secure Configuration:** Load API credentials from environment variables using `python-dotenv`.
- **API Error Handling:** Handle authentication failures, rate limiting, connection failures, and HTTP errors.
- **MCP Integration:** Expose all three operations as discoverable and callable MCP tools.

## System Architecture

```text
        MCP-Compatible AI Client
                  |
                  | MCP Tool Call
                  v
          MCP Server (server.py)
                  |
                  | Input Validation
                  v
       Hunter Client (hunter_client.py)
                  |
                  | HTTPX GET Request
                  v
            Hunter.io REST API
                  |
                  | JSON Response
                  v
       Response Processing & Parsing
                  |
                  v
            MCP Tool Result
                  |
                  v
                AI Client
```

The architecture separates MCP tool registration from external API communication, improving maintainability and code reuse.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core implementation |
| MCP Python SDK | MCP server and tool registration |
| HTTPX | HTTP communication with Hunter.io |
| Pydantic | Input validation |
| python-dotenv | Environment variable management |
| Hunter.io API v2 | Professional contact discovery and verification |
| MCP Inspector | Interactive tool testing |

## Project Structure

```text
hunter-mcp/
├── hunter_client.py
├── server.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

**`hunter_client.py`** — Implements Hunter.io API communication, JSON parsing, reusable HTTP request handling, and error handling.

**`server.py`** — Registers MCP tools and validates incoming arguments.

**`.env`** — Stores the Hunter.io API key locally. This file must not be committed to Git.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/<YOUR_USERNAME>/<REPOSITORY_NAME>.git
cd <REPOSITORY_NAME>
```

Replace the placeholders with the actual repository information after publishing.

### 2. Create a Virtual Environment

On Windows PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

For development with MCP Inspector, ensure that `uv` is also installed and available on your PATH.

### 4. Configure the API Key

Create a `.env` file in the project root:

```env
HUNTER_API_KEY=test-api-key
```

Hunter.io provides `test-api-key` for testing API integration with predefined sample responses.

For real contact discovery and verification, replace it with your own API key from the [Hunter.io dashboard](https://hunter.io/dashboard).

**Never commit your real API key to GitHub.**

## Available MCP Tools

### 1. `find_company_emails`

Discovers professional email addresses associated with a company domain.

**Input:**

```json
{
  "domain": "stripe.com"
}
```

**Returns:** Organization name, total reported results, and a list of email addresses.

### 2. `find_person_email_tool`

Attempts to find a person's professional email using their name and company domain.

**Input:**

```json
{
  "first_name": "Alexis",
  "last_name": "Ohanian",
  "domain": "reddit.com"
}
```

**Returns:** First name, last name, email address, and Hunter.io's confidence score, where available.

### 3. `verify_professional_email`

Checks an email address using Hunter.io's Email Verifier API.

**Input:**

```json
{
  "email": "richard@piedpiper.com"
}
```

**Returns:** Email address, verification status, and score.

Verification results are estimates based on Hunter.io's checks and do not guarantee successful email delivery.

## Running the MCP Server

Start the server using:

```powershell
python server.py
```

The server uses standard input/output (stdio) transport to communicate with an MCP client.

### Testing with MCP Inspector

Run:

```powershell
mcp dev server.py --with httpx --with python-dotenv --with email-validator
```

Open MCP Inspector and connect to the server.

1. Navigate to the Tools section.
2. Select a registered MCP tool.
3. Enter the required parameters.
4. Execute the tool.
5. Inspect the returned response or validation error.

All three MCP tools have been manually tested using MCP Inspector with Hunter.io's test API key.

## Input Validation

The server uses Pydantic to validate incoming tool arguments before making external API requests.

| Input | Validation |
|---|---|
| Email address | Email format validation using `EmailStr` |
| Domain | Length and basic domain-format validation |
| First name | Whitespace trimming, length constraints, and alphabetic-character validation |
| Last name | Whitespace trimming, length constraints, and alphabetic-character validation |

Input validation reduces unnecessary API calls and provides more informative feedback for invalid arguments.

It does not establish that a domain, person, or email address actually exists.

## Error Handling

The API client includes a reusable `hunter_get()` helper responsible for making HTTP requests, checking response status codes, and parsing successful JSON responses.

Implemented handling includes:

| Error | Behaviour |
|---|---|
| HTTP 401 | Authentication failure |
| HTTP 429 | Rate-limit error |
| Other HTTP 4xx/5xx | API error containing the status code |
| Connection or network errors | Connection error message |
| Request timeout | Handled as an HTTPX request error |

The client avoids including complete request URLs in its custom error messages because API keys may be passed as query parameters.

## Security

API credentials are loaded through environment variables instead of being hardcoded.

The `.gitignore` file excludes sensitive and generated files:

```gitignore
.env
.venv/
__pycache__/
*.pyc
.pytest_cache/
```

Additional security considerations:

- Do not expose API credentials in logs or public repositories.
- Rotate any compromised API keys.
- Avoid logging complete authenticated request URLs.
- Use professional contact information responsibly and comply with applicable privacy requirements.

## Current Limitations

This project is a working MCP prototype and is not yet production-ready.

- Automated unit and integration tests have not yet been added.
- HTTP 202 pending email-verification responses are not fully handled.
- Automatic retries and exponential backoff are not implemented.
- Domain and name validation check basic format rather than real-world existence.
- Live API requests depend on Hunter.io account permissions, quotas, and service availability.
- Docker packaging and deployment are not yet implemented.

## Future Improvements

- Add automated tests with pytest and mocked HTTP responses.
- Improve error handling for pending verification and unexpected API responses.
- Implement retry logic and rate-limit-aware backoff.
- Introduce structured logging and configuration management.
- Add Docker support.
- Test integration with additional MCP-compatible AI clients.
- Improve documentation and usage examples.

## References

- [Hunter.io API Documentation](https://hunter.io/api-documentation)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [HTTPX Documentation](https://www.python-httpx.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## License

No license has been selected yet. A license can be added before public distribution.
