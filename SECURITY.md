# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Security Best Practices

### GitHub Token

- **Never commit tokens** to the repository
- Use environment variables: `export GITHUB_TOKEN="your_token"`
- Token only needs **read access to public repositories**
- No scopes/permissions required for public repo access
- Rotate tokens periodically

### Running the Tool

- The tool only makes **read-only API calls** to GitHub
- No write operations are performed
- No data is sent to external services
- Cache is stored locally in `~/.gitish/cache/`

### For Contributors

- Never commit `.env` files
- Never commit tokens or API keys
- Use `.gitignore` to exclude sensitive files
- Review code for hardcoded credentials before committing

## Reporting a Vulnerability

If you discover a security vulnerability, please:

1. **DO NOT** open a public issue
2. Email: [your-email@example.com] (or use GitHub Security Advisories)
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will respond within 48 hours and work with you to address the issue.

## Security Features

- ✅ No hardcoded credentials
- ✅ Environment variable for token
- ✅ Read-only GitHub API access
- ✅ Local file-based caching only
- ✅ No external data transmission
- ✅ No database or persistent storage
- ✅ HTTPS for all API calls

## Audit Log

- **2026-05-20**: Initial security review completed
- No vulnerabilities found
- All secrets properly externalized
