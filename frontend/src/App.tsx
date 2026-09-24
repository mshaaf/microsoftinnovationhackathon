import { BrowserRouter, Link } from "react-router";
import styles from "./App.module.css";
import { JourneyProvider } from "./app/JourneyContext";
import { LanguageProvider, useT } from "./app/LanguageContext";
import { LanguageToggle } from "./app/LanguageToggle";
import { AppRoutes } from "./app/routes";
import { Stepper } from "./app/Stepper";

function AppLayout() {
  const t = useT();

  return (
    <div className={styles.site}>
      <header className={styles.header}>
        <div className={styles.headerInner}>
          <Link className={styles.brand} to="/">
            {t("app.title")}
          </Link>
          <LanguageToggle />
          <nav className={styles.secondaryNav} aria-label={t("app.moreLinks")}>
            <Link to="/programs">{t("app.programs")}</Link>
            <Link to="/about">{t("app.about")}</Link>
          </nav>
        </div>
      </header>

      <aside className={styles.disclaimer}>
        <p>{t("app.banner")}</p>
      </aside>

      <main className={styles.main}>
        <Stepper />
        <AppRoutes />
      </main>

      <footer className={styles.footer}>
        <nav className={styles.footerInner} aria-label={t("app.footerLinks")}>
          <Link to="/status">{t("app.status")}</Link>
          <Link to="/about">{t("app.about")}</Link>
        </nav>
      </footer>
    </div>
  );
}

export default function App() {
  return (
    <JourneyProvider>
      <LanguageProvider>
        <BrowserRouter>
          <AppLayout />
        </BrowserRouter>
      </LanguageProvider>
    </JourneyProvider>
  );
}
