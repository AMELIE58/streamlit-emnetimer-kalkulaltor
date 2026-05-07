import streamlit as st

st.markdown("""
<style>
img { border-radius: 0 !important; }
</style>
""", unsafe_allow_html=True)

st.image("NIH NO CMYK.jpg", width=180)
st.title("Beregning av timer per emne")
st.markdown("Juster verdiene nedenfor for å beregne antall timer.")

st.divider()

# --- Bachelor / Master ---
grad = st.radio("Velg grad", ["Bachelor", "Master"], horizontal=True)

st.divider()

if grad == "Bachelor":

    # --- Studiepoeng og k ---
    sp_options = {5: 1.0, 10: 1.5, 15: 2.0, 20: 2.5}
    studiepoeng = st.selectbox(
        "Studiepoeng (SP)",
        options=list(sp_options.keys()),
        format_func=lambda x: f"{x} SP"
    )
    k = sp_options[studiepoeng]
    st.caption(f"Sats per student (k): **{k}**")

    st.divider()

    # --- Egenartsfaktor f ---
    f_options = {
        "1,0 – Teoretisk": 1.0,
        "1,5 – Teoretisk/praktisk": 1.5,
        "2,0 – Praktisk": 2.0,
    }
    f_label = st.selectbox("Egenartsfaktor (f)", options=list(f_options.keys()))
    f = f_options[f_label]

    st.divider()

    # --- Antall studenter ---
    antall_studenter = st.number_input(
        "Antall studenter",
        min_value=1,
        max_value=1000,
        value=35,
        step=1
    )

    st.divider()

    # --- Beregning ---
    total_timer = (studiepoeng * 25 * (0.75 + 0.25 * f)) + ((antall_studenter - 35) * k * f)

    st.subheader("Resultat")
    st.metric("Totalt antall timer", f"{total_timer:.1f} timer")

    with st.expander("Vis formel"):
        st.latex(
            r"\text{Total timer} = (\text{SP} \times 25 \times (0{,}75 + 0{,}25 \times f))"
            r" + ((\text{Studenter} - 35) \times k \times f)"
        )
        st.markdown(f"""
    | Variable | Verdi |
    |----------|-------|
    | Studiepoeng (SP) | {studiepoeng} |
    | Egenartsfaktor (f) | {f} |
    | Sats per student (k) | {k} |
    | Antall studenter | {antall_studenter} |
    """)

else:  # Master
    # --- Studiepoeng og k ---
    sp_options = {5: 1.0, 10: 1.5, 15: 2.0, 20: 2.5}
    studiepoeng = st.selectbox(
        "Studiepoeng (SP)",
        options=list(sp_options.keys()),
        format_func=lambda x: f"{x} SP"
    )
    k = sp_options[studiepoeng]
    st.caption(f"Sats per student (k): **{k}**")

    st.divider()

    # --- Egenartsfaktor f ---
    f_options = {
        "1,0 – Teoretisk": 1.0,
        "1,5 – Teoretisk/praktisk": 1.5,
        "2,0 – Praktisk": 2.0,
    }
    f_label = st.selectbox("Egenartsfaktor (f)", options=list(f_options.keys()))
    f = f_options[f_label]

    st.divider()

    # --- Antall studenter ---
    antall_studenter = st.number_input(
        "Antall studenter",
        min_value=1,
        max_value=1000,
        value=35,
        step=1
    )

    st.divider()

    # --- Beregning ---
    total_timer = (studiepoeng * 25 * (0.75 + 0.25 * f)) + ((antall_studenter - 35) * k * f)

    st.subheader("Resultat")
    st.metric("Totalt antall timer", f"{total_timer:.1f} timer")

    with st.expander("Vis formel"):
        st.latex(
            r"\text{Total timer} = (\text{SP} \times 25 \times (0{,}75 + 0{,}25 \times f))"
            r" + ((\text{Studenter} - 35) \times k \times f)"
        )
        st.markdown(f"""
    | Variable | Verdi |
    |----------|-------|
    | Studiepoeng (SP) | {studiepoeng} |
    | Egenartsfaktor (f) | {f} |
    | Sats per student (k) | {k} |
    | Antall studenter | {antall_studenter} |
    """)
