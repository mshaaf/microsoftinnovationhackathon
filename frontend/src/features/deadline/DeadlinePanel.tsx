import { useState } from "react";
import { useLanguage } from "../../app/LanguageContext";
import type { ApiResponse } from "../../shared/api/client";
import styles from "./DeadlinePanel.module.css";

type Result = ApiResponse<"/api/letter/decode">;

export function DeadlinePanel({ deadline, templateId }: { deadline: Result["deadline"]; templateId: string }) {
  const { t, language } = useLanguage();
  const [name, setName] = useState("");
  const [registration, setRegistration] = useState("");
  const [copied, setCopied] = useState(false);
  const due = new Date(`${deadline.appeal_due}T00:00:00Z`).toLocaleDateString(language === "es" ? "es-ES" : "en-US", { year: "numeric", month: "long", day: "numeric", timeZone: "UTC" });
  const reason = t(`deadline.template.${templateId}`);
  const detail = reason === `deadline.template.${templateId}` ? t("deadline.template.other_or_unclear") : reason;
  const draft = [
    t("deadline.draftTo"),
    "",
    t("deadline.draftSubject"),
    "",
    t("deadline.draftIntro"),
    detail,
    t("deadline.draftClose"),
    "",
    name || t("deadline.namePlaceholder"),
    registration ? `${t("deadline.registration")}: ${registration}` : "",
  ].filter((line, index) => line || index < 9).join("\n");

  async function copy() {
    try {
      await navigator.clipboard.writeText(draft);
      setCopied(true);
    } catch {
      setCopied(false);
    }
  }

  return <section className={styles.panel}>
    <h2>{t("deadline.heading")}</h2>
    <p><strong>{due}</strong> · {deadline.days_left > 0 ? t("deadline.daysLeft").replace("{n}", String(deadline.days_left)) : deadline.days_left === 0 ? t("deadline.dueToday") : t("deadline.pastDue")}</p>
    <p>{deadline.rule}</p>
    <h3>{t("deadline.draftHeading")}</h3>
    <p>{t("deadline.localOnly")}</p>
    <label>{t("deadline.name")}<input value={name} onChange={(event) => setName(event.target.value)} autoComplete="off" /></label>
    <label>{t("deadline.registrationLabel")}<input value={registration} onChange={(event) => setRegistration(event.target.value)} autoComplete="off" /></label>
    <label>{t("deadline.draftLabel")}<textarea className={styles.draft} value={draft} readOnly rows={12} /></label>
    <div className={styles.actions}>
      <button type="button" onClick={() => void copy()}>{t("deadline.copy")}</button>
      <button type="button" onClick={() => window.print()}>{t("deadline.print")}</button>
    </div>
    {copied && <p role="status">{t("deadline.copied")}</p>}
    <p>{t("deadline.review")}</p>
    <a href="https://www.fema.gov/assistance/individual/after-applying/appeals" target="_blank" rel="noreferrer">{t("deadline.send")}</a>
  </section>;
}
