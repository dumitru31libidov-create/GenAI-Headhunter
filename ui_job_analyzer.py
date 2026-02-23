import streamlit as st
import os
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================
# INITIALIZARE SESSION STATE
# ============================

if "processing_times" not in st.session_state:
    st.session_state.processing_times = []

if "logs" not in st.session_state:
    st.session_state.logs = []

if "last_timeline" not in st.session_state:
    st.session_state.last_timeline = []

if "request_count" not in st.session_state:
    st.session_state.request_count = 0

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# --- LOGICĂ SIMPLĂ ---
from job_analyzer import (
    scrape_clean_job_text,
    analyze_job_with_ai,
    JobAnalysis,
)

# --- MULTI-AGENT ---
from agents.extractor import run_extractor
from agents.validator import run_validator
from agents.counselor import run_counselor

# ======================================================================
# UI
# ======================================================================

st.title("🕵️ GenAI Headhunter — AI Job Intelligence Suite")

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🔹 Analiză Simplă (JobAnalysis)",
        "🔷 Multi-Agent System",
        "🟩 Compară Joburi",
        "🟦 Monitoring & Logs",
    ]
)

# ======================================================================
# TAB 1 — AGENT SIMPLU
# ======================================================================

with tab1:
    st.subheader("Analiză Simplă a unui Job Description")

    url_simple = st.text_input("Introdu URL job (Simplu):")

    if st.button("Analizează (Simplu)"):
        # resetăm timeline-ul pentru această analiză
        st.session_state.last_timeline = []

        with st.spinner("Scraping..."):
            start = time.time()
            text = scrape_clean_job_text(url_simple)
            duration = time.time() - start

            st.session_state.processing_times.append(duration)
            st.session_state.logs.append(
                f"Scraping (Simplu) finalizat în {duration:.2f} sec"
            )
            st.session_state.last_timeline.append(
                {"name": "Scraping (Simplu)", "duration": duration}
            )

        with st.spinner("AI Analysis..."):
            start = time.time()
            result: JobAnalysis = analyze_job_with_ai(text)
            duration = time.time() - start

            st.session_state.processing_times.append(duration)
            st.session_state.logs.append(
                f"JobAnalysis finalizat în {duration:.2f} sec"
            )
            st.session_state.last_timeline.append(
                {"name": "JobAnalysis", "duration": duration}
            )

        st.session_state.request_count += 1

        st.subheader("📌 Rezultat JobAnalysis")
        st.json(result.model_dump(), expanded=True)

# ======================================================================
# TAB 2 — MULTI-AGENT SYSTEM
# ======================================================================

with tab2:
    st.subheader("Analiză Multi-Agent")

    url_multi = st.text_input("Introdu URL job (Multi-Agent):")

    if st.button("Analizează (Multi-Agent)"):
        # resetăm timeline-ul pentru această analiză
        st.session_state.last_timeline = []

        # --- SCRAPING ---
        with st.spinner("Scraping..."):
            start = time.time()
            text = scrape_clean_job_text(url_multi)
            duration = time.time() - start

            st.session_state.processing_times.append(duration)
            st.session_state.logs.append(
                f"Scraping (Multi-Agent) finalizat în {duration:.2f} sec"
            )
            st.session_state.last_timeline.append(
                {"name": "Scraping (Multi-Agent)", "duration": duration}
            )

        # --- EXTRACTOR ---
        with st.spinner("Extractor..."):
            start = time.time()
            raw = run_extractor(text)
            duration = time.time() - start

            st.session_state.processing_times.append(duration)
            st.session_state.logs.append(
                f"Extractor finalizat în {duration:.2f} sec"
            )
            st.session_state.last_timeline.append(
                {"name": "Extractor", "duration": duration}
            )

        # --- VALIDATOR ---
        with st.spinner("Validator..."):
            start = time.time()
            validation = run_validator(text, raw)
            duration = time.time() - start

            st.session_state.processing_times.append(duration)
            st.session_state.logs.append(
                f"Validator finalizat în {duration:.2f} sec"
            )
            st.session_state.last_timeline.append(
                {"name": "Validator", "duration": duration}
            )

        # --- COUNSELOR ---
        with st.spinner("Counselor..."):
            start = time.time()
            advice = run_counselor(raw)
            duration = time.time() - start

            st.session_state.processing_times.append(duration)
            st.session_state.logs.append(
                f"Counselor finalizat în {duration:.2f} sec"
            )
            st.session_state.last_timeline.append(
                {"name": "Counselor", "duration": duration}
            )

        st.session_state.request_count += 1

        st.subheader("📌 Raw Extraction")
        st.json(raw.model_dump(), expanded=True)

        st.subheader("🔍 Validator")
        if validation.is_consistent:
            st.success("Extractorul este consistent cu textul.")
        else:
            st.error("Probleme detectate:")
            st.write(validation.issues)

        st.subheader("🎯 Strategic Advice")
        st.json(advice.model_dump(), expanded=True)

# ======================================================================
# TAB 3 — COMPARĂ JOBURI
# ======================================================================

with tab3:
    st.subheader("🟩 Compară mai multe joburi (Agent Simplu)")

    urls_text = st.text_area("Introdu URL-urile (unul pe linie):", height=150)

    if st.button("Compară Joburi"):
        urls = [u.strip() for u in urls_text.split("\n") if u.strip()]

        if not urls:
            st.warning("Te rugăm introdu cel puțin un URL.")
        else:
            results = []
            progress = st.progress(0)
            status = st.empty()

            for i, url in enumerate(urls):
                status.text(f"Analizez jobul {i+1}/{len(urls)}...")

                text = scrape_clean_job_text(url)

                if "Error" not in text:
                    try:
                        analysis: JobAnalysis = analyze_job_with_ai(text)
                        results.append(
                            {
                                "URL": url,
                                "Role": analysis.role_title,
                                "Company": analysis.company_name,
                                "Seniority": analysis.seniority,
                                "Score": analysis.match_score,
                                "Remote": "Da" if analysis.is_remote else "Nu",
                                "Tech Count": len(analysis.tech_stack),
                                "Tech Stack": analysis.tech_stack,
                            }
                        )
                    except Exception as e:
                        st.error(f"Eroare la jobul {url}: {str(e)}")

                progress.progress((i + 1) / len(urls))

            status.text("Gata!")

            if results:
                df = pd.DataFrame(results)

                st.subheader("📊 Rezultate Comparate")
                st.dataframe(df)

                # 1. EXPORT CSV
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="⬇️ Descarcă CSV",
                    data=csv,
                    file_name="comparatie_joburi.csv",
                    mime="text/csv",
                )

                # 2. RANKING AUTOMAT
                st.subheader("🏆 Ranking după Score")
                df_ranked = df.sort_values(by="Score", ascending=False)
                st.dataframe(df_ranked)

                # 3. SCOR DE SIMILARITATE (Tech Stack)
                st.subheader("🔗 Similaritate între joburi (Tech Stack)")

                def jaccard(a, b):
                    set_a = set(a)
                    set_b = set(b)
                    return (
                        len(set_a & set_b) / len(set_a | set_b)
                        if len(set_a | set_b) > 0
                        else 0
                    )

                similarity_matrix = []
                for i in range(len(results)):
                    row = []
                    for j in range(len(results)):
                        row.append(
                            jaccard(
                                results[i]["Tech Stack"],
                                results[j]["Tech Stack"],
                            )
                        )
                    similarity_matrix.append(row)

                sim_df = pd.DataFrame(
                    similarity_matrix,
                    columns=df["Role"],
                    index=df["Role"],
                )
                st.dataframe(sim_df.style.background_gradient(cmap="Blues"))

                # 4. GRAFIC RADAR (Tech Stack)
                st.subheader("📡 Radar Chart — Tech Stack Overlap")

                all_techs = sorted(
                    list({tech for r in results for tech in r["Tech Stack"]})
                )

                fig = go.Figure()
                for r in results:
                    values = [
                        1 if tech in r["Tech Stack"] else 0 for tech in all_techs
                    ]
                    fig.add_trace(
                        go.Scatterpolar(
                            r=values,
                            theta=all_techs,
                            fill="toself",
                            name=r["Role"],
                        )
                    )

                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True)),
                    showlegend=True,
                )

                st.plotly_chart(fig, use_container_width=True)

# ======================================================================
# TAB 4 — DASHBOARD PREMIUM
# ======================================================================

with tab4:
    st.title("📊 Dashboard Premium — Monitoring & Analytics")

    # 1. KPI CARDS
    st.subheader("📌 KPI Overview")

    col1, col2, col3 = st.columns(3)

    # Uptime
    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()
    uptime = time.time() - st.session_state.start_time
    col1.metric("⏱️ Uptime", f"{uptime:.0f} sec")

    # Request count
    if "request_count" not in st.session_state:
        st.session_state.request_count = 0
    col2.metric("📨 Request-uri procesate", st.session_state.request_count)

    # Average processing time
    if "processing_times" not in st.session_state:
        st.session_state.processing_times = []

    avg_time = (
        sum(st.session_state.processing_times)
        / len(st.session_state.processing_times)
        if st.session_state.processing_times
        else 0
    )
    col3.metric("⚡ Timp mediu procesare", f"{avg_time:.2f} sec")

    st.markdown("---")

    # 2. TIMELINE PIPELINE
    st.subheader("🕒 Pipeline Timeline (ultimul job)")

    if st.session_state.last_timeline:
        timeline = st.session_state.last_timeline

        fig_timeline = go.Figure()
        for step in timeline:
            fig_timeline.add_trace(
                go.Bar(
                    x=[step["duration"]],
                    y=[step["name"]],
                    orientation="h",
                    text=f"{step['duration']:.2f} sec",
                    textposition="auto",
                )
            )

        fig_timeline.update_layout(
            height=300,
            title="Durata fiecărui pas din pipeline",
            xaxis_title="Secunde",
        )

        st.plotly_chart(fig_timeline, use_container_width=True)
    else:
        st.info("Niciun job procesat încă.")

    st.markdown("---")

    # 3. LOGGING
    st.subheader("📜 Logs în timp real")

    if "logs" not in st.session_state:
        st.session_state.logs = []

    for log in st.session_state.logs[-15:]:
        st.text(log)

    st.markdown("---")

    # 4. HEALTH MONITOR
    st.subheader("🩺 Health Monitor")

    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        st.success("🔑 API Key loaded")
    else:
        st.error("❌ API Key missing")

    st.info("Groq API Status: OK (ping simulated)")

    st.markdown("---")

    # 5. DEBUG MODE
    debug = st.checkbox("🔍 Debug Mode")

    if debug:
        st.warning("Debug Mode activat — afișăm date brute.")

        if "last_raw_prompt" in st.session_state:
            st.subheader("📤 Prompt trimis")
            st.code(st.session_state.last_raw_prompt, language="json")

        if "last_raw_response" in st.session_state:
            st.subheader("📥 Răspuns brut")
            st.code(st.session_state.last_raw_response, language="json")