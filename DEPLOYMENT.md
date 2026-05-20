# Victim Advocate Deployment

Status: live on owned AIIT domain
Date: 2026-05-20

Public URL:

- https://victim-advocate.aiit-threshold.com

Runtime:

- Local Flask/Gunicorn app on `127.0.0.1:5100`
- User systemd service: `victim-advocate.service`
- Cloudflare Tunnel ingress: `/home/buddy_ai/.cloudflared/buddy-rig.yml`
- Tunnel DNS route: `victim-advocate.aiit-threshold.com`

Operational commands:

```bash
systemctl --user status victim-advocate.service
systemctl --user restart victim-advocate.service
curl -fsS http://127.0.0.1:5100/api/stats
curl -fsS https://victim-advocate.aiit-threshold.com/api/stats
```

Public AI behavior:

- The public service must not carry an AIIT-owned `ANTHROPIC_API_KEY`.
- Users can bring their own Anthropic API key through the UI for chat and appeal-letter generation.
- Evidence packets, deadline calculators, ACE impact, crisis resources, search, and category APIs work without an API key.
