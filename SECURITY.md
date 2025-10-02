# Security Guidelines for HydroAI Platform

## 🔒 Critical Security Practices

### Environment Variables & Secrets Management

#### ✅ DO:
- **Always use `.env` files for secrets** - Never hardcode credentials
- **Use App-Specific Passwords** for Gmail/email services
- **Generate strong secrets** using Python's `secrets` module:
  ```python
  import secrets
  secrets.token_hex(32)  # For SECRET_KEY
  secrets.token_urlsafe(32)  # For JWT keys
  ```
- **Keep `.env` in `.gitignore`** (already configured)
- **Use different credentials** for development vs production
- **Rotate credentials regularly** (quarterly minimum)

#### ❌ NEVER:
- Commit `.env` files to git
- Use your main email password for SMTP
- Share credentials in plain text
- Use default or weak passwords
- Store production credentials in development files

### Gmail Integration Security

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to [Google Account Settings](https://myaccount.google.com/apppasswords)
   - Select "Mail" and your device
   - Copy the 16-character password
3. **Use App Password** in `MAIL_PASSWORD`, not your main password

### Repository Security

#### Pre-commit Security Checks
Install and configure git hooks to prevent credential commits:

```bash
# Install detect-secrets
pip install detect-secrets

# Initialize detection
detect-secrets scan --baseline .secrets.baseline

# Add pre-commit hook
echo '#!/bin/sh\ndetect-secrets-hook --baseline .secrets.baseline' > .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

#### GitHub Security Features
- Enable **Dependabot alerts** for dependency vulnerabilities
- Use **GitHub Secrets** for CI/CD environment variables
- Enable **Secret scanning** (already active)
- Review **Security advisories** regularly

### Production Deployment Security

#### Environment Configuration
```bash
# Production-ready settings
FLASK_ENV=production
DEBUG=false
SECURE_SSL_REDIRECT=true
SESSION_COOKIE_SECURE=true
CSRF_COOKIE_SECURE=true
```

#### Database Security
- Use **PostgreSQL** in production (not SQLite)
- Enable **SSL connections**
- Use **connection pooling**
- Regular **backups** with encryption

#### API Security
- Implement **rate limiting**
- Use **HTTPS only**
- Validate **all inputs**
- Log **security events**

## 🚨 Incident Response

### If Credentials Are Exposed:

1. **Immediate Actions** (within 5 minutes):
   - Change the exposed password/key immediately
   - Revoke API keys/tokens
   - Check for unauthorized access

2. **Investigation** (within 1 hour):
   - Review git history for other exposures
   - Check application logs for suspicious activity
   - Audit all related accounts

3. **Remediation** (within 24 hours):
   - Force password reset for affected accounts
   - Update all affected systems
   - Document the incident

4. **Prevention** (ongoing):
   - Implement additional security measures
   - Review and update security practices
   - Conduct security training if needed

## 📋 Security Checklist

### Development
- [ ] `.env` files are in `.gitignore`
- [ ] No hardcoded credentials in code
- [ ] Using App Passwords for email
- [ ] Strong, unique passwords/keys
- [ ] Pre-commit hooks configured

### Deployment
- [ ] HTTPS enforced
- [ ] Database encryption enabled
- [ ] Regular security updates
- [ ] Monitoring and logging active
- [ ] Backup and recovery tested

### Maintenance
- [ ] Quarterly credential rotation
- [ ] Security audit every 6 months
- [ ] Dependency updates monthly
- [ ] Access review quarterly

## 🔗 Security Resources

- [OWASP Security Guidelines](https://owasp.org/)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [Flask Security Documentation](https://flask.palletsprojects.com/en/2.3.x/security/)
- [Python Security Guide](https://python-security.readthedocs.io/)

## 📞 Security Contact

For security issues or questions:
- **Email**: [Your Security Email]
- **Response Time**: Within 24 hours for critical issues

---

**Remember**: Security is everyone's responsibility. When in doubt, ask for help!

*Last Updated: October 2025*