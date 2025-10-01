import streamlit as st, requests, json, os
from pathlib import Path
from dotenv import load_dotenv; load_dotenv()

API = os.getenv("API_URL", st.secrets.get("API_URL", "http://localhost:8000"))

LANG = st.session_state.get("lang", "en")
def _t(key, **kwargs):
    path = Path(__file__).parent / "i18n" / f"{LANG}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    val = data.get(key, key)
    for k,v in kwargs.items():
        val = val.replace("{"+k+"}", str(v))
    return val

st.set_page_config(page_title="YouTube Transcriber", page_icon="🎧", layout="centered")

# Language toggle
colL, colR = st.columns([1,1])
with colL:
    st.title("🎧 YouTube Transcriber")
with colR:
    lang = st.selectbox("Language", ["en","pt"], index=0 if LANG=="en" else 1)
    st.session_state["lang"] = lang
    LANG = lang

def t(k, **kw): return _t(k, **kw)

yt = st.text_input("YouTube URL", placeholder=t("url_placeholder"))
col1, col2 = st.columns(2)
target = col1.selectbox(t("output_language"), [t("original"), t("ptbr"), t("english")])
maxmin = col2.number_input(t("max_duration"), 1, 60, 60)
store = st.checkbox(t("store_sqlite"), value=False)
prefer_captions = st.checkbox(t("prefer_captions"), value=True)
export = st.multiselect(t("export_formats"), ["txt","srt","vtt"], default=["txt"])

if st.button(t("transcribe")):
    body = {
        "youtube_url": yt,
        "target_lang": "original" if target==t("original") else ("pt-BR" if target==t("ptbr") else "en"),
        "max_minutes": int(maxmin),
        "store": bool(store),
        "prefer_captions": bool(prefer_captions),
        "export_format": export or ["txt"]
    }
    with st.spinner(t("processing")):
        try:
            r = requests.post(f"{API}/transcribe", json=body, timeout=3600)
        except Exception as e:
            st.error(f"Request failed: {e}")
            r = None
    if r and r.ok:
        data = r.json()
        st.success(t("done"))
        st.caption(t("detected_title", lang=data.get("detected_lang",""), title=data.get("title","")))
        st.text_area(t("preview"), value=(data.get("text_joined","")[:5000]), height=260)
        st.download_button(t("download_txt"), data=data.get("text_joined","").encode("utf-8"),
                           file_name="transcript.txt", mime="text/plain")
        if "export" in data:
            if "srt" in data["export"]:
                st.download_button("Download .srt", data=data["export"]["srt"].encode("utf-8"),
                                   file_name="transcript.srt")
            if "vtt" in data["export"]:
                st.download_button("Download .vtt", data=data["export"]["vtt"].encode("utf-8"),
                                   file_name="transcript.vtt")
        if "transcript_id" in data:
            st.info(t("saved_with_id", id=data["transcript_id"]))
    elif r is not None:
        try:
            er = r.json()
        except Exception:
            er = {"error": {"code": "UNKNOWN", "message": r.text}}
        st.error(f"{er.get('error',{}).get('code')}: {er.get('error',{}).get('message')}")

if st.button(t("reset")):
    try: requests.post(f"{API}/reset", timeout=10)
    except: pass
    # compat: Streamlit < 1.31
    try: st.rerun()
    except: st.experimental_rerun()
