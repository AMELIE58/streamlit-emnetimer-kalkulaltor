import streamlit as st

st.markdown("""
<style>
img { border-radius: 0 !important; }
</style>
""", unsafe_allow_html=True)

st.image("img/NIH NO CMYK.jpg", width=180)
st.title("Beregning av timer per emne")
st.markdown(
    "Beregner arbeidstidsressurs per emne etter **Normer for "
    "studentrettet aktivitet** (kap. 2). Juster verdiene nedenfor."
)
st.divider()

# --- Felles konstanter fra normen ---
BASESATS = {"Bachelor": 25, "Master": 15}   # timer per studiepoeng
NORMTALL = {"Bachelor": 35, "Master": 25}   # normert studentgruppe (campus-emner)
NORMTALL_DIGITALT = 60                      # normert studentgruppe, digitale emner
SENSOR_GRENSE_SP = 15                       # fra hvilket sp-nivå sensortillegget gjelder
SENSOR_TILLEGG_PER_STUDENT = 0.5            # timer per student, alle studenter, uavhengig av f og normtall

SP_VALG = [2.5, 5, 7.5, 10, 15, 20, 30]

# Undervisningsform: hver form definerer f_grunn (påvirker 25% av grunnressursen),
# f_student (påvirker studentjusteringen), og ev. eget normtall (kun digitalt avviker).
UNDERVISNINGSFORMER = {
    "Teoretisk":            {"f_grunn": 1.0, "f_student": 1.0, "normtall": None},
    "Teoretisk/praktisk":   {"f_grunn": 1.5, "f_student": 1.5, "normtall": None},
    "Praktisk":             {"f_grunn": 2.0, "f_student": 2.0, "normtall": None},
    "Digitalt (nettemne)":  {"f_grunn": 1.0, "f_student": 0.5, "normtall": NORMTALL_DIGITALT},
}


def sats_per_student(sp: float) -> float:
    """Tillegg/fratrekk-sats (t/student) etter skalaen i punkt 2.1."""
    if sp < 5:
        return 0.75
    elif sp < 10:
        return 1.0
    else:
        return 1.25


def sensortillegg(sp: float, antall_studenter: int) -> float:
    """Fast tillegg for emner med krav om to sensorer (fotnote til 2.1).
    Gjelder alle studenter, uavhengig av normtall og undervisningsform."""
    if sp >= SENSOR_GRENSE_SP:
        return SENSOR_TILLEGG_PER_STUDENT * antall_studenter
    return 0.0


def beregn_total(sp, basesats, normtall, f_grunn, f_student, antall_studenter, sensor=True):
    grunnressurs = sp * basesats
    grunnressurs_justert = grunnressurs * (0.75 + 0.25 * f_grunn)
    studentjustering = (antall_studenter - normtall) * sats_per_student(sp) * f_student
    sensor_t = sensortillegg(sp, antall_studenter) if sensor else 0.0
    total = grunnressurs_justert + studentjustering + sensor_t
    return total, grunnressurs_justert, studentjustering, sensor_t


def vis_resultat(total, grunnressurs_justert, studentjustering, sensor_t, ekstra_rader=None):
    st.subheader("Resultat")
    st.metric("Totalt antall timer", f"{total:.1f} timer")
    with st.expander("Vis beregning"):
        rows = f"""
| Komponent | Timer |
|---|---|
| Justert grunnressurs | {grunnressurs_justert:.1f} |
| Studentjustering (tillegg/fratrekk) | {studentjustering:+.1f} |
| Sensortillegg (≥15 sp, alle studenter) | {sensor_t:+.1f} |
| **Total** | **{total:.1f}** |
"""
        st.markdown(rows)
        if ekstra_rader:
            st.markdown(ekstra_rader)


# --- Steg 1: Nivå ---
nivaa = st.radio("Velg nivå", ["Bachelor", "Master"], horizontal=True)
basesats = BASESATS[nivaa]
st.divider()

# --- Steg 2: Studiepoeng ---
studiepoeng = st.selectbox(
    "Studiepoeng (SP)", options=SP_VALG, index=SP_VALG.index(10),
    format_func=lambda x: f"{x} SP"
)
st.divider()

# --- Steg 3: Undervisningsform (inkl. digitalt) ---
form_label = st.selectbox("Undervisningsform", options=list(UNDERVISNINGSFORMER.keys()))
form = UNDERVISNINGSFORMER[form_label]
f_grunn = form["f_grunn"]
f_student = form["f_student"]
normtall = form["normtall"] if form["normtall"] is not None else NORMTALL[nivaa]
st.divider()

# --- Steg 4: Antall studenter ---
antall_studenter = st.number_input(
    "Antall studenter", min_value=1, max_value=1000, value=normtall, step=1
)
st.caption(
    f"Grunnressurs: **{basesats} t/sp** · Normtall: **{normtall} studenter** · "
    f"Sats per student (k): **{sats_per_student(studiepoeng)}**"
)
st.divider()

# --- Beregning ---
total, gb, sj, sensor_t = beregn_total(
    studiepoeng, basesats, normtall, f_grunn, f_student, antall_studenter
)
vis_resultat(
    total, gb, sj, sensor_t,
    ekstra_rader=f"""
| Variabel | Verdi |
|---|---|
| Nivå | {nivaa} |
| Undervisningsform | {form_label} |
| Studiepoeng (SP) | {studiepoeng} |
| Faktor grunnressurs | {f_grunn} |
| Faktor studentjustering | {f_student} |
| Sats per student (k) | {sats_per_student(studiepoeng)} |
| Normtall | {normtall} |
| Antall studenter | {antall_studenter} |
""",
)

st.divider()
with st.expander("Mer informasjon om normer for studentrettet aktivitet "):
    st.markdown(
        "Ressursen skal dekke emneansvar, forberedelse og gjennomføring av "
        "undervisning, veiledning og studentkontakt, sensur- og "
        "vurderingsarbeid, administrasjon og koordinering, samt faglig "
        "oppdatering.\n\n"
        "- **Grunnressurs**: emnets studiepoeng multiplisert med en fast sats "
        "(25 t/sp for bachelor, 15 t/sp for master).\n"
        "- **Undervisningsform**: justerer 25 % av grunnressursen og hele "
        "studentjusteringen, bortsett fra digitale emner, som beregnes med "
        "egne satser og et eget normtall (60 studenter).\n"
        "- **Studentjustering**: tillegg eller fratrekk dersom antall "
        "studenter avviker fra normtallet for emnet.\n"
        "- **Sensortillegg**: et fast tillegg på 0,5 timer per student for "
        "emner på 15 studiepoeng eller mer, som følge av krav om to "
        "sensorer. Gjelder alle studenter i emnet, uavhengig av normtall og "
        "undervisningsform.\n\n"
        "Se normdokumentet (**Normer for studentrettet aktivitet**, kap. 2) "
        "for fullstendig regelverk og særskilte ordninger (bl.a. "
        "veiledningsemner, friluftslivsundervisning og praksisemner)."
    )