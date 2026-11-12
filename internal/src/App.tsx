import { lazy, Suspense, useCallback } from "react";
import { Navigate, Route, Routes, useNavigate } from "react-router";
import { Analytics } from "@vercel/analytics/react";
import { SpeedInsights } from "@vercel/speed-insights/react";
import { ShellLayout } from "./components/layout/ShellLayout";
import { RouteLoading } from "./components/ui/AsyncState";
import { usePortfolioUI } from "./context/PortfolioUIContext";
import { ROUTES } from "./routes";

const DashboardTab = lazy(() => import("./components/DashboardTab").then((m) => ({ default: m.DashboardTab })));
const CensusRoute = lazy(() => import("./pages/CensusRoute"));
const MattersRoute = lazy(() => import("./pages/MattersRoute"));
const TimelineTab = lazy(() => import("./components/TimelineTab").then((m) => ({ default: m.TimelineTab })));
const DamagesTab = lazy(() => import("./components/DamagesTab").then((m) => ({ default: m.DamagesTab })));
const DamagesLeverageTab = lazy(() => import("./components/DamagesLeverageTab").then((m) => ({ default: m.DamagesLeverageTab })));
const TheoriesTab = lazy(() => import("./components/TheoriesTab").then((m) => ({ default: m.TheoriesTab })));
const CostOfCounselTab = lazy(() => import("./components/CostOfCounselTab").then((m) => ({ default: m.CostOfCounselTab })));
const OutcomesTab = lazy(() => import("./components/OutcomesTab").then((m) => ({ default: m.OutcomesTab })));
const JudicialOpinionsTab = lazy(() => import("./components/JudicialOpinionsTab").then((m) => ({ default: m.JudicialOpinionsTab })));
const NotableQuotesTab = lazy(() => import("./components/NotableQuotesTab").then((m) => ({ default: m.NotableQuotesTab })));
const MatterDetailPage = lazy(() => import("./pages/MatterDetailPage").then((m) => ({ default: m.MatterDetailPage })));

const noop = () => undefined;

function DashboardRoute() {
  const navigate = useNavigate();
  // Stable identities so DashboardTab can bail out on unrelated shell re-renders.
  const setClusterFilter = useCallback((cluster: number) => navigate(`${ROUTES.matters}?cluster=${cluster}`), [navigate]);
  return <DashboardTab setClusterFilter={setClusterFilter} setActiveTab={noop} />;
}

function TimelineRoute() {
  const ui = usePortfolioUI();
  return <TimelineTab showPastEvents={ui.showPastEvents} setShowPastEvents={ui.setShowPastEvents} />;
}

function DamagesRoute() {
  const ui = usePortfolioUI();
  return <DamagesTab damagesView={ui.damagesView} setDamagesView={ui.setDamagesView} />;
}

export default function App() {
  return (
    <>
      <Suspense fallback={<RouteLoading label="Loading portfolio section" />}>
        <Routes>
          <Route element={<ShellLayout />}>
            <Route index element={<DashboardRoute />} />
            <Route path="census" element={<CensusRoute />} />
            <Route path="calendar" element={<Navigate to={ROUTES.timeline} replace />} />
            <Route path="matters" element={<MattersRoute />} />
            <Route path="matters/:matterNumber" element={<MatterDetailPage />} />
            <Route path="timeline" element={<TimelineRoute />} />
            <Route path="deadlines" element={<Navigate to={ROUTES.dashboard} replace />} />
            <Route path="cross-matter" element={<Navigate to={ROUTES.dashboard} replace />} />
            <Route path="damages" element={<DamagesRoute />} />
            <Route path="damages/leverage" element={<DamagesLeverageTab />} />
            <Route path="theories" element={<TheoriesTab />} />
            <Route path="cost-of-counsel" element={<CostOfCounselTab />} />
            <Route path="outcomes" element={<OutcomesTab />} />
            <Route path="judicial-opinions" element={<JudicialOpinionsTab />} />
            <Route path="notable-quotes" element={<NotableQuotesTab />} />
            <Route path="*" element={<Navigate to={ROUTES.dashboard} replace />} />
          </Route>
        </Routes>
      </Suspense>
      <Analytics />
      <SpeedInsights />
    </>
  );
}
