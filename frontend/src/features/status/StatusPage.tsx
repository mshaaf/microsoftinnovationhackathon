import { useEffect, useState } from "react";
import { useT } from "../../app/LanguageContext";
import { apiRequest } from "../../shared/api/client";
import type { ApiResponse } from "../../shared/api/client";
import styles from "./StatusPage.module.css";

type Health = ApiResponse<"/api/health">;
type ServiceName = keyof Health["services"];

const serviceNames: Record<ServiceName, string> = {
  openfema: "OpenFEMA",
  geo: "Geo",
  search: "Search",
  model: "Model",
  ocr: "OCR",
  pii: "PII",
  translator: "Translator",
  safety: "Safety",
};

export function StatusPage() {
  const t = useT();
  const [health, setHealth] = useState<Health | null>(null);
  const [failed, setFailed] = useState(false);
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    let active = true;
    setHealth(null);
    setFailed(false);

    apiRequest("/api/health")
      .then((response) => {
        if (active) setHealth(response);
      })
      .catch(() => {
        if (active) setFailed(true);
      });

    return () => {
      active = false;
    };
  }, [attempt]);

  if (failed) {
    return (
      <section className={styles.page}>
        <h1>{t("status.title")}</h1>
        <p role="alert">{t("status.error")}</p>
        <button
          className={styles.retry}
          type="button"
          onClick={() => setAttempt((current) => current + 1)}
        >
          {t("status.retry")}
        </button>
      </section>
    );
  }

  if (!health) {
    return (
      <section className={styles.page}>
        <h1>{t("status.title")}</h1>
        <p role="status">{t("status.loading")}</p>
      </section>
    );
  }

  const services = Object.entries(health.services);

  return (
    <section className={styles.page}>
      <h1>{t("status.title")}</h1>
      <p className={styles.mode}>
        {t("status.mode")}: {t(`status.${health.mode}`)}
      </p>
      {services.length === 0 ? (
        <p>{t("status.empty")}</p>
      ) : (
        <dl className={styles.services}>
          {services.map(([key, value]) => (
            <div className={styles.service} key={key}>
              <dt>{serviceNames[key as ServiceName]}</dt>
              <dd>{t(`status.service.${value}`)}</dd>
            </div>
          ))}
        </dl>
      )}
    </section>
  );
}
