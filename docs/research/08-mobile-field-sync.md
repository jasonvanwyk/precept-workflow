---

# Field Data Sync for Solo IT Technicians: Research Report

## For Precept Systems -- Jason van Wyk, Howick, KZN, South Africa

---

## 1. Current State Analysis

Based on examining the existing project structure at `/home/jason/Projects/`, each client project follows a consistent template (`/home/jason/Projects/ict_project_template/`) with:

- `CLAUDE.md`, `README.md`, `STATUS.md`, `RESUME.md` -- structured markdown files
- `correspondence/` -- dated client communication logs
- `docs/` -- planning documents, proposals, checklists
- `pics/` -- site photos and screenshots
- Git/GitHub for version control

The real-world evidence from `/home/jason/Projects/jenkins-network/pics/` reveals a common field problem: photos arrive with inconsistent naming -- UUID filenames (`22f884bd-...jpeg`), WhatsApp downloads (`WhatsApp Image 2026-01-06 at 13.35.20.jpeg`), generic names (`unnamed (1).jpg`), and original camera names (`IMG_4776.HEIC` in the `originals/` subfolder). This is precisely the chaos that a mobile workflow should address.

---

## 2. How the Industry Handles Field Data Capture

The field service management (FSM) market is projected to reach $9.68 billion by 2030. Enterprise solutions (Salesforce Field Service, Microsoft Dynamics 365, ServiceMax) offer offline-first mobile apps where technicians receive job details, update work orders, capture photos, collect signatures, and process payments on-site. These are overkill for a solo operator.

For MSPs and small IT services, the practical patterns are:

- **Photo-as-documentation**: Take photos on a set schedule at each visit. Use metadata tagging (date, location, description) and standard naming conventions.
- **Standardised checklists**: Pre-visit and on-site checklists (Precept already does this with self-contained HTML documents).
- **Mobile-first data entry**: Technicians increasingly use smartphones as primary capture devices.
- **Offline-first sync**: All data captured locally first, synced when connectivity is available.

The key insight from MSP best practices: documentation should happen *during* the visit, not after. Waiting until you get home to organise notes and photos means lost context.

---

## 3. Git-Based Mobile Workflows

### GitHub Mobile App
The official GitHub Mobile app (iOS/Android) can browse repos, review PRs, edit files, and create commits. However, it does **not** function as a full git client -- you cannot clone repos, manage branches freely, or push bulk file additions. It is useful for quick edits to STATUS.md or RESUME.md while on-site, but not for adding photos.

### Termux (Android) -- The Power Option
Termux provides a full Linux terminal on Android. You can install `git`, `ssh`, `rsync`, and more. The workflow:
1. Install Termux from F-Droid (not Google Play -- the Play Store version is outdated)
2. `pkg install git openssh`
3. Generate SSH keys, add to GitHub
4. Clone project repos into Termux storage
5. Copy photos from phone camera into the repo's `pics/` folder
6. `git add`, `git commit`, `git push`

This works, but the UX is rough -- small screen, command-line file management, manual photo copying between Android storage and Termux storage. Good for power users, impractical as a daily field workflow.

### Working Copy (iOS only)
If Jason ever uses an iPhone or iPad, Working Copy is a polished git client at $35.99 (free for GitHub Student Pack holders). It supports clone, edit, commit, push, and PR creation. It is the gold standard for mobile git, but is iOS-only.

---

## 4. Photo Ingestion Pipelines

This is the highest-value problem to solve. Getting photos from the phone camera into `~/Projects/[client]/pics/` with sensible names.

### Option A: Syncthing (Recommended)
**What it is**: Peer-to-peer file sync, no cloud, no third party, no subscription. Open source. Runs on Android (F-Droid) and Linux natively.

**Configuration for Precept's use case**:
- **Phone side**: Set a shared folder pointing to the phone's camera directory (DCIM). Configure as **Send Only**.
- **Desktop side**: Set the corresponding folder as **Receive Only**, pointing to a staging directory like `~/incoming-photos/`.
- **WiFi-only sync**: Configure Syncthing on Android to sync only on WiFi (critical for South African data costs). Can also restrict to "only when charging."
- **One-way flow**: With Send Only (phone) and Receive Only (desktop), deletions on the phone do not propagate to the desktop.

**Limitations**: Syncthing syncs *all* photos from the camera folder, not per-project. You need a second step to sort photos into the right project folder. There have been reported bugs where Syncthing used mobile data despite WiFi-only settings, so monitoring is wise.

### Option B: FolderSync Pro (Android)
FolderSync syncs specific Android folders to a remote server via SFTP/SSH. Unlike Syncthing, it connects directly to your Linux desktop over SSH, so you can target specific remote directories. You can create multiple "folder pairs" -- for example, mapping a specific phone folder to a specific project's `pics/` directory. It supports scheduled syncs and WiFi-only restrictions.

Cost: Free version available; Pro is a one-time purchase on Google Play.

### Option C: KDE Connect
If Jason runs KDE (or GNOME with the GSConnect extension), KDE Connect provides ad-hoc file transfer between phone and desktop over WiFi. Tap "Send files" on the phone, select photos, and they land in the desktop's Downloads folder. This is manual but simple -- good for sending a handful of photos from a specific visit immediately. No subscription, no configuration complexity.

### Option D: Telegram Bot
Build a simple Telegram bot that receives photos sent to it and saves them to the desktop. The workflow: while on-site, open Telegram, send photos to "Precept Bot" with a caption like "jenkins-network". A Python script on the desktop listens for messages, saves photos to `~/Projects/[caption]/pics/`. This works over mobile data (photos are compressed by Telegram) but loses original resolution unless sent as "files" rather than "photos."

### Option E: Manual USB/ADB Transfer
The lowest-tech option. Plug the phone into the desktop when home, copy photos. Simple but requires discipline and creates a delay between capture and filing.

### Desktop-Side Automation (gitwatch/inotifywait)
Once photos land in a project folder, [gitwatch](https://github.com/gitwatch/gitwatch) can automatically commit them. It uses `inotifywait` to watch a directory and auto-commits on file changes. This closes the loop: photos arrive via Syncthing/FolderSync, a watcher script detects new files, and they get committed to git automatically.

---

## 5. Voice-to-Text for Field Notes

### OpenAI Whisper API (Recommended for simplicity)
- **Cost**: $0.006/minute ($0.36/hour). The GPT-4o Mini Transcribe model is even cheaper at $0.003/minute.
- **Quality**: Excellent with accents, background noise, and technical language. Supports multiple languages.
- **Workflow**: Record voice memo on phone, sync audio file to desktop, run through Whisper API, save output as markdown in the project's `docs/` or `correspondence/` folder.
- **For a solo technician**: At 10 minutes of voice notes per site visit, that is R1-2 per visit. Negligible.

### Self-Hosted Whisper
The model is open source and free. Running it locally on the desktop avoids API costs entirely. However, it requires a GPU for reasonable speed ($276/month for cloud GPU instances, or a local GPU). If Jason has a desktop GPU (even a modest one), this is viable. The `whisper.cpp` project runs efficiently on CPU as well, though slower.

### On-Device Transcription (Android)
Several apps run Whisper directly on the phone:
- **Whisper Notes**: Local-first transcription app, no data leaves the device.
- **NotelyVoice**: Open source, 50+ languages, fully on-device.
- **Easy Transcription**: Uses whisper.cpp locally, available on Google Play and F-Droid.
- **Termux + whisper.cpp**: For the technically adventurous, you can build whisper.cpp in Termux and transcribe directly on the phone.

On-device transcription is slower and uses significant battery, but works completely offline -- ideal for sites with no connectivity.

### Practical Recommendation
Use the phone's built-in voice recorder for capture. Sync the audio files via Syncthing/FolderSync. On the desktop, run a simple script that processes new `.m4a`/`.ogg` files through Whisper (API or local) and outputs `.md` files. This keeps the field workflow minimal (just hit record) and handles the heavy processing at home.

---

## 6. WiFi Survey Tools

### WiFiAnalyzer (Open Source, Android)
Available on F-Droid and Google Play. Features include AP detection, channel signal strength graphing, signal strength over time, channel rating, and distance estimation. Supports export of access point details. Being open source, it is free with no ads or premium tiers.

### WiFi Heatmap (Android)
Supports data export in CSV and Google Earth KML formats. Upload a floor plan, walk the space marking your position, and it builds a signal coverage map. The CSV export is directly useful for including in project documentation.

### NetSpot (Android)
More polished, offers full WiFi heatmaps and site surveys. Projects can be exported to desktop for detailed analysis. PDF and CSV export available. The free tier is limited; paid plans exist.

### Getting Data into Project Files
The practical workflow:
1. Run WiFi survey on-site using WiFiAnalyzer or WiFi Heatmap
2. Export to CSV
3. Sync the CSV to desktop via Syncthing/FolderSync
4. Include in the project's `docs/` folder
5. Optionally, a script could parse the CSV and generate a summary markdown table

---

## 7. Offline-First Considerations

This is critical for South African field work where:
- Many residential sites have poor or no WiFi during initial assessment
- Mobile data is expensive (especially in KZN rural areas)
- Load shedding can take out home internet infrastructure

### The Pattern: Capture Locally, Sync Later
The industry-standard approach (used by Microsoft Dynamics 365 Field Service and others) is:
1. All data written to local storage immediately
2. User sees instant confirmation, no network dependency
3. Changes queued with "pending sync" status
4. Background process monitors connectivity
5. When WiFi is available, queued operations sync in FIFO order
6. Failed syncs retry with exponential backoff

### For Precept's Git-Based System
Syncthing inherently supports this. When the phone and desktop are on the same WiFi (e.g., at home, or on the client's WiFi), Syncthing discovers peers and syncs. When offline, files simply queue. No data is lost, no manual intervention required.

FolderSync also queues operations and retries when connectivity returns.

### Key Settings for Data-Expensive Environments
- **Syncthing**: "Sync only on WiFi" (verify it is actually working; there have been bugs)
- **FolderSync**: Can be configured to sync only on specific WiFi SSIDs (e.g., only your home WiFi, not client WiFi where you might be tethering)
- **Termux rsync**: Schedule to run only when on home WiFi, using Tasker to detect SSID

---

## 8. VPN/Remote Access -- SSH from Phone

### Tailscale (Strongly Recommended)
Tailscale builds a mesh VPN on top of WireGuard. It is the simplest way to securely access your desktop from your phone, anywhere.

- **Free Personal plan**: Up to 3 users, 100 devices. More than enough for a solo technician.
- **Tailscale SSH**: Once Tailscale is running on both phone and desktop, you can SSH into your desktop without managing keys or passwords on the phone. Tailscale handles authentication via WireGuard.
- **NAT traversal**: Works through most networks without port forwarding. Connects phone to desktop even when both are behind NAT.
- **Use case**: From a client site, SSH into the desktop to look up credentials, check project files, or run a quick command. Use Termius (SSH client for Android) connected via Tailscale's private IP.

### Termius (Android SSH Client)
Termius has replaced JuiceSSH (which was removed from the Play Store in 2025/2026 due to abandonment). Termius runs on Android, iOS, Windows, macOS, and Linux with cross-device sync of server lists and SSH keys. The free tier is sufficient for basic SSH access.

### Alternative: WireGuard (Self-Managed)
If you want to avoid any third-party service, set up WireGuard directly. Requires port forwarding on your home router and manual key management. More work than Tailscale, but zero dependency on external services.

### Practical Value
With Tailscale + Termius, Jason can:
- SSH to desktop from any client site
- Read project files (`cat STATUS.md`)
- Look up credentials (`cat credentials.txt`)
- Check git log for previous visit context
- Run scripts (e.g., trigger a Whisper transcription)
- Access the desktop's Syncthing web UI remotely

---

## 9. Existing Integrated Solutions

### Open Source Field Service Management
- **Open FSM** (based on Odoo): Full-featured FSM with scheduling, dispatching, work order management. Overkill for a solo operator, but since Precept already uses Odoo for quoting and invoicing, there could be integration value.
- **OCA field-service** (GitHub: OCA/field-service): Odoo Community Association field service modules. Since Precept uses Odoo, these modules could add mobile work order management to the existing ERP.
- **Budibase/NocoDB**: Low-code platforms that could build a simple mobile-friendly field data capture app, self-hosted.

### The Problem with FSM Software
Most FSM tools assume a dispatching model (office sends jobs to technicians) and are built for teams, not solo operators. They also generally do not integrate with git-based project management. The overhead of maintaining an FSM platform likely exceeds the benefit for a one-person operation.

### Lightweight Alternatives Worth Considering
- **Obsidian** with Git plugin: Markdown editor with mobile apps. The Git plugin enables sync to GitHub. However, the mobile Git implementation is described as "very unstable" and the plugin uses a JavaScript re-implementation of Git rather than native git.
- **Markor** (Android, open source): Plain markdown editor, works completely offline, stores files as plain `.md` files on the filesystem. Combined with Syncthing, Markor could edit project files (STATUS.md, RESUME.md, correspondence notes) on the phone and have them sync to the project repo on the desktop.

---

## 10. Tiered Recommendations

### Tier 1: Minimum Viable Mobile Workflow (Set up in an afternoon)

**Cost**: R0 (all free/open source)
**Complexity**: Low
**Components**:

| Component | Tool | Purpose |
|-----------|------|---------|
| File sync | **Syncthing** (Android + Linux) | Sync photos and files, WiFi-only |
| Markdown editing | **Markor** (Android) | Edit STATUS.md, RESUME.md, write notes on-site |
| Remote access | **Tailscale** (free plan) + **Termius** | SSH to desktop from client sites |
| Photo capture | Phone camera | Take photos normally |
| Voice notes | Phone voice recorder | Record, transcribe later at desk |

**How it works**:
1. Install Syncthing on phone and desktop. Share a single `field-capture/` folder.
2. On-site: Take photos (they save to camera roll as normal). Open Markor, write timestamped notes in a file like `2026-02-07-jenkins-notes.md`. Record voice memos with the phone's recorder.
3. At home: Syncthing syncs everything over home WiFi. Manually move photos and notes from `field-capture/` into the correct project's `pics/` and `docs/` folders. Commit to git.
4. When you need to reference project files on-site: Use Termius + Tailscale to SSH into the desktop and `cat` the relevant files.

**Limitations**: Manual sorting of photos into projects. Voice notes stay as audio unless you manually transcribe. No automatic git commits.

---

### Tier 2: Semi-Automated Workflow (A weekend project)

**Cost**: R100-200 once (FolderSync Pro) + minimal API costs
**Complexity**: Medium
**Additional components over Tier 1**:

| Component | Tool | Purpose |
|-----------|------|---------|
| Targeted sync | **FolderSync Pro** | Sync specific folders via SFTP to specific project dirs |
| Voice transcription | **Whisper API** ($0.006/min) | Transcribe voice memos to markdown |
| Auto-commit | **gitwatch** (Linux) | Watch project folders, auto-commit new files |
| WiFi surveys | **WiFiAnalyzer** (F-Droid) | Export AP data to CSV |
| Note-taking | **Obsidian Mobile** or **Markor** + Syncthing | Edit markdown files that sync to project repos |

**How it works**:
1. Before a site visit, create a folder on the phone named after the project (e.g., `jenkins-network/`).
2. FolderSync is configured with SFTP folder pairs: `phone:/sdcard/field/jenkins-network/` syncs to `desktop:~/Projects/jenkins-network/pics/` on WiFi.
3. On-site: Take photos, move them to the project folder on the phone. Record voice memos into the same folder. Take WiFi readings, export CSV.
4. At home: FolderSync pushes everything to the right project directory over SSH/SFTP. A desktop script runs voice memos through Whisper API and saves `.md` transcripts. gitwatch detects new files and auto-commits.
5. Review auto-commits, clean up transcripts, update STATUS.md.

**Desktop-side script** (conceptual): A watcher that processes incoming `.m4a`/`.ogg` files through the Whisper API, outputs markdown, and deletes the audio original (or archives it). Combined with gitwatch for auto-commits.

---

### Tier 3: Fully Integrated Workflow (A week-long project)

**Cost**: R0-500 once + hardware (if no GPU) + minimal API costs
**Complexity**: High
**Additional components over Tier 2**:

| Component | Tool | Purpose |
|-----------|------|---------|
| On-device transcription | **whisper.cpp** via Termux or NotelyVoice | Transcribe on the phone, offline |
| Telegram bot | Custom Python bot | Send photos with project name as caption, auto-filed |
| Photo renaming | **Tasker** + script | Auto-rename photos with date-project prefix |
| Git from phone | **Termux** + git + SSH keys | Full git operations from the phone |
| Self-hosted Whisper | **whisper.cpp** on desktop | Zero API costs for transcription |
| Automated pipeline | **inotifywait** + scripts | Full automation: photo arrive, rename, commit, push |

**How it works**:
1. Tailscale mesh network connects phone, desktop, and optionally a Raspberry Pi at home for always-on services.
2. Telegram bot running on the desktop (or Pi) receives photos. Caption format: `jenkins-network cable-run-hallway`. Bot saves to `~/Projects/jenkins-network/pics/2026-02-07-cable-run-hallway.jpg` and auto-commits.
3. Termux on the phone has git configured. For text updates (STATUS.md, notes), edit in Markor, then switch to Termux to commit and push.
4. Voice memos transcribed on-device using NotelyVoice or whisper.cpp in Termux. Transcripts saved as markdown, synced via Syncthing.
5. Desktop runs self-hosted whisper.cpp for any audio that needs re-processing at higher quality.
6. Full inotifywait pipeline watches all project `pics/` and `docs/` folders, auto-commits and pushes to GitHub.
7. WiFi survey data exported as CSV, automatically parsed into markdown tables by a script.

---

## 11. Recommended Starting Point for Precept Systems

Given the South African context (expensive mobile data, unreliable connectivity at client sites, solo operator, existing git/GitHub workflow), I recommend starting with **Tier 1 plus two elements from Tier 2**:

### Immediate Setup (Today)

1. **Tailscale** on phone and desktop. This is the single highest-value addition. Being able to SSH into the desktop from a client site to look up credentials, network diagrams, or previous visit notes is transformative. Install Termius on the phone as the SSH client.

2. **Syncthing** between phone and desktop with a dedicated `field-capture/` folder, WiFi-only. This gets photos and files from the phone to the desktop without touching cloud services or mobile data.

3. **Markor** on the phone for on-site markdown notes. Point it at the Syncthing folder so notes auto-sync.

### Next Week

4. **A simple desktop script** that processes the `field-capture/` folder: prompts for which project the files belong to, moves them to the right `pics/` or `docs/` directory, renames with date prefix, and commits to git. This replaces the current manual process that produces the naming chaos visible in the jenkins-network project.

5. **Whisper API integration** for voice memos. At R1-2 per site visit, the cost is negligible and the time saved is significant.

### Next Month

6. **FolderSync Pro** if the single-folder Syncthing approach proves too coarse. Being able to set up per-project folder pairs via SFTP is more precise.

7. **gitwatch** on the desktop for auto-committing incoming files to the right repos.

---

## 12. Key Considerations for South Africa

| Factor | Implication | Mitigation |
|--------|------------|------------|
| Expensive mobile data (R100-150/GB) | Never sync over cellular | Syncthing WiFi-only; FolderSync restrict to home SSID |
| Load shedding | Desktop may be off when you return | UPS for desktop; or use a Raspberry Pi (low power) as always-on sync target |
| Rural/residential poor connectivity | May have no internet at client site | Capture everything locally; sync later at home or in the car on WiFi |
| HEIC photo format (iPhone clients) | HEIC files in project folders | Desktop-side conversion script (heif-convert) as part of ingestion pipeline |
| WhatsApp as primary communication | Photos arrive via WhatsApp with terrible naming | Download to field-capture folder, rename during ingestion |

---

## Sources

- [Field Service Management Trends 2026 - Fieldwork](https://fieldworkhq.com/2025/12/26/field-service-management-trends-in-2026/)
- [Global FSM Trends 2026 - Brocoders](https://brocoders.com/blog/global-field-service-management-trends-2026/)
- [Git Mobile Apps - Livable Software](https://livablesoftware.com/mobile-apps-git-github-android-iphone/)
- [GitHub Mobile](https://github.com/mobile)
- [Working Copy - Git on iOS](https://workingcopy.app/)
- [Termux Git Guide 2025](https://hub.egwimcodes.dev/2025/05/06/install-git-in-termux-on-android-2025-beginners-guide/)
- [Termux for SSH Git Commits](https://dev.to/terminaltools/how-to-use-termux-for-on-the-go-ssh-git-commits-1h4h)
- [Syncthing Community Forum - Photo Sync](https://forum.syncthing.net/t/seeking-the-recommended-way-to-use-syncthing-for-photos-sync/15049)
- [Syncthing Folder Types Documentation](https://docs.syncthing.net/users/foldertypes.html)
- [FolderSync SFTP Documentation](https://foldersync.io/docs/faq/sftp/)
- [FolderSync - Baheyeldin Dynasty](https://baheyeldin.com/android/foldersync-android-app-can-sync-your-photos-over-sftp.html)
- [KDE Connect](https://kdeconnect.kde.org/)
- [OpenAI Whisper - GitHub](https://github.com/openai/whisper)
- [Whisper API Pricing 2026](https://brasstranscripts.com/blog/openai-whisper-api-pricing-2025-self-hosted-vs-managed)
- [OpenAI Transcription Pricing Feb 2026](https://costgoat.com/pricing/openai-transcription)
- [NotelyVoice - On-Device Whisper](https://github.com/tosinonikute/NotelyVoice)
- [Whisper Notes App](https://whispernotes.app/)
- [WiFiAnalyzer - GitHub](https://github.com/VREMSoftwareDevelopment/WiFiAnalyzer)
- [WiFi Heatmap - Google Play](https://play.google.com/store/apps/details?id=ua.com.wifisolutions.wifiheatmap)
- [NetSpot for Android](https://www.netspotapp.com/netspot-wifi-analyzer-for-android.html)
- [Offline-First Sync Patterns](https://developersvoice.com/blog/mobile/offline-first-sync-patterns/)
- [Offline Sync Architecture - Alpha Software](https://www.alphasoftware.com/blog/offline-sync-architecture-tutorial-examples-tools-for-field-operations)
- [Tailscale SSH Documentation](https://tailscale.com/kb/1193/tailscale-ssh)
- [Tailscale Free Plans](https://tailscale.com/kb/1154/free-plans-discounts)
- [Tailscale Pricing](https://tailscale.com/pricing)
- [Termius SSH Client](https://termius.com/index.html)
- [JuiceSSH Removed from Play Store](https://owrbit.com/hub/juicessh-removed-from-play-store-5-best-ssh-clients/)
- [Markor - GitHub](https://github.com/gsantner/markor)
- [Obsidian Git Plugin](https://github.com/Vinzent03/obsidian-git)
- [Obsidian Sync with GitHub](https://medium.com/@proflead/sync-obsidian-notes-across-devices-for-free-using-github-mobile-pc-40db42eb91d0)
- [Open Source FSM Software](https://buildops.com/resources/field-service-management-open-source/)
- [OCA Field Service - GitHub](https://github.com/OCA/field-service)
- [Gitwatch - GitHub](https://github.com/gitwatch/gitwatch)
- [Tasker - Google Play](https://play.google.com/store/apps/details?id=net.dinglisch.android.taskerm)
- [Telegram Bot Image Save - GitHub](https://github.com/Mrjavaci/telegram-image-save)
- [Rsync with Termux](https://howtos.davidsebek.com/android-rsync-termux.html)
- [git-annex for Managing Photos](https://switowski.com/blog/git-annex/)
