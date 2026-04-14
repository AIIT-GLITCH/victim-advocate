"""Inline HTML templates for Victim Advocate."""

DISCLAIMER = '<div class="alert alert-warning text-center small mt-3"><strong>Disclaimer:</strong> This tool provides general legal information, not legal advice. Consult a licensed attorney for your specific situation.</div>'

BASE_CSS = """
<style>
:root { --primary: #6C3FA0; --secondary: #1ABC9C; --dark: #2C1654; --light: #F5F0FF; }
body { font-family: 'Segoe UI', system-ui, sans-serif; background: var(--light); }
.navbar { background: linear-gradient(135deg, var(--dark), var(--primary)) !important; }
.btn-primary { background: var(--primary); border-color: var(--primary); }
.btn-primary:hover { background: var(--dark); border-color: var(--dark); }
.btn-secondary { background: var(--secondary); border-color: var(--secondary); color: #fff; }
.btn-secondary:hover { background: #16A085; }
.card { border: none; box-shadow: 0 2px 8px rgba(108,63,160,0.1); border-radius: 12px; }
.hero { background: linear-gradient(135deg, var(--dark), var(--primary)); color: white; padding: 80px 0; }
.badge-open { background: var(--secondary); }
.badge-closed { background: #95a5a6; }
footer { background: var(--dark); color: #ccc; padding: 20px 0; margin-top: 40px; }
</style>
"""

NAV_LOGGED_OUT = """
<nav class="navbar navbar-expand-lg navbar-dark mb-4">
<div class="container">
  <a class="navbar-brand fw-bold" href="/">&#x1f6e1; Victim Advocate</a>
  <div class="navbar-nav ms-auto">
    <a class="nav-link" href="/rights">Know Your Rights</a>
    <a class="nav-link" href="/resources">Resources</a>
    <a class="nav-link" href="/pricing">Pricing</a>
    <a class="nav-link" href="/about">About</a>
    <a class="nav-link btn btn-secondary btn-sm ms-2 px-3" href="/login">Login</a>
  </div>
</div>
</nav>
"""

NAV_LOGGED_IN = """
<nav class="navbar navbar-expand-lg navbar-dark mb-4">
<div class="container">
  <a class="navbar-brand fw-bold" href="/">&#x1f6e1; Victim Advocate</a>
  <div class="navbar-nav ms-auto">
    <a class="nav-link" href="/rights">Know Your Rights</a>
    <a class="nav-link" href="/resources">Resources</a>
    <a class="nav-link" href="/dashboard">My Cases</a>
    <a class="nav-link btn btn-secondary btn-sm ms-2 px-3" href="/logout">Logout</a>
  </div>
</div>
</nav>
"""

FOOTER = """
<footer class="text-center">
  <div class="container">
    <p class="mb-1">&copy; 2025 AIIT Apps Division | Victim Advocate</p>
    <p class="small mb-0">If you are in immediate danger, call 911.</p>
  </div>
</footer>
"""

def page(title, body, logged_in=False):
    nav = NAV_LOGGED_IN if logged_in else NAV_LOGGED_OUT
    return f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | Victim Advocate</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
{BASE_CSS}
</head><body>
{nav}
<div class="container">{body}</div>
{DISCLAIMER}
{FOOTER}
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body></html>"""

INDEX_BODY = """
<div class="hero text-center rounded-4 mb-4" style="margin-top:-24px;">
  <h1 class="display-4 fw-bold">You Are Not Alone</h1>
  <p class="lead mt-3 mb-4">Free, confidential information about your legal rights as a crime victim.</p>
  <form action="/rights" method="get" class="row g-2 justify-content-center px-3">
    <div class="col-auto">
      <select name="state" class="form-select" required>
        <option value="">Select State...</option>
        {{STATE_OPTIONS}}
      </select>
    </div>
    <div class="col-auto">
      <select name="crime" class="form-select" required>
        <option value="">Type of Crime...</option>
        {{CRIME_OPTIONS}}
      </select>
    </div>
    <div class="col-auto">
      <button class="btn btn-secondary btn-lg" type="submit">Know Your Rights &rarr;</button>
    </div>
  </form>
</div>
<div class="row g-4 mb-4">
  <div class="col-md-4"><div class="card p-4 text-center h-100">
    <h3>&#x1f4d6;</h3><h5>Know Your Rights</h5>
    <p>Search by state and crime type. Understand your protections, statutes, and restitution options.</p>
  </div></div>
  <div class="col-md-4"><div class="card p-4 text-center h-100">
    <h3>&#x1f4de;</h3><h5>Find Help Now</h5>
    <p>National hotlines, local shelters, legal aid. All free, all confidential.</p>
    <a href="/resources" class="btn btn-primary btn-sm">Find Resources</a>
  </div></div>
  <div class="col-md-4"><div class="card p-4 text-center h-100">
    <h3>&#x1f4cb;</h3><h5>Track Your Case</h5>
    <p>Pro members can track case events, upload documents, and generate reports.</p>
    <a href="/pricing" class="btn btn-primary btn-sm">Learn More</a>
  </div></div>
</div>
<div class="card p-4 text-center bg-white">
  <h5 class="text-danger">In Immediate Danger?</h5>
  <p class="mb-1"><strong>Call 911</strong> | National DV Hotline: <strong>1-800-799-7233</strong> | Crisis Text: <strong>Text HOME to 741741</strong></p>
</div>
"""