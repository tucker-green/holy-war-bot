# Cloud Deployment Guide for Holy War Bot

This guide will help you deploy the bot to run 24/7 in the cloud.

## Option 1: Oracle Cloud Free Tier (Recommended - FREE)

Oracle Cloud offers a generous free tier that's perfect for running this bot.

### Step 1: Create Oracle Cloud Account
1. Go to [Oracle Cloud Free Tier](https://www.oracle.com/cloud/free/)
2. Sign up for a free account
3. Select a region close to you

### Step 2: Create a VM Instance
1. Click "Create a VM Instance"
2. Choose these settings:
   - **Image**: Ubuntu 22.04 (or latest LTS)
   - **Shape**: VM.Standard.E2.1.Micro (Always Free)
   - **Add SSH Keys**: Generate a new key pair and download it
3. Click "Create"
4. Note your instance's **Public IP Address**

### Step 3: Connect to Your Server
```bash
# On your local machine
chmod 400 /path/to/your-ssh-key.key
ssh -i /path/to/your-ssh-key.key ubuntu@YOUR_PUBLIC_IP
```

### Step 4: Install Dependencies on Server
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip git -y

# Install Firefox and dependencies for Playwright
sudo apt install firefox -y
```

### Step 5: Clone and Setup Your Bot
```bash
# Clone your repository
git clone https://github.com/tucker-green/holy-war-bot.git
cd holy-war-bot

# Install Python dependencies
pip3 install -r requirements.txt

# Install Playwright browsers
playwright install firefox
playwright install-deps firefox

# Create config file
cp config.example.py config.py
nano config.py  # Edit with your credentials
# Make sure to set HEADLESS = True
```

### Step 6: Run the Bot with Screen (keeps it running)
```bash
# Install screen
sudo apt install screen -y

# Start a new screen session
screen -S holywar

# Run the bot
python3 holy_war_bot.py

# Detach from screen: Press Ctrl+A, then D
# To reattach later: screen -r holywar
# To see logs: screen -r holywar
```

### Step 7: Setup Automatic Restart (Optional)
Create a systemd service to auto-restart the bot:

```bash
sudo nano /etc/systemd/system/holywar-bot.service
```

Paste this content:
```ini
[Unit]
Description=Holy War Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/holy-war-bot
ExecStart=/usr/bin/python3 /home/ubuntu/holy-war-bot/holy_war_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl enable holywar-bot
sudo systemctl start holywar-bot

# Check status
sudo systemctl status holywar-bot

# View logs
sudo journalctl -u holywar-bot -f
```

---

## Option 2: DigitalOcean Droplet ($4/month)

### Step 1: Create DigitalOcean Account
1. Go to [DigitalOcean](https://www.digitalocean.com/)
2. Sign up (get $200 credit for 60 days with referral links)

### Step 2: Create a Droplet
1. Click "Create" → "Droplets"
2. Choose:
   - **Image**: Ubuntu 22.04 LTS
   - **Plan**: Basic ($4/month - 512MB RAM)
   - **Datacenter**: Closest to you
   - **Authentication**: SSH Key (generate if needed)
3. Click "Create Droplet"

### Step 3: Follow Same Steps as Oracle Cloud
Use steps 3-7 from Oracle Cloud guide above.

---

## Option 3: AWS EC2 (Free for 12 months)

### Step 1: Create AWS Account
1. Go to [AWS Free Tier](https://aws.amazon.com/free/)
2. Sign up for free tier

### Step 2: Launch EC2 Instance
1. Go to EC2 Dashboard
2. Click "Launch Instance"
3. Choose:
   - **AMI**: Ubuntu Server 22.04 LTS
   - **Instance Type**: t2.micro (Free tier eligible)
   - **Key Pair**: Create and download
4. Configure Security Group (allow SSH port 22)
5. Launch instance

### Step 3: Connect and Setup
```bash
ssh -i /path/to/your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

Follow steps 4-7 from Oracle Cloud guide.

---

## Important Notes

### 1. Set Bot to Headless Mode
In your `config.py`, make sure:
```python
HEADLESS = True  # Must be True for cloud deployment
```

### 2. Monitor Your Bot
Check logs regularly:
```bash
# If using screen
screen -r holywar

# If using systemd
sudo journalctl -u holywar-bot -f

# Check bot is running
ps aux | grep python3
```

### 3. Update Your Bot
```bash
cd /home/ubuntu/holy-war-bot
git pull origin main
sudo systemctl restart holywar-bot  # If using systemd
```

### 4. Stop the Bot
```bash
# If using screen
screen -r holywar
# Then press Ctrl+C to stop

# If using systemd
sudo systemctl stop holywar-bot
```

---

## Troubleshooting

### Bot Crashes or Stops
```bash
# Check what went wrong
sudo journalctl -u holywar-bot -n 100

# Or check the log file
tail -f /home/ubuntu/holy-war-bot/bot.log
```

### Firefox/Playwright Issues
```bash
# Reinstall Playwright browsers
playwright install firefox
playwright install-deps firefox
```

### Memory Issues (if droplet has <1GB RAM)
```bash
# Add swap space
sudo fallocate -l 1G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

---

## Cost Comparison

| Provider | Cost | Free Tier | RAM | Best For |
|----------|------|-----------|-----|----------|
| Oracle Cloud | **FREE** | Forever | 1GB | Best value |
| DigitalOcean | $4/mo | $200/60 days | 512MB | Easiest |
| AWS EC2 | Free/~$5 | 12 months | 1GB | Most flexible |

**Recommendation**: Start with **Oracle Cloud Free Tier** - it's completely free forever and has enough resources for your bot.

---

## Quick Start Command Summary

```bash
# 1. Connect to server
ssh -i your-key.key ubuntu@YOUR_IP

# 2. Install everything
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip git firefox screen -y

# 3. Clone and setup
git clone https://github.com/tucker-green/holy-war-bot.git
cd holy-war-bot
pip3 install -r requirements.txt
playwright install firefox
playwright install-deps firefox

# 4. Configure
cp config.example.py config.py
nano config.py  # Edit credentials and set HEADLESS = True

# 5. Run with screen
screen -S holywar
python3 holy_war_bot.py

# 6. Detach (Ctrl+A, then D)
# Your bot is now running 24/7!
```

---

## Security Tips

1. **Never commit config.py** - It's already in .gitignore
2. **Use SSH keys** - Not passwords
3. **Update regularly**: `sudo apt update && sudo apt upgrade`
4. **Monitor resource usage**: `htop` or `top`
5. **Setup firewall** (optional):
   ```bash
   sudo ufw allow 22/tcp
   sudo ufw enable
   ```

---

Need help? Check the logs or reach out!

