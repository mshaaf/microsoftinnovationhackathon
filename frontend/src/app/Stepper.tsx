import { Link, useLocation } from "react-router";
import { useT } from "./LanguageContext";
import styles from "./Stepper.module.css";

const stages = [
  { path: "/help-here", label: "app.step.helpHere" },
  { path: "/apply", label: "app.step.apply" },
  { path: "/letter", label: "app.step.letter" },
  { path: "/deadline", label: "app.step.deadline" },
] as const;

export function Stepper() {
  const { pathname } = useLocation();
  const t = useT();
  const currentPath = pathname === "/" ? "/help-here" : pathname;

  return (
    <nav className={styles.navigation} aria-label={t("app.stepsLabel")}>
      <ol className={styles.steps}>
        {stages.map((stage, index) => (
          <li className={styles.item} key={stage.path}>
            <Link
              aria-current={currentPath === stage.path ? "step" : undefined}
              className={styles.step}
              to={stage.path}
            >
              <span className={styles.number}>{index + 1}</span>
              <span className={styles.label}>{t(stage.label)}</span>
            </Link>
          </li>
        ))}
      </ol>
    </nav>
  );
}
