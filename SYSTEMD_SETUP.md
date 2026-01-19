# Setting Up a Systemd Service for Auto-Start on Boot

This guide explains how to configure a service to automatically start when your system boots, using systemd.

## Overview

We will create a systemd service unit file that tells the system:
- What program to run
- When to start it
- How to restart it if it fails
- Which user to run it as

## Step-by-Step Setup

### Step 1: Create the Service File

Create a new service file in `/etc/systemd/system/`:

```bash
sudo nano /etc/systemd/system/md-processor.service
```

### Step 2: Add the Service Configuration

Paste the following content:

```ini
[Unit]
Description=MD Processor Web Service
After=network.target

[Service]
Type=simple
User=yash
WorkingDirectory=/home/yash/git/personal/md-processor
ExecStart=/usr/bin/python3 /home/yash/git/personal/md-processor/server.py
Restart=always
RestartSec=5
Environment=PORT=5001

[Install]
WantedBy=multi-user.target
```

Save and exit (Ctrl+X, then Y, then Enter in nano).

### Step 3: Reload Systemd

Tell systemd to recognize the new service:

```bash
sudo systemctl daemon-reload
```

### Step 4: Enable the Service (Auto-Start on Boot)

```bash
sudo systemctl enable md-processor.service
```

### Step 5: Start the Service Now

```bash
sudo systemctl start md-processor.service
```

### Step 6: Verify It's Running

```bash
systemctl status md-processor.service
```

You should see `active (running)` in the output.

---

## Configuration Explained

| Section | Key | Description |
|---------|-----|-------------|
| `[Unit]` | `Description` | Human-readable name for the service |
| `[Unit]` | `After` | Start this service after network is available |
| `[Service]` | `Type` | `simple` means the process started is the main process |
| `[Service]` | `User` | Run the service as this user (not root) |
| `[Service]` | `WorkingDirectory` | Set the current directory before starting |
| `[Service]` | `ExecStart` | The command to run |
| `[Service]` | `Restart` | `always` means restart if the process exits |
| `[Service]` | `RestartSec` | Wait 5 seconds before restarting |
| `[Service]` | `Environment` | Set environment variables |
| `[Install]` | `WantedBy` | Start during normal multi-user boot |

---

## Common Commands

| Command | Description |
|---------|-------------|
| `sudo systemctl start md-processor` | Start the service |
| `sudo systemctl stop md-processor` | Stop the service |
| `sudo systemctl restart md-processor` | Restart the service |
| `sudo systemctl status md-processor` | Check status |
| `sudo systemctl enable md-processor` | Enable auto-start on boot |
| `sudo systemctl disable md-processor` | Disable auto-start on boot |
| `journalctl -u md-processor -f` | View live logs |
| `journalctl -u md-processor --since "1 hour ago"` | View recent logs |

---

## Alternative: Using Gunicorn (Production)

For production use, replace the `ExecStart` line with gunicorn:

```ini
ExecStart=/usr/bin/gunicorn server:app --bind 0.0.0.0:5001 --timeout 120 --workers 2
```

Make sure gunicorn is installed: `pip install gunicorn`

---

## Troubleshooting

### Service won't start
```bash
# Check detailed logs
journalctl -u md-processor.service -n 50 --no-pager
```

### Permission denied errors
- Ensure the `User` in the service file has read/execute access to the script
- Check file permissions: `ls -la /home/yash/git/personal/md-processor/`

### Port already in use
```bash
# Find what's using the port
lsof -i :5001
```

### Changes to service file not taking effect
```bash
# Always reload after editing the service file
sudo systemctl daemon-reload
sudo systemctl restart md-processor
```

---

## Quick Setup Script

Run this to set everything up in one go:

```bash
# Create the service file
sudo tee /etc/systemd/system/md-processor.service > /dev/null << 'EOF'
[Unit]
Description=MD Processor Web Service
After=network.target

[Service]
Type=simple
User=yash
WorkingDirectory=/home/yash/git/personal/md-processor
ExecStart=/usr/bin/python3 /home/yash/git/personal/md-processor/server.py
Restart=always
RestartSec=5
Environment=PORT=5001

[Install]
WantedBy=multi-user.target
EOF

# Reload, enable, and start
sudo systemctl daemon-reload
sudo systemctl enable md-processor.service
sudo systemctl start md-processor.service

# Check status
systemctl status md-processor.service
```
