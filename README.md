# Multi-Persona AI Assistant Suite with Privacy-Preserving Feedback

A professional, responsive Flask-based web application providing specialized AI interaction across multiple domain roles using the Google GenAI SDK and native SQLite tracking. The application features an unfolding UI design paradigm, multi-document multimodal support, and an isolated administrative analytics workspace for development debugging.

## 🚀 Key Features

*   **Dynamic Multi-Persona Engineering:** Hot-swappable client-side roles (Python Coding Coach, Technical Support Specialist, and Local Tour Guide) driving dedicated system instructions and prompt constraints.
*   **Decoupled Context Memory:** Leverages custom relational database filters ensuring chat transcripts remain isolated per persona profile without overlapping logs.
*   **Unfolding UI/UX Interface:** Built with a minimal footprint layout centered on the laptop display viewport that animates into full rendering space only upon the initialization of the primary user message thread.
*   **Privacy-Preserving User Feedback Loop:** An embedded evaluation utility panel passing upvotes/downvotes along with optional textual notes.
*   **Developer Analytics Dashboard:** A dedicated administrative sub-route displaying user input-response text pairs side-by-side with feedback reviews to expedite systemic alignment analysis.

---

## 🏗️ Technical Architecture & Core Concepts

This application utilizes foundational software engineering practices to achieve safe runtime isolation and data persistence:

1. **Database Schema Migrations:** The initialization controller dynamically probes the localized database engine using metadata queries, appending schema structural modifications (`ALTER TABLE`) automatically at startup to protect legacy test data configurations.
2. **Relational Context Mapping:** Chat histories are partitioned inside a unified message ledger using structural column filtering tags (`WHERE persona = ?`) to bypass overhead multi-table setups.
3. **Session Context Caching:** Employs precise string variable buffering on the frontend client to extract *only* the immediate response message loop pairs for administrative review, safeguarding overall participant data anonymity.

---

## 🛠️ Project Workspace Installation

### Prerequisites
* Python 3.10 or higher
* Google GenAI API key configured within your environment workspace variables

### Setup Instuctions

1. **Clone the repository track to your machine:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
   cd YOUR_REPO_NAME
