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

# =====================================================================
# VERDIER FRA NORMEN - endres her
# =====================================================================
BASESATS = {"Bachelor": 25, "Master": 20}   # timer per studiepoeng (campus-emner)
NORMTALL = {"Bachelor": 35, "Master": 25}   # normert studentgruppe (campus-emner)
BASESATS_DIGITALT = 15                      # timer per studiepoeng, digitale emner (ikke normtall)
SENSOR_GRENSE_SP = 15                       # fra hvilket sp-nivaa sensortillegget gjelder
SENSOR_TILLEGG_PER_STUDENT = 0.5            # timer per student, alle studenter

# Friluftsliv med laererstyrt turaktivitet (punkt 2.3)
FRILUFTSLIV_FAKTOR = 2.0                    # samme som kategori C
TURTILLEGG_TIMER = 15                       # timer per turdogn per ekstra laerer
LAERERGRENSE_STUDENTER = 30                 # over dette kreves tredje laerer (to ekstra)
MAX_TURDOGN = {10: 9, 15: 14}               # inntil dette antall turdogn per emnestorrelse (sp)

SP_VALG = [2.5, 5, 7.5, 10, 15, 20, 30]

# Egenartsfaktor (kategori A, B, C) og emnetyper med egen beregning
KATEGORIER = {
    "Kategori A (faktor 1,0)": 1.0,
    "Kategori B (faktor 1,5)": 1.5,
    "Kategori C (faktor 2,0)": 2.0,
    "Friluftsliv med lærerstyrt turaktivitet": FRILUFTSLIV_FAKTOR,
    "Digitalt emne": None,   # egen beregning, uten egenartsfaktor og normtall
}
FRILUFTSLIV = "Friluftsliv med lærerstyrt turaktivitet"
DIGITALT = "Digitalt emne"
# =====================================================================


def sats_per_student(sp: float) -> float:
    """Tillegg/fratrekk-sats (timer per student) etter skalaen i punkt 2.1."""
    if sp < 5:
        return 1.0
    elif sp < 10:
        return 1.25
    else:
        return 1.5


def sensortillegg(sp: float, antall_studenter: int) -> float:
    """Fast tillegg for emner med krav om to sensorer (fotnote til 2.1).
    Gjelder alle studenter, uavhengig av normtall og egenartsfaktor."""
    if sp >= SENSOR_GRENSE_SP:
        return SENSOR_TILLEGG_PER_STUDENT * antall_studenter
    return 0.0


def ekstra_laerere(antall_studenter: int) -> int:
    """Antall lærere på tur utover én: 1 ved ordinær bemanning (to lærere),
    2 ved mer enn 30 studenter (tre lærere)."""
    return 2 if antall_studenter > LAERERGRENSE_STUDENTER else 1


def turtillegg(turdogn: float, antall_studenter: int) -> float:
    return TURTILLEGG_TIMER * turdogn * ekstra_laerere(antall_studenter)


def beregn_campus(sp, basesats, normtall, f, antall_studenter, turdogn=0.0):
    grunnressurs = sp * basesats
    grunnressurs_justert = grunnressurs * (0.75 + 0.25 * f)
    studentjustering = (antall_studenter - normtall) * sats_per_student(sp) * f
    sensor_t = sensortillegg(sp, antall_studenter)
    tur_t = turtillegg(turdogn, antall_studenter) if turdogn else 0.0
    total = grunnressurs_justert + studentjustering + sensor_t + tur_t
    return total, grunnressurs_justert, studentjustering, sensor_t, tur_t


def beregn_digitalt(sp, antall_studenter):
    """Digitale emner: egen grunnressurs, ingen egenartsfaktor, ingen normtall,
    ingen fratrekk. Alle studenter gir tillegg etter samme skala som campus."""
    grunnressurs = sp * BASESATS_DIGITALT
    studentressurs = antall_studenter * sats_per_student(sp)
    sensor_t = sensortillegg(sp, antall_studenter)
    total = grunnressurs + studentressurs + sensor_t
    return total, grunnressurs, studentressurs, sensor_t


def vis_resultat(total, rader, ekstra=None):
    st.subheader("Resultat")
    st.metric("Totalt antall timer", f"{total:.1f} timer")
    with st.expander("Vis beregning"):
        tabell = "| Komponent | Timer |\n|---|---|\n"
        for navn, verdi in rader:
            tabell += f"| {navn} | {verdi} |\n"
        tabell += f"| **Total** | **{total:.1f}** |\n"
        st.markdown(tabell)
        if ekstra:
            st.markdown(ekstra)


# --- Steg 1: Studiepoeng ---
studiepoeng = st.selectbox(
    "Studiepoeng (SP)", options=SP_VALG, index=SP_VALG.index(10),
    format_func=lambda x: f"{x} SP"
)
st.divider()

# --- Steg 2: Kategori / emnetype ---
kategori_label = st.selectbox("Egenartsfaktor / emnetype", options=list(KATEGORIER.keys()))
er_digitalt = kategori_label == DIGITALT
er_friluftsliv = kategori_label == FRILUFTSLIV
st.divider()

if not er_digitalt:
    # --- Steg 3: Nivaa (kun campus) ---
    nivaa = st.radio("Velg nivå", ["Bachelor", "Master"], horizontal=True)
    basesats = BASESATS[nivaa]
    normtall = NORMTALL[nivaa]
    f = KATEGORIER[kategori_label]
    st.divider()

    antall_studenter = st.number_input(
        "Antall studenter", min_value=1, max_value=1000, value=normtall, step=1
    )

    turdogn = 0
    if er_friluftsliv:
        ramme = MAX_TURDOGN.get(int(studiepoeng)) if float(studiepoeng).is_integer() else None
        turdogn = st.number_input(
            "Antall turdøgn i emnet", min_value=0, max_value=60,
            value=ramme if ramme is not None else 0, step=1
        )
        if ramme is not None:
            st.caption(f"Ramme: inntil {ramme} turdøgn for {int(studiepoeng)} studiepoeng.")
            if turdogn > ramme:
                st.warning(
                    f"Over rammen på {ramme} turdøgn for {int(studiepoeng)} sp. "
                    "Omfordeling forutsetter at samlet antall turdøgn i programmet ikke øker."
                )
        else:
            st.caption("Normen angir ramme for 10 og 15 studiepoeng.")
        n_ekstra = ekstra_laerere(antall_studenter)
        st.caption(
            f"Lærere på tur: **{n_ekstra + 1}** ({n_ekstra} ekstra) "
            f"{'– mer enn ' + str(LAERERGRENSE_STUDENTER) + ' studenter krever tredje lærer' if n_ekstra == 2 else ''}"
        )

    st.caption(
        f"Grunnressurs: **{basesats} t/sp** · Normtall: **{normtall} studenter** · "
        f"Sats per student: **{sats_per_student(studiepoeng)} t**"
    )
    st.divider()

    total, gb, sj, sensor_t, tur_t = beregn_campus(
        studiepoeng, basesats, normtall, f, antall_studenter, turdogn
    )
    rader = [
        ("Justert grunnressurs", f"{gb:.1f}"),
        ("Studentjustering (tillegg/fratrekk)", f"{sj:+.1f}"),
        ("Sensortillegg (≥15 sp, alle studenter)", f"{sensor_t:+.1f}"),
    ]
    if er_friluftsliv:
        rader.append((
            f"Turtillegg ({TURTILLEGG_TIMER} t × {turdogn} turdøgn × {ekstra_laerere(antall_studenter)} ekstra lærer(e))",
            f"{tur_t:+.1f}",
        ))
    vis_resultat(
        total,
        rader,
        ekstra=f"""
| Variabel | Verdi |
|---|---|
| Nivå | {nivaa} |
| Kategori / emnetype | {kategori_label} |
| Studiepoeng (SP) | {studiepoeng} |
| Egenartsfaktor | {f} |
| Sats per student | {sats_per_student(studiepoeng)} |
| Normtall | {normtall} |
| Antall studenter | {antall_studenter} |
""",
    )

else:
    antall_studenter = st.number_input(
        "Antall studenter", min_value=1, max_value=1000, value=60, step=1
    )
    st.caption(
        f"Grunnressurs: **{BASESATS_DIGITALT} t/sp** · Ingen normtall og ingen fratrekk · "
        f"Sats per student: **{sats_per_student(studiepoeng)} t**"
    )
    st.divider()

    total, gb, sr, sensor_t = beregn_digitalt(studiepoeng, antall_studenter)
    vis_resultat(
        total,
        [
            ("Grunnressurs", f"{gb:.1f}"),
            ("Ressurs per student (alle studenter)", f"{sr:.1f}"),
            ("Sensortillegg (≥15 sp, alle studenter)", f"{sensor_t:+.1f}"),
        ],
        ekstra=f"""
| Variabel | Verdi |
|---|---|
| Emnetype | Digitalt |
| Studiepoeng (SP) | {studiepoeng} |
| Grunnressurs per sp | {BASESATS_DIGITALT} |
| Sats per student | {sats_per_student(studiepoeng)} |
| Antall studenter | {antall_studenter} |
""",
    )

st.divider()
with st.expander("Mer informasjon om normer for studentrettet aktivitet"):
    st.markdown(
        "Ressursen skal dekke emneansvar, forberedelse og gjennomføring av "
        "undervisning, veiledning og studentkontakt, sensur- og "
        "vurderingsarbeid, administrasjon og koordinering, samt faglig "
        "oppdatering.\n\n"
        "- **Grunnressurs**: studiepoeng multiplisert med en fast sats "
        f"({BASESATS['Bachelor']} t/sp for bachelor, {BASESATS['Master']} t/sp for master, "
        f"{BASESATS_DIGITALT} t/sp for digitale emner).\n"
        "- **Egenartsfaktor (kategori A, B, C)**: påvirker 25 % av grunnressursen "
        "og hele studentjusteringen. Gjelder ikke digitale emner.\n"
        "- **Studentjustering**: tillegg eller fratrekk dersom antall studenter "
        "avviker fra normtallet. Digitale emner har ikke normtall, og alle "
        "studenter gir tillegg.\n"
        "- **Sensortillegg**: 0,5 timer per student for emner på 15 studiepoeng "
        "eller mer (krav om to sensorer). Gjelder alle studenter, uavhengig av "
        "normtall og egenartsfaktor.\n"
        "- **Friluftsliv med lærerstyrt turaktivitet**: beregnes som kategori C, "
        f"med et turtillegg på {TURTILLEGG_TIMER} timer × antall turdøgn × antall "
        "ekstra lærere (lærere utover én). Ved mer enn "
        f"{LAERERGRENSE_STUDENTER} studenter kreves tredje lærer.\n\n"
        "Se normdokumentet (**Normer for studentrettet aktivitet**, kap. 2) "
        "for fullstendig regelverk og særskilte ordninger (bl.a. "
        "veiledningsemner og praksisemner)."
    )