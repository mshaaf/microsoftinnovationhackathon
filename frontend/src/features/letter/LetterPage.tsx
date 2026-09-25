import { useRef, useState } from "react";
import { Link } from "react-router";
import { useLanguage } from "../../app/LanguageContext";
import { apiRequest } from "../../shared/api/client";
import type { ApiResponse } from "../../shared/api/client";
import { DeadlinePanel } from "../deadline/DeadlinePanel";
import { HandoffCard } from "../handoff/HandoffCard";
import styles from "./LetterPage.module.css";

type Result = ApiResponse<"/api/letter/decode">;
type Status = "empty" | "reading" | "removing" | "explaining" | "error" | "done";
const allowed = ["image/jpeg", "image/png", "application/pdf"];

export function LetterPage() {
  const { t, language } = useLanguage();
  const [status, setStatus] = useState<Status>("empty");
  const [result, setResult] = useState<Result | null>(null);
  const [error, setError] = useState("");
  const lastFile = useRef<File | null>(null);

  async function decode(file: File) {
    lastFile.current = file;
    setResult(null);
    if (!allowed.includes(file.type) || file.size > 10_000_000) {
      setError(t("letter.fileError"));
      setStatus("error");
      return;
    }
    const body = new FormData();
    body.append("file", file);
    body.append("lang", language);
    setStatus("reading");
    try {
      const response = await apiRequest("/api/letter/decode", { method: "POST", body });
      setStatus("removing");
      await new Promise((resolve) => setTimeout(resolve, 350));
      setStatus("explaining");
      await new Promise((resolve) => setTimeout(resolve, 350));
      setResult(response);
      setStatus("done");
    } catch {
      setError(t("letter.error"));
      setStatus("error");
    }
  }

  const handoff = result?.handoff;
  return <section className={styles.page}>
    <h1>{t("letter.title")}</h1>
    <p>{t("letter.description")}</p>
    <div className={styles.upload}>
      <label>{t("letter.fileLabel")}<input type="file" accept={allowed.join(",")} onChange={(event) => { const file = event.target.files?.[0]; if (file) void decode(file); }} /></label>
      <label>{t("letter.cameraLabel")}<input type="file" accept="image/*" capture="environment" onChange={(event) => { const file = event.target.files?.[0]; if (file) void decode(file); }} /></label>
      <p>{t("letter.fileHint")}</p>
    </div>
    {status === "empty" && <p>{t("letter.empty")}</p>}
    {["reading", "removing", "explaining"].includes(status) && <p role="status">{t(`letter.${status}`)}</p>}
    {status === "error" && <div role="alert"><p>{error}</p><button type="button" onClick={() => { if (lastFile.current) void decode(lastFile.current); }}>{t("letter.retry")}</button></div>}
    {status === "done" && result && <>
      <section className={styles.panel}>
        <h2>{t("letter.removedTitle")}</h2>
        <p>{t("letter.removedCount").replace("{n}", String(result.redaction.entities_removed))}</p>
        <p>{result.redaction.categories.map((category) => {
          const key = `letter.category.${category}`;
          const label = t(key);
          return label === key ? t("letter.category.fallback") : label;
        }).join(", ") || t("letter.noneRemoved")}</p>
      </section>
      <section className={styles.panel}>
        <h2>{t("letter.previewTitle")}</h2>
        {result.redacted_preview ? <pre className={styles.preview} aria-label={t("letter.previewLabel")}>{result.redacted_preview}</pre> : <p>{t("letter.noPreview")}</p>}
      </section>
      {handoff ? <HandoffCard card={{ title: t("letter.handoffTitle"), steps: [t("letter.handoffStep")], phones: [{ label: t("letter.helpline"), number: "1-800-621-3362" }] }} /> : <>
        <section className={styles.panel}>
          <h2>{t("letter.explanationTitle")}</h2>
          <p>{result.explanation || t("letter.noExplanation")}</p>
          <h2>{t("letter.checklistTitle")}</h2>
          {result.checklist.length ? <ul>{result.checklist.map((item) => <li key={item.id}>{item.text} <a href={item.source_url} target="_blank" rel="noreferrer">{t("letter.source")}</a></li>)}</ul> : <p>{t("letter.noChecklist")}</p>}
        </section>
        <DeadlinePanel deadline={result.deadline} templateId={result.appeal_template_id} />
      </>}
    </>}
    <Link className={styles.continue} to="/deadline">{t("app.continue")}</Link>
  </section>;
}
