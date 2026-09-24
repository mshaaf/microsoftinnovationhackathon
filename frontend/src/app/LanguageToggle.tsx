import styles from "./LanguageToggle.module.css";
import { useLanguage } from "./LanguageContext";

export function LanguageToggle() {
  const { language, setLanguage, t } = useLanguage();

  return (
    <button
      className={styles.button}
      type="button"
      onClick={() => setLanguage(language === "en" ? "es" : "en")}
    >
      {t("app.languageButton")}
    </button>
  );
}
