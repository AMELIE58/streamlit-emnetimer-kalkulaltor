# Kalkulator for timer per emne

En liten Streamlit-app som beregner arbeidstidsressurs per emne ("Beregning av timer per emne"), basert på utkastet til **Normer for studentrettet aktivitet** (kap. 2). Kalkulatoren tar utgangspunkt i emnets størrelse (studiepoeng), antall studenter, nivå og egenart.

## Kjør lokalt

```bash
pip install streamlit
streamlit run main.py
```

Appen må kjøres med `streamlit run` i et vanlig terminalvindu (cmd, PowerShell eller Anaconda Prompt) fra mappen der `main.py` ligger. Den fungerer ikke med «Run file» i Spyder.

## Verdier i modellen

| | Bachelor | Master | Digitale emner |
|---|---|---|---|
| Grunnressurs | 25 t/sp | 20 t/sp | 15 t/sp |
| Normtall (normert studentgruppe) | 35 | 25 | ingen |
| Egenartsfaktor | A / B / C | A / B / C | brukes ikke |
| Fratrekk ved få studenter | ja | ja | nei |

**Egenartsfaktor (kategori):** A = 1,0, B = 1,5, C = 2,0. Faktoren påvirker 25 % av grunnressursen og hele studentjusteringen.

**Sats per student (studentjustering):**

| Studiepoeng | Timer per student |
|---|---|
| under 5 | 1,0 |
| 5–9 | 1,25 |
| 10 eller mer | 1,5 |

**Sensortillegg:** 0,5 timer per student for emner på 15 studiepoeng eller mer (krav om to sensorer). Gjelder alle studenter, uavhengig av normtall og egenartsfaktor. Det gjelder også digitale emner.

## Formler

**Campus-emner (bachelor og master)**

```
Total = SP × grunnsats × (0,75 + 0,25 × f)
      + (Studenter − Normtall) × sats × f
      + Sensortillegg
```

der `SP` er studiepoeng, `f` er egenartsfaktoren, `sats` er sats per student etter skalaen over, og sensortillegget er 0,5 × antall studenter ved 15 sp eller mer.

**Digitale emner**

```
Total = SP × 15 + Studenter × sats + Sensortillegg
```

Egenartsfaktor og normtall brukes ikke, og det gjøres ikke fratrekk ved lavt studenttall.

**Friluftsliv med lærerstyrt turaktivitet**

Beregnes som kategori C (faktor 2,0), pluss et turtillegg:

```
Turtillegg = 15 timer × antall turdøgn × antall ekstra lærere
```

Med ekstra lærere menes lærere på tur utover én. Det er én ekstra lærer ved ordinær bemanning, og to ekstra ved mer enn 30 studenter (tredje lærer av sikkerhetshensyn). Rammen er inntil 9 turdøgn per 10 sp og 14 per 15 sp.

## Ikke med i kalkulatoren

- Emner med hovedvekt på veiledning (bachelor- og masteroppgaver), som beregnes etter punkt 2.3 i normen.
- Praksisemner, som dekkes innenfor ordinær timeressurs og avklares med instituttleder.

## Endre verdier

Alle tall fra normen ligger samlet øverst i `main.py`, under «VERDIER FRA NORMEN». Når normen endres, er det normalt bare der noe må justeres.

## Status

Dette er et utkast til arbeidsgruppen. Satsene og tallene kan endres før normen vedtas.