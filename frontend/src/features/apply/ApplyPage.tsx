import { useState } from "react";
import { Link } from "react-router";
import { useJourney } from "../../app/JourneyContext";
import { useLanguage } from "../../app/LanguageContext";
import { apiRequest } from "../../shared/api/client";
import type { ApiResponse } from "../../shared/api/client";
import { ChatPanel } from "./ChatPanel";
import styles from "./ApplyPage.module.css";

type Option = { value: string | boolean; label: string };
const yesNo: Option[] = [
  { value: true, label: "a.yes" },
  { value: false, label: "a.no" },
];
const questions: { key: string; options: Option[] }[] = [
  { key: "housing", options: [{ value: "own", label: "a.own" }, { value: "rent", label: "a.rent" }] },
  {
    key: "insured",
    options: [
      { value: "yes", label: "a.yes" },
      { value: "no", label: "a.no" },
      { value: "not_sure", label: "a.not_sure" },
    ],
  },
  { key: "lost_id", options: yesNo },
  { key: "displaced", options: yesNo },
];

type Checklist = ApiResponse<"/api/checklist">;
type Status = "asking" | "loading" | "error" | "done";

export function ApplyPage() {
  const { t, language } = useLanguage();
  const { journey, updateJourney } = useJourney();
  const [step, setStep] = useState(0);
  const [status, setStatus] = useState<Status>("asking");
  const [items, setItems] = useState<Checklist["items"]>([]);

  async function load(answers: Record<string, unknown>) {
    setStatus("loading");
    try {
      const res = await apiRequest("/api/checklist", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        // 9999 is the mock disaster; used only until Stage 1 sets a real one.
        body: JSON.stringify({
          disaster_number: Number(journey.disasterNumber) || 9999,
          lang: language,
          answers,
        }),
      });
      setItems(res.items);
      setStatus("done");
    } catch {
      setStatus("error");
    }
  }

  function answer(key: string, value: string | boolean) {
    updateJourney({ answers: { [key]: value } });
    if (step < questions.length - 1) setStep(step + 1);
    else void load({ ...journey.answers, [key]: value });
  }

  const q = questions[step];
  return (
    <section className={styles.page}>
      <h1>{t("apply.title")}</h1>
      <p className={styles.description}>{t("apply.description")}</p>

      {status === "asking" && (
        <div className={styles.panel}>
          <p className={styles.step}>{t("apply.step").replace("{n}", String(step + 1))}</p>
          <h2>{t(`apply.q.${q.key}`)}</h2>
          <div className={styles.options}>
            {q.options.map((o) => (
              <button
                key={String(o.value)}
                type="button"
                className={styles.big}
                onClick={() => answer(q.key, o.value)}
              >
                {t(`apply.${o.label}`)}
              </button>
            ))}
          </div>
          {step > 0 && (
            <button type="button" className={styles.link} onClick={() => setStep(step - 1)}>
              {t("apply.back")}
            </button>
          )}
        </div>
      )}

      {status === "loading" && <p role="status">{t("apply.loading")}</p>}

      {status === "error" && (
        <div role="alert" className={styles.panel}>
          <p>{t("apply.error")}</p>
          <button type="button" className={styles.big} onClick={() => void load(journey.answers)}>
            {t("apply.retry")}
          </button>
        </div>
      )}

      {status === "done" && (
        <div className={styles.panel}>
          <h2>{t("apply.checklistTitle")}</h2>
          {items.length === 0 ? (
            <p>{t("apply.empty")}</p>
          ) : (
            <ul className={styles.items}>
              {items.map((item) => (
                <li key={item.id}>
                  <strong>{item.text}</strong>
                  <p>
                    {t("apply.why")}: {item.why}
                  </p>
                  <a href={item.source_url} target="_blank" rel="noreferrer">
                    {t("apply.source")}
                  </a>
                </li>
              ))}
            </ul>
          )}
          <button
            type="button"
            className={styles.link}
            onClick={() => {
              setStep(0);
              setStatus("asking");
            }}
          >
            {t("apply.startOver")}
          </button>
        </div>
      )}

      <ChatPanel />

      <Link className={styles.continue} to="/letter">
        {t("app.continue")}
      </Link>
    </section>
  );
}
