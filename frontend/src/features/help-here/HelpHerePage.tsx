import { useState } from "react";
import type { FormEvent } from "react";
import { Link } from "react-router";
import { useJourney } from "../../app/JourneyContext";
import { useLanguage } from "../../app/LanguageContext";
import { apiRequest } from "../../shared/api/client";
import type { ApiResponse } from "../../shared/api/client";
import styles from "./HelpHerePage.module.css";

type County = ApiResponse<"/api/location">["counties"][number];
type Declaration = ApiResponse<"/api/declarations">["declarations"][number];
type View =
  | { step: "form" }
  | { step: "loading" }
  | { step: "error" }
  | { step: "pick"; counties: County[] }
  | { step: "result"; county: County; declarations: Declaration[] };

export function HelpHerePage() {
  const { t, language } = useLanguage();
  const { updateJourney } = useJourney();
  const [zip, setZip] = useState("");
  const [zipError, setZipError] = useState(false);
  const [view, setView] = useState<View>({ step: "form" });
  const [picked, setPicked] = useState("");

  const fill = (key: string, vars: Record<string, string | number> = {}) =>
    Object.entries(vars).reduce(
      (text, [k, v]) => text.replaceAll(`{${k}}`, String(v)),
      t(`help-here.${key}`),
    );
  // Dates arrive as YYYY-MM-DD; format in UTC so the day never shifts.
  const date = (iso: string) =>
    new Intl.DateTimeFormat(language, { dateStyle: "long", timeZone: "UTC" }).format(
      new Date(iso),
    );

  async function lookup(county: County) {
    setView({ step: "loading" });
    try {
      const data = await apiRequest("/api/declarations", {
        params: new URLSearchParams({
          state: county.state,
          county_fips: county.county_fips,
          lang: language,
        }),
      });
      const first = data.declarations[0];
      updateJourney({
        zipCode: zip,
        county: county.name,
        disasterNumber: first ? String(first.disaster_number) : "",
      });
      setView({ step: "result", county, declarations: data.declarations });
    } catch {
      setView({ step: "error" });
    }
  }

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    if (!/^\d{5}$/.test(zip)) {
      setZipError(true);
      return;
    }
    setZipError(false);
    setView({ step: "loading" });
    try {
      const loc = await apiRequest("/api/location", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ zip }),
      });
      if (loc.needs_confirmation) {
        setPicked("");
        setView({ step: "pick", counties: loc.counties });
      } else {
        await lookup(loc.counties[0]);
      }
    } catch {
      setView({ step: "error" });
    }
  }

  const busy = view.step === "loading";

  return (
    <section className={styles.page}>
      <h1>{t("help-here.title")}</h1>
      <p className={styles.description}>{t("help-here.description")}</p>

      <form onSubmit={onSubmit} noValidate className={styles.form}>
        <label htmlFor="zip">{t("help-here.zipLabel")}</label>
        <span id="zip-hint" className={styles.hint}>
          {t("help-here.zipHint")}
        </span>
        <div className={styles.row}>
          <input
            id="zip"
            inputMode="numeric"
            autoComplete="postal-code"
            maxLength={5}
            value={zip}
            aria-invalid={zipError}
            aria-describedby={zipError ? "zip-hint zip-error" : "zip-hint"}
            onChange={(e) => setZip(e.target.value)}
          />
          <button type="submit" disabled={busy}>
            {t("help-here.check")}
          </button>
        </div>
        {zipError && (
          <p id="zip-error" role="alert" className={styles.error}>
            {t("help-here.zipError")}
          </p>
        )}
      </form>

      {view.step === "loading" && (
        <p role="status" className={styles.status}>
          {t("help-here.loading")}
        </p>
      )}

      {view.step === "error" && (
        <div role="alert" className={styles.error}>
          <p>{t("help-here.error")}</p>
          <button type="button" onClick={() => setView({ step: "form" })}>
            {t("help-here.retry")}
          </button>
        </div>
      )}

      {view.step === "pick" && (
        <fieldset className={styles.pick}>
          <legend>{t("help-here.pickCounty")}</legend>
          {view.counties.map((c) => (
            <label key={c.county_fips} className={styles.option}>
              <input
                type="radio"
                name="county"
                value={c.county_fips}
                checked={picked === c.county_fips}
                onChange={() => setPicked(c.county_fips)}
              />
              {fill("countyName", { name: c.name, state: c.state })}
            </label>
          ))}
          <button
            type="button"
            disabled={!picked}
            onClick={() => {
              const c = view.counties.find((x) => x.county_fips === picked);
              if (c) void lookup(c);
            }}
          >
            {t("help-here.countyChoose")}
          </button>
        </fieldset>
      )}

      {view.step === "result" && view.declarations.length === 0 && (
        <div className={styles.card}>
          <h2>{fill("noneHeading", { county: view.county.name })}</h2>
          <p>{t("help-here.noneBody")}</p>
          <ul>
            <li>{t("help-here.noneCall211")}</li>
            <li>{t("help-here.noneFema")}</li>
          </ul>
        </div>
      )}

      {view.step === "result" &&
        view.declarations.map((d) => (
          <article key={d.disaster_number} className={styles.card}>
            <h2>{fill("cardHeading", { number: d.disaster_number, title: d.title })}</h2>
            <p>{fill("declaredOn", { date: date(d.declaration_date) })}</p>
            <p className={styles.strong}>
              {fill(d.individual_assistance ? "iaOpen" : "iaClosed", {
                county: view.county.name,
              })}
            </p>
            {d.individual_assistance &&
              (d.registration_open ? (
                <p>{fill("registerBy", { date: date(d.registration_deadline) })}</p>
              ) : (
                <p className={styles.error}>
                  {fill("registrationClosed", { date: date(d.registration_deadline) })}
                </p>
              ))}
            <a href={d.fema_url} target="_blank" rel="noreferrer">
              {t("help-here.officialLink")}
            </a>
            {d.serious_needs.available && (
              <aside className={styles.callout}>
                <h3>{t("help-here.snHeading")}</h3>
                <p>{fill("snBody", { amount: d.serious_needs.amount_usd })}</p>
                <p>
                  {fill("snApplyBy", { date: date(d.serious_needs.apply_by) })}
                  {/* extension_possible is true in every current record; text says "may" */}
                </p>
                <p>{t("help-here.snNotTotal")}</p>
                <a href={d.serious_needs.source_url} target="_blank" rel="noreferrer">
                  {t("help-here.snSource")}
                </a>
              </aside>
            )}
          </article>
        ))}

      {view.step === "result" && (
        <Link className={styles.continue} to="/apply">
          {t("app.continue")}
        </Link>
      )}
    </section>
  );
}
