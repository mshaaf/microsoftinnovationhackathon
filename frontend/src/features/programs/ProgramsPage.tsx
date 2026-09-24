import { useState } from "react";
import type { FormEvent } from "react";
import { Link } from "react-router";
import { useJourney } from "../../app/JourneyContext";
import { useLanguage } from "../../app/LanguageContext";
import { apiRequest } from "../../shared/api/client";
import type { ApiResponse } from "../../shared/api/client";
import styles from "./ProgramsPage.module.css";

type ApiCard = ApiResponse<"/api/programs">["cards"][number];
type Card = Omit<ApiCard, "deadline"> & { deadline: ApiCard["deadline"] | null };
type Tier = Card["tier"];
type Status = "asking" | "loading" | "error" | "done" | "empty";

const tierOrder: Record<Tier, number> = {
  check_now: 0,
  open: 1,
  likely: 2,
  optional: 3,
};

const tierDisplay: Record<Tier, { icon: string; label: string }> = {
  check_now: { icon: "!", label: "checkNow" },
  open: { icon: "✓", label: "open" },
  likely: { icon: "?", label: "likely" },
  optional: { icon: "○", label: "optional" },
};

const yesNo = [true, false] as const;

export function ProgramsPage() {
  const { t, language } = useLanguage();
  const { journey } = useJourney();
  const [lostWork, setLostWork] = useState<boolean | null>(null);
  const [onSnap, setOnSnap] = useState<boolean | null>(null);
  const [householdSize, setHouseholdSize] = useState("");
  const [status, setStatus] = useState<Status>("asking");
  const [cards, setCards] = useState<Card[]>([]);

  const housing = journey.answers.housing;
  const disasterNumber = Number(journey.disasterNumber);
  const hasJourney =
    /^\d{5}$/.test(journey.zipCode) &&
    Boolean(journey.county) &&
    Number.isInteger(disasterNumber) &&
    disasterNumber > 0 &&
    (housing === "own" || housing === "rent");
  const questions = [
    { name: "lost-work", label: "lostWork", answer: lostWork, setAnswer: setLostWork },
    { name: "on-snap", label: "onSnap", answer: onSnap, setAnswer: setOnSnap },
  ];

  async function load() {
    const size = Number(householdSize);
    if (lostWork === null || onSnap === null || !Number.isInteger(size) || size < 1) return;

    setStatus("loading");
    try {
      const location = await apiRequest("/api/location", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ zip: journey.zipCode }),
      });
      const matches = location.counties.filter((county) => county.name === journey.county);
      if (matches.length !== 1) throw new Error("Could not match the selected county");

      const response = await apiRequest("/api/programs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          disaster_number: disasterNumber,
          county_fips: matches[0].county_fips,
          lang: language,
          answers: {
            housing,
            lost_work_or_self_employed: lostWork,
            on_snap: onSnap,
            household_size: size,
          },
        }),
      });
      setCards(response.cards);
      setStatus(response.cards.length ? "done" : "empty");
    } catch {
      setStatus("error");
    }
  }

  function submit(event: FormEvent) {
    event.preventDefault();
    void load();
  }

  const date = (value: string) =>
    new Intl.DateTimeFormat(language, { dateStyle: "long", timeZone: "UTC" }).format(
      new Date(`${value}T00:00:00Z`),
    );

  if (!hasJourney) {
    return (
      <section className={styles.page}>
        <h1>{t("programs.title")}</h1>
        <p>{t("programs.missingJourney")}</p>
        <Link to="/help-here">{t("programs.backToStart")}</Link>
      </section>
    );
  }

  return (
    <section className={styles.page}>
      <h1>{t("programs.title")}</h1>
      <p className={styles.description}>{t("programs.description")}</p>

      <form className={styles.form} onSubmit={submit}>
        {questions.map(({ name, label, answer, setAnswer }) => (
          <fieldset key={name} className={styles.question}>
            <legend>{t(`programs.${label}`)}</legend>
            {yesNo.map((value) => (
              <label key={String(value)} className={styles.choice}>
                <input type="radio" name={name} value={String(value)} checked={answer === value}
                  required onChange={() => setAnswer(value)} />
                {t(value ? "programs.yes" : "programs.no")}
              </label>
            ))}
          </fieldset>
        ))}

        <label className={styles.household} htmlFor="household-size">
          {t("programs.householdSize")}
          <input
            id="household-size"
            type="number"
            min="1"
            step="1"
            required
            value={householdSize}
            onChange={(event) => setHouseholdSize(event.target.value)}
          />
        </label>
        <button type="submit" disabled={status === "loading"}>
          {t("programs.submit")}
        </button>
      </form>

      {status === "loading" && <p role="status">{t("programs.loading")}</p>}

      {status === "error" && (
        <div className={styles.error} role="alert">
          <p>{t("programs.error")}</p>
          <button type="button" onClick={() => void load()}>
            {t("programs.retry")}
          </button>
        </div>
      )}

      {status === "empty" && <p>{t("programs.empty")}</p>}

      {status === "done" && (
        <div className={styles.cards}>
          {[...cards]
            .sort((a, b) => tierOrder[a.tier] - tierOrder[b.tier])
            .map((card) => {
              const tier = tierDisplay[card.tier];
              return (
                <article key={card.program_id} className={styles.card}>
                  <p className={styles.tier} data-tier={card.tier}>
                    <span aria-hidden="true">{tier.icon}</span>
                    <span>{t(`programs.tier.${tier.label}`)}</span>
                  </p>
                  <h2>{card.title}</h2>
                  <p>{card.why}</p>
                  <p>
                    <strong>{card.deadline ? `${card.deadline.label}:` : t("programs.noDeadline")}</strong>
                    {card.deadline && ` ${date(card.deadline.date)}`}
                  </p>
                  <p>
                    <strong>{t("programs.howToApply")}:</strong> {card.how_to_apply}
                  </p>
                  <a href={card.source_url} target="_blank" rel="noreferrer">
                    {t("programs.source")}
                  </a>
                  <p className={styles.verified}>
                    {t("programs.lastVerified")}: {date(card.last_verified)}
                  </p>
                </article>
              );
            })}
        </div>
      )}
    </section>
  );
}
