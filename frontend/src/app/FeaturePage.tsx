import { Link } from "react-router";
import { useT } from "./LanguageContext";
import styles from "./FeaturePage.module.css";

type Feature = "help-here" | "apply" | "letter" | "deadline" | "programs" | "about";

export function FeaturePage({
  feature,
  next,
}: {
  feature: Feature;
  next?: string;
}) {
  const t = useT();

  return (
    <section className={styles.page}>
      <h1>{t(`${feature}.title`)}</h1>
      <p className={styles.description}>{t(`${feature}.description`)}</p>
      {next && (
        <Link className={styles.continue} to={next}>
          {t("app.continue")}
        </Link>
      )}
    </section>
  );
}
