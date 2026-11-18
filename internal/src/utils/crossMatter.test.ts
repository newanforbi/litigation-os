import { describe, expect, it } from "vitest";
import {
  CROSS_MATTER_CLUSTERS,
  allLinkKinds,
  authorityChain,
  clusterForMatter,
  exposuresForMatter,
  foundationForMatter,
  kindsBetween,
  linkDegree,
  linkKindLabel,
  linksBetween,
  openExposures,
  partiesForMatter,
  precedentPeers,
  relatedMatterNumbers,
  relatedMatters,
  relationshipFor,
} from "./crossMatter";
import { getMatterSummary } from "../data/matters";

const CLUSTER_MATTERS = [1, 2, 7, 20, 24, 32, 33];

describe("cross-matter graph integrity", () => {
  it("defines at least one cluster", () => {
    expect(CROSS_MATTER_CLUSTERS.length).toBeGreaterThan(0);
  });

  it("resolves every cluster matter to a real matter record", () => {
    for (const cluster of CROSS_MATTER_CLUSTERS) {
      for (const matter of cluster.matters) {
        expect(getMatterSummary(matter), `matter ${matter}`).toBeDefined();
      }
    }
  });

  it("keeps every link endpoint inside its cluster", () => {
    for (const cluster of CROSS_MATTER_CLUSTERS) {
      for (const link of cluster.links) {
        expect(cluster.matters).toContain(link.from);
        expect(cluster.matters).toContain(link.to);
        expect(link.from).not.toBe(link.to);
      }
    }
  });

  it("uses only declared link kinds", () => {
    const kinds = allLinkKinds();
    for (const cluster of CROSS_MATTER_CLUSTERS) {
      for (const link of cluster.links) {
        expect(link.kinds.length).toBeGreaterThan(0);
        for (const kind of link.kinds) expect(kinds).toContain(kind);
      }
    }
  });

  it("cites at least one source per link", () => {
    for (const cluster of CROSS_MATTER_CLUSTERS) {
      for (const link of cluster.links) {
        expect(link.sources.length, link.id).toBeGreaterThan(0);
        expect(link.significance.length).toBeGreaterThan(40);
      }
    }
  });

  it("uses unique link ids", () => {
    for (const cluster of CROSS_MATTER_CLUSTERS) {
      const ids = cluster.links.map((link) => link.id);
      expect(new Set(ids).size).toBe(ids.length);
    }
  });

  it("gives every exposure a remedy and in-cluster matters", () => {
    for (const cluster of CROSS_MATTER_CLUSTERS) {
      for (const exposure of cluster.exposures) {
        expect(exposure.remedy.length, exposure.id).toBeGreaterThan(20);
        expect(exposure.matters.length).toBeGreaterThan(0);
        for (const matter of exposure.matters) expect(cluster.matters).toContain(matter);
      }
    }
  });

  it("scopes foundation items and parties to cluster matters", () => {
    for (const cluster of CROSS_MATTER_CLUSTERS) {
      for (const item of cluster.foundation) {
        for (const matter of item.matters) expect(cluster.matters).toContain(matter);
      }
      for (const party of cluster.parties) {
        for (const matter of [...party.defendantIn, ...party.factualIn]) {
          expect(cluster.matters).toContain(matter);
        }
      }
    }
  });

  it("leaves no cluster matter unlinked", () => {
    for (const cluster of CROSS_MATTER_CLUSTERS) {
      for (const matter of cluster.matters) {
        expect(linkDegree(matter), `matter ${matter} degree`).toBeGreaterThan(0);
      }
    }
  });
});

describe("clusterForMatter", () => {
  it("finds the CHP cluster for each member matter", () => {
    for (const matter of CLUSTER_MATTERS) {
      expect(clusterForMatter(matter)?.id).toBe("chp-nov2024");
    }
  });

  it("returns undefined for a matter outside any cluster", () => {
    expect(clusterForMatter(9999)).toBeUndefined();
  });

  it("places the UPS docket in the §290.46 employment cluster", () => {
    expect(clusterForMatter(26)?.id).toBe("megan-law-employment");
    expect(kindsBetween(26, 27)).toContain("same_statute");
    expect(precedentPeers(26)).toEqual([22, 25, 27, 29, 42, 44]);
  });
});

describe("relatedMatters", () => {
  it("ties Matter 1 to the six other cluster matters", () => {
    // High-severity peers first (2, 7, 20, 32, 33), then medium (24)
    expect(relatedMatterNumbers(1)).toEqual([2, 7, 20, 32, 33, 24]);
  });

  it("never returns the matter itself", () => {
    for (const matter of CLUSTER_MATTERS) {
      expect(relatedMatterNumbers(matter)).not.toContain(matter);
    }
  });

  it("collapses multiple links to one entry per peer", () => {
    const entry = relatedMatters(1).find((item) => item.number === 2);
    expect(entry).toBeDefined();
    expect(entry!.kinds).toContain("stay_dependency");
    expect(entry!.kinds).toContain("damages_overlap");
  });

  it("orders high-severity peers first", () => {
    const severities = relatedMatters(1).map((item) => item.severity);
    expect(severities.indexOf("high")).toBeLessThan(severities.lastIndexOf("medium"));
  });

  it("is symmetric: every peer lists the matter back", () => {
    for (const matter of CLUSTER_MATTERS) {
      for (const peer of relatedMatterNumbers(matter)) {
        expect(relatedMatterNumbers(peer)).toContain(matter);
      }
    }
  });

  it("returns nothing for an unclustered matter", () => {
    expect(relatedMatters(9999)).toEqual([]);
  });
});

describe("relationshipFor", () => {
  const stay = linksBetween(2, 1).find((link) => link.kinds.includes("stay_dependency"))!;

  it("reads a dependency from the dependent side", () => {
    expect(relationshipFor(stay, 2)).toBe("This matter depends on Matter 1");
  });

  it("reads the same dependency from the controlling side", () => {
    expect(relationshipFor(stay, 1)).toBe("Matter 2 depends on this matter");
  });

  it("reads citation direction from the citing side", () => {
    const cite = linksBetween(24, 1).find((link) => link.kinds.includes("persuasive_authority"))!;
    expect(relationshipFor(cite, 1)).toBe("This matter cites Matter 24");
    expect(relationshipFor(cite, 24)).toBe("Matter 1 cites this matter");
  });

  it("labels mutual links reciprocally from both sides", () => {
    const overlap = linksBetween(1, 20).find((link) => link.kinds.includes("damages_overlap"))!;
    expect(relationshipFor(overlap, 1)).toBe("Reciprocal with Matter 20");
    expect(relationshipFor(overlap, 20)).toBe("Reciprocal with Matter 1");
  });
});

describe("kindsBetween", () => {
  it("reports the same kinds regardless of argument order", () => {
    expect(kindsBetween(20, 24).sort()).toEqual(kindsBetween(24, 20).sort());
  });

  it("records the related-case disclosure gap between 24 and 20", () => {
    expect(kindsBetween(24, 20)).toContain("disclosure_gap");
  });

  it("returns an empty list for unrelated pairs", () => {
    expect(kindsBetween(1, 9999)).toEqual([]);
  });
});

describe("exposures, foundation, parties", () => {
  it("flags the unreserved CDL damages exposure on all four damages matters", () => {
    for (const matter of [1, 2, 7, 20]) {
      const ids = exposuresForMatter(matter).map((exposure) => exposure.id);
      expect(ids, `matter ${matter}`).toContain("cdl-double-recovery");
    }
  });

  it("excludes resolved exposures from the open list", () => {
    const cluster = clusterForMatter(1)!;
    expect(openExposures(cluster).every((exposure) => exposure.status !== "resolved")).toBe(true);
  });

  it("shares the dashcam and Detention Certificate across every cluster matter", () => {
    for (const matter of CLUSTER_MATTERS) {
      const ids = foundationForMatter(matter).map((item) => item.id);
      expect(ids, `matter ${matter}`).toContain("dashcam");
      expect(ids).toContain("detention-certificate");
    }
  });

  it("lists the CHP officers as parties to the state-court matters", () => {
    const names = partiesForMatter(2).map((party) => party.name);
    expect(names.some((name) => name.includes("Meza-Gonzalez"))).toBe(true);
  });
});

describe("authorityChain", () => {
  it("collects only authority-bearing links", () => {
    const cluster = clusterForMatter(1)!;
    const chain = authorityChain(cluster);
    expect(chain.length).toBeGreaterThan(2);
    expect(
      chain.every((link) =>
        link.kinds.some((kind) =>
          ["authority_dependency", "persuasive_authority", "stay_dependency"].includes(kind),
        ),
      ),
    ).toBe(true);
  });
});

describe("linkKindLabel", () => {
  it("returns readable labels for declared kinds", () => {
    expect(linkKindLabel("damages_overlap")).toBe("Overlapping damages claim");
  });

  it("falls back to the raw key for unknown kinds", () => {
    expect(linkKindLabel("not_a_kind")).toBe("not_a_kind");
  });
});
