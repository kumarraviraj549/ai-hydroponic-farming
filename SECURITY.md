# Security Guidelines

## 🔒 Important Security Notice

This document outlines critical security practices for the HydroAI project. **Please read carefully before contributing or deploying.**

## 🚨 GitGuardian Alert Response

If you received a GitGuardian alert about exposed credentials:

1. **Immediate Actions Taken:**
   - All example environment files contain only placeholder values
   - Actual `.env` files are properly gitignored
   - No real credentials are committed to this repository

2. **Verification Steps:**
   - ✅ `.gitignore` includes all environment files
   - ✅ `.env.example` contains only safe placeholder values
   - ✅ No hardcoded credentials in source code
   - ✅ All sensitive data uses environment variables

## 🛡️ Environment Variables Security

### DO NOT COMMIT:
- `.env` files with real credentials
- Hardcoded API keys, passwords, or tokens
- Database connection strings with real credentials
- Email passwords or app-specific passwords

### ALWAYS:
- Use environment variables for all sensitive data
- Keep `.env` files in `.gitignore`
- Use `.env.example` with placeholder values only
- Generate strong, unique passwords for each service

## 📧 Email Configuration Security

### For Gmail SMTP:
1. **Never use your main Gmail password**
2. **Generate App-Specific Password:**
   - Go to [Google Account Security](https://myaccount.google.com/security)
   - Enable 2-Step Verification
   - Generate App Password at [App Passwords](https://myaccount.google.com/apppasswords)
   - Use the 16-character app password in `MAIL_PASSWORD`

### Environment Setup:
```bash
# Copy the example file
cp backend/.env.example backend/.env

# Edit with your actual values (NEVER commit this file)
vim backend/.env
```

## 🔐 Production Security Checklist

- [ ] All environment variables are set via deployment platform
- [ ] No `.env` files are deployed to production
- [ ] Database credentials are rotated regularly
- [ ] API keys have proper scope limitations
- [ ] SSL/TLS is enforced for all connections
- [ ] CSRF protection is enabled
- [ ] Rate limiting is implemented
- [ ] Security headers are configured

## 🚀 Deployment Security

### Environment Variables by Platform:

**Vercel/Netlify:**
```bash
# Set via dashboard or CLI
vercel env add SECRET_KEY
```

**Docker:**
```bash
# Use secrets or env files outside repo
docker run --env-file /secure/path/.env app
```

**Kubernetes:**
```yaml
# Use ConfigMaps and Secrets
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  SECRET_KEY: <base64-encoded-value>
```

## 📊 Security Monitoring

- GitGuardian scans for exposed secrets
- Dependabot monitors dependency vulnerabilities
- Regular security audits of dependencies
- Automated security testing in CI/CD

## 🆘 Security Incident Response

If credentials are accidentally committed:

1. **Immediately rotate all exposed credentials**
2. **Remove from git history:**
   ```bash
   git filter-branch --force --index-filter \
   'git rm --cached --ignore-unmatch path/to/file' \
   --prune-empty --tag-name-filter cat -- --all
   ```
3. **Force push to all branches**
4. **Notify team members to re-clone repository**
5. **Update all deployment environments**

## 📞 Contact

For security concerns or questions:
- Create a private security issue
- Email: kumarraviraj549@gmail.com
- Mark as "SECURITY" in subject line

---

**Remember: Security is everyone's responsibility. When in doubt, ask for review.**