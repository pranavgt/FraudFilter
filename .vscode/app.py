from flask import Flask, render_template, request
from PIL import Image, UnidentifiedImageError
import pytesseract, io

import sqlite3, os, datetime
DB_PATH = os.path.join(os.path.dirname(__file__), "fraudfilter.db")

# ✅ Safer: only set tesseract path on Windows if present
if os.name == "nt":
    win_path = r"C:\Users\prana\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
    if os.path.exists(win_path):
        pytesseract.pytesseract.tesseract_cmd = win_path

app = Flask(__name__)

def init_db():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS checks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            source      TEXT,
            verdict     TEXT NOT NULL,
            message     TEXT NOT NULL
        )
    """)
    con.commit(); con.close()

def save_check(message: str, verdict: str, source: str):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO checks (created_at, source, verdict, message) VALUES (?, ?, ?, ?)",
        (datetime.datetime.utcnow().isoformat(timespec="seconds"), source, verdict, message)
    )
    con.commit(); con.close()

def get_recent_checks(limit: int = 20):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    # ✅ Guard limit to avoid SQL injection-by-parameter misuse on some drivers
    limit = max(1, min(int(limit), 100))
    cur.execute("SELECT created_at, source, verdict, message FROM checks ORDER BY id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    con.close()
    return rows

URGENT_WORDS = [
    "urgent", "act now", "final notice", "crypto",
    "wire transfer", "gift card", "warrant", "lawsuit", "arrest",
    "verify your account", "confirm your password"
]

def is_scam(msg: str) -> bool:
    msg_low = msg.lower()
    return any(w in msg_low for w in URGENT_WORDS)

def ocr_image(file_storage) -> str:
    """Convert an uploaded image to text with OCR."""
    img_bytes = file_storage.read()
    img = Image.open(io.BytesIO(img_bytes))
    # ✅ Convert to RGB to avoid mode issues
    img = img.convert("RGB")
    text = pytesseract.image_to_string(img)
    return (text or "").strip()

@app.route("/", methods=["GET", "POST"])
def index():
    verdict = None          # message for the user
    msg = ""                # final text we will evaluate
    extracted = ""          # OCR text (for display)
    source = None

    if request.method == "POST":
        # 1) Text from textarea (optional)
        typed = (request.form.get("message") or "").strip()

        # 2) Image from file input (optional) -> OCR
        file = request.files.get("image")
        had_image = bool(file and file.filename)

        if had_image:
            try:
                extracted = ocr_image(file)
            except UnidentifiedImageError:
                extracted = "(OCR failed: not a valid image file)"
            except Exception as e:
                extracted = f"(OCR failed: {e})"

        # Combine typed + extracted
        parts = [p for p in [typed, extracted] if p]
        msg = "\n\n".join(parts)

        # 3) Evaluate and SAVE to DB
        if msg:
            verdict = "⚠️ Scam detected!" if is_scam(msg) else "✅ Looks safe."
            had_text = bool(typed)
            source = "both" if (had_text and had_image) else ("image" if had_image else "text")
            save_check(msg, verdict, source)
        else:
            verdict = "No text found. Paste text or upload a clearer image."
            source = "none"

    # ✅ ALWAYS return a template
    return render_template("index.html", verdict=verdict, extracted=extracted, message=msg, source=source)

@app.route("/history")
def history():
    rows = get_recent_checks(20)
    return render_template("history.html", rows=rows)

if __name__ == "__main__":
    print("DB at:", DB_PATH)
    init_db()
    # ✅ Keep debug for dev only; in production use a real WSGI server
    app.run(debug=True)
