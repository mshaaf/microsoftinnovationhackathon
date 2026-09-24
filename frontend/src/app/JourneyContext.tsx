import { createContext, useContext, useMemo, useState } from "react";
import type { PropsWithChildren } from "react";

export type JourneyState = {
  zipCode: string;
  county: string;
  answers: Record<string, string>;
  disasterNumber: string;
};

type JourneyContextValue = {
  journey: JourneyState;
  updateJourney: (changes: Partial<JourneyState>) => void;
};

const initialJourney: JourneyState = {
  zipCode: "",
  county: "",
  answers: {},
  disasterNumber: "",
};

const JourneyContext = createContext<JourneyContextValue | null>(null);

export function JourneyProvider({ children }: PropsWithChildren) {
  const [journey, setJourney] = useState(initialJourney);
  const value = useMemo(
    () => ({
      journey,
      updateJourney: (changes: Partial<JourneyState>) =>
        setJourney((current) => ({ ...current, ...changes })),
    }),
    [journey],
  );

  return (
    <JourneyContext.Provider value={value}>{children}</JourneyContext.Provider>
  );
}

export function useJourney() {
  const context = useContext(JourneyContext);
  if (!context) throw new Error("useJourney must be used inside JourneyProvider");
  return context;
}
