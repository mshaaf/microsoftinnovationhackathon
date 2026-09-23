import styles from "./App.module.css";

export default function App() {
  return (
    <main className={styles.page}>
      <div className={styles.content}>
        <h1 className={styles.title}>Survivor Journey Navigator</h1>
        <p className={styles.description}>
          Clear information and next steps for disaster recovery.
        </p>
      </div>
    </main>
  );
}
