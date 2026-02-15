# Laptop Tools

Network diagnostic tools for field work. Run from the laptop, results are filed into project directories and registered in the Precept SQLite database.

## Setup

1. Copy `precept-scan.sh` to somewhere on your PATH:
   ```bash
   sudo cp precept-scan.sh /usr/local/bin/precept-scan
   ```

2. Ensure SSH key auth works to the dev server:
   ```bash
   ssh jason@10.0.10.21 echo ok
   ```

3. Projects directory must exist at `~/Projects/` (or set `PROJECTS_DIR`).

## Usage

### Network scans

```bash
# nmap scan
precept-scan nmap fairfield-water "10.0.10.0/24"
precept-scan nmap fairfield-water "-sV -p 1-1000 10.0.10.1"

# iperf3 throughput test
precept-scan iperf3 fairfield-water "-c 10.0.10.1 -t 30"
precept-scan iperf3 fairfield-water "-c 10.0.10.1 -u -b 100M"

# File any existing results
precept-scan file fairfield-water wifi-survey /tmp/survey-results.csv
```

### What it does

1. Runs the scan tool (nmap, iperf3)
2. Saves output to `{project}/docs/network/YYYY-MM-DD-{type}-{desc}.txt`
3. Git commits locally
4. SCPs the file to the dev server
5. Registers in the SQLite database via SSH
6. Git commits on the dev server

### Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PRECEPT_DEV_SERVER` | `10.0.10.21` | Dev server hostname/IP |
| `PRECEPT_DEV_USER` | `jason` | SSH username |
| `PROJECTS_DIR` | `~/Projects` | Local projects directory |

## Via Telegram

You can also send any document file to @preceptserver_bot and it will be saved to the active project and logged in the database.
