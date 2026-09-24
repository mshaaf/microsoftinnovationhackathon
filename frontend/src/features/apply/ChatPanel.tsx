import { useState } from "react";
import { useJourney } from "../../app/JourneyContext";
import { useLanguage } from "../../app/LanguageContext";
import { apiRequest } from "../../shared/api/client";
import { HandoffCard } from "../handoff/HandoffCard";
import type { Handoff } from "../handoff/HandoffCard";
import styles from "./ApplyPage.module.css";

type Reply = { reply: string; citations: { title: string; url: string }[] };
const post = (body: unknown) => ({
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(body),
});

export function ChatPanel() {
  const { t, language } = useLanguage();
  const { journey } = useJourney();
  // In memory only: never written to storage or URLs.
  const [sessionId] = useState(() => crypto.randomUUID());
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [reply, setReply] = useState<Reply | null>(null);
  const [card, setCard] = useState<Handoff | null>(null);

  async function send(e: React.FormEvent) {
    e.preventDefault();
    if (!message.trim()) return;
    setBusy(true);
    setError("");
    try {
      const res = await apiRequest(
        "/api/chat",
        post({
          session_id: sessionId,
          message,
          lang: language,
          context: { disaster_number: Number(journey.disasterNumber) || 9999 },
        }),
      );
      setReply(res);
      setCard(res.handoff ?? null);
      setMessage("");
    } catch {
      setError(t("apply.chatError"));
    } finally {
      setBusy(false);
    }
  }

  async function person() {
    setError("");
    try {
      const res = await apiRequest(
        "/api/escalate",
        post({ session_id: sessionId, reason: "user_request", lang: language }),
      );
      setCard(res.card);
    } catch {
      setError(t("apply.personError"));
    }
  }

  return (
    <section className={styles.panel} aria-labelledby="chat-title">
      <h2 id="chat-title">{t("apply.chatTitle")}</h2>
      <p className={styles.hint}>{t("apply.chatHint")}</p>
      <form onSubmit={send}>
        <label htmlFor="chat-input">{t("apply.chatLabel")}</label>
        <textarea
          id="chat-input"
          className={styles.input}
          rows={3}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />
        <button type="submit" className={styles.big} disabled={busy}>
          {busy ? t("apply.sending") : t("apply.send")}
        </button>
      </form>
      {error && <p role="alert">{error}</p>}
      {reply && (
        <div className={styles.reply} aria-live="polite">
          <p>{reply.reply}</p>
          {reply.citations.length > 0 && (
            <>
              <p className={styles.hint}>{t("apply.sources")}</p>
              <ul>
                {reply.citations.map((c) => (
                  <li key={c.url}>
                    <a href={c.url} target="_blank" rel="noreferrer">
                      {c.title}
                    </a>
                  </li>
                ))}
              </ul>
            </>
          )}
        </div>
      )}
      {card && <HandoffCard card={card} />}
      <button type="button" className={styles.link} onClick={() => void person()}>
        {t("apply.person")}
      </button>
    </section>
  );
}
