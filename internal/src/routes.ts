export const ROUTES = {
  dashboard: "/",
  census: "/census",
  matters: "/matters",
  timeline: "/timeline",
  damages: "/damages",
  damagesLeverage: "/damages/leverage",
  theories: "/theories",
  costOfCounsel: "/cost-of-counsel",
  outcomes: "/outcomes",
  judicialOpinions: "/judicial-opinions",
  notableQuotes: "/notable-quotes",
} as const;

export const NAV_ITEMS = [
  { label: "Dashboard", path: ROUTES.dashboard, end: true, icon: "⌂", group: "Overview" },
  { label: "Matters", path: ROUTES.matters, end: false, icon: "§", group: "Casework" },
  { label: "Timeline", path: ROUTES.timeline, end: false, icon: "↦", group: "Casework" },
  { label: "Damages", path: ROUTES.damages, end: false, icon: "$", group: "Analysis" },
  { label: "Theories", path: ROUTES.theories, end: false, icon: "¶", group: "Analysis" },
  { label: "Cost of Counsel", path: ROUTES.costOfCounsel, end: false, icon: "◈", group: "Analysis" },
  { label: "Outcomes", path: ROUTES.outcomes, end: false, icon: "✓", group: "Analysis" },
  { label: "Judicial Opinions", path: ROUTES.judicialOpinions, end: false, icon: "⚖", group: "Record" },
  { label: "Notable Quotes", path: ROUTES.notableQuotes, end: false, icon: "“", group: "Record" },
] as const;

export const routeForTab = (tab: string) =>
  NAV_ITEMS.find((item) => item.label === tab)?.path ?? ROUTES.dashboard;
