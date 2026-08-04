# Course Hour Calculator

A small Streamlit app for calculating teaching hours per course ("Beregning av timer per emne"), based on credits (SP), a subject-type factor, and number of students. Supports Bachelor and Master level courses.

## Run locally

```bash
pip install streamlit
streamlit run main.py
```

## Formula

```
Total hours = (SP × 25 × (0.75 + 0.25 × f)) + ((Students - 35) × k × f)
```

- **SP** – credits (studiepoeng)
- **f** – subject-type factor (theoretical / practical)
- **k** – rate per student, derived from SP
