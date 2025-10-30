import streamlit as st
import pandas as pd
import os
from main import generate_leads, stop_scraping, reset_stop_flag

# --- PAGE CONFIG ---
st.set_page_config(page_title="Smart Maps Scraper 🧠", layout="centered", page_icon="🗺️")

st.title("🧠 Smart Google Maps Scraper")
st.caption("Extract business **Name, Website, Email, and Phone** directly from Google Maps in seconds!")

# --- SIDEBAR SETTINGS ---
with st.sidebar:
    st.header("⚙️ Settings")
    city = st.text_input("🏙️ City", "Lucknow")
    business = st.text_input("🏢 Business / Keyword", "marketing agencies")
    max_items = st.slider("🔢 Number of Businesses", 10, 500, 50, step=10)
    st.info("💡 Tip: Use specific business keywords for best results.")

st.markdown("---")

# --- UI Placeholders ---
progress_placeholder = st.empty()
progress_bar = st.progress(0)
output_placeholder = st.empty()
stop_button_placeholder = st.empty()
progress_state = {"value": 0}

# --- PROGRESS CALLBACK ---
def progress_callback(message):
    progress_placeholder.text(message)
    if "Saved" in message:
        progress_bar.progress(100)
    else:
        progress_state["value"] = min(progress_state["value"] + 5, 95)
        progress_bar.progress(progress_state["value"])

# --- START SCRAPING BUTTON ---
start_clicked = st.button("🚀 Start Scraping", use_container_width=True)

if start_clicked:
    reset_stop_flag()
    progress_bar.progress(0)
    progress_state["value"] = 0
    progress_placeholder.text("🕒 Initializing browser and preparing to scrape...")

    stop_btn = stop_button_placeholder.button("🛑 Stop Scraping", use_container_width=True)

    try:
        if stop_btn:
            stop_scraping()
            st.warning("⏹ Stopped manually.")
        else:
            out_path, total = generate_leads(city, business, progress_callback, max_items=max_items)

            if os.path.exists(out_path):
                df = pd.read_csv(out_path)
                st.success(f"✅ Completed! {total} businesses extracted successfully.")
                st.dataframe(df, use_container_width=True)

                with open(out_path, "rb") as f:
                    st.download_button(
                        label="📥 Download CSV",
                        data=f,
                        file_name=os.path.basename(out_path),
                        mime="text/csv",
                        use_container_width=True
                    )
            else:
                st.error("❌ No CSV file was generated.")

    except Exception as e:
        st.error(f"⚠️ Error occurred: {e}")

    finally:
        progress_bar.progress(100)
        progress_placeholder.text("✅ Scraping Finished.")

else:
    st.info("👆 Click 'Start Scraping' to begin extracting data.")

st.markdown("---")
st.markdown("<small>Developed by <b>Harsh Shukla</b> • Smart Maps Scraper © 2025</small>", unsafe_allow_html=True)
