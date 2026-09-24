export type Language = "en" | "es";
type Messages = Record<string, string>;
type MessageModule = { default: Messages };

const appFiles = import.meta.glob<MessageModule>("../../app/i18n/*.json", {
  eager: true,
});
const featureFiles = import.meta.glob<MessageModule>(
  "../../features/*/i18n/*.json",
  { eager: true },
);

export function loadMessages(language: Language): Messages {
  const messages: Messages = {};

  for (const [path, file] of Object.entries(appFiles)) {
    if (path.endsWith(`/${language}.json`)) Object.assign(messages, file.default);
  }

  for (const [path, file] of Object.entries(featureFiles)) {
    const match = path.match(/features\/([^/]+)\/i18n\/(en|es)\.json$/);
    if (match?.[2] !== language) continue;

    for (const [key, value] of Object.entries(file.default)) {
      messages[`${match[1]}.${key}`] = value;
    }
  }

  return messages;
}
