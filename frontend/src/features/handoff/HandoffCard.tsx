import { useT } from "../../app/LanguageContext";
import styles from "./HandoffCard.module.css";

export type Handoff = {
  title: string;
  steps: string[];
  phones: { label: string; number: string }[];
};

// Text comes from the server already translated; only the "Call" label is local.
export function HandoffCard({ card }: { card: Handoff }) {
  const t = useT();
  return (
    <section className={styles.card} aria-label={card.title}>
      <h2>{card.title}</h2>
      <ul>
        {card.steps.map((step) => (
          <li key={step}>{step}</li>
        ))}
      </ul>
      <div className={styles.phones}>
        {card.phones.map((p) => (
          <a
            key={p.number}
            className={styles.phone}
            href={`tel:${p.number.replace(/[^\d+]/g, "")}`}
            aria-label={`${t("handoff.call")} ${p.label} ${p.number}`}
          >
            {p.label}: {p.number}
          </a>
        ))}
      </div>
    </section>
  );
}
