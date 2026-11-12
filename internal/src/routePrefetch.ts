import { ROUTES } from "./routes";

// Route chunks only start downloading when the route mounts, so a click pays the
// full fetch before anything renders. Hovering or focusing a nav link is a strong
// enough signal to start early — by the time the click lands the chunk is usually
// there. Import paths are string literals so the bundler can still see them.
const LOADERS: Record<string, () => Promise<unknown>> = {
  [ROUTES.dashboard]: () => import("./components/DashboardTab"),
  [ROUTES.census]: () => import("./pages/CensusRoute"),
  [ROUTES.matters]: () => import("./pages/MattersRoute"),
  [ROUTES.timeline]: () => import("./components/TimelineTab"),
  [ROUTES.damages]: () => import("./components/DamagesTab"),
  [ROUTES.damagesLeverage]: () => import("./components/DamagesLeverageTab"),
  [ROUTES.theories]: () => import("./components/TheoriesTab"),
  [ROUTES.costOfCounsel]: () => import("./components/CostOfCounselTab"),
  [ROUTES.outcomes]: () => import("./components/OutcomesTab"),
  [ROUTES.judicialOpinions]: () => import("./components/JudicialOpinionsTab"),
  [ROUTES.notableQuotes]: () => import("./components/NotableQuotesTab"),
};

/** Paths that have a chunk to warm. Exported so a test can assert the map keeps
 *  up with ROUTES — a renamed route would otherwise stop prefetching in silence. */
export const PREFETCHABLE_ROUTES = Object.keys(LOADERS);

const started = new Set<string>();

/** Warm a route's chunk. Safe to call repeatedly — each route is fetched once,
 *  and a failure is swallowed so a prefetch never breaks navigation. */
export function prefetchRoute(path: string) {
  if (started.has(path)) return;
  const load = LOADERS[path];
  if (!load) return;
  started.add(path);
  load().catch(() => started.delete(path));
}

/** The search dialog is the largest lazy chunk in the app, and ⌘K expects it to
 *  be instant. Warmed when the trigger is hovered or focused. */
export function prefetchSearch() {
  if (started.has("search")) return;
  started.add("search");
  import("./components/search/GlobalSearchDialog").catch(() => started.delete("search"));
}
