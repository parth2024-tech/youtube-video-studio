# Verifiable Data Sources & Audit Ledger

**Audit Completed:** October 12, 2026  
**Auditor:** Compliance Agent & Technical Auditor  
**Audit Standard:** Strict HTTP verification. Direct URLs were opened via automated GET requests. If a page was accessible (HTTP 200), exact sentences were copied verbatim. If a domain returned HTTP 403 (e.g. Gartner bot protection) or 404, it is explicitly marked **UNVERIFIED DIRECT HTTP (403 PAYWALL/BOTWALL)**.

---

### Fact-Check Table

| Claim / Statistic in Script | Original URL Attempted | HTTP Status Code | Direct Page Content / Verification Note | Verification Status | Script & Asset Treatment |
| :--- | :--- | :---: | :--- | :---: | :--- |
| **Klarna Public Statement:** Shutting down Salesforce, phasing out Workday to build in-house tools and simplify stack. | `https://www.salesforceben.com/klarna-salesforce-workday/` | **200 OK** | **Exact sentence copied verbatim from live page:**<br>“*There are large ongoing internal initiatives that are a combination of AI, standardization, and simplification. As an example, we just shut down Salesforce. Within a few weeks, we will shut down Workday. We are shutting down a lot of our SaaS providers, as we are able to consolidate.*” | **VERIFIED (Direct HTTP 200)** | Quoted accurately in Act 3 with subsequent nuance regarding human support escalation. |
| **Gartner \$234 Billion Exposure:** Up to \$234B in enterprise SaaS exposed to agentic arbitrage by 2030 (~20% of SaaS spend). | `https://www.gartner.com/en/newsroom/press-releases/2026-07-01-gartner-estimates-234-billion-in-enterprise-software-as-a-service-spending-at-risk`<br>and webinar `https://www.gartner.com/en/webinars/526711/saaspocalypse-234b-of-enterprise-apps-spending-will-be-exposed-to-agentic-arbitrage` | **403 Forbidden** (Cloudflare / Bot-block) | Direct HTTP GET blocked by Gartner anti-bot wall. Verified via Google Grounding Index summarizing Gartner's report *"SaaSpocalypse - \$234B of Enterprise Apps Spending Will be Exposed to Agentic Arbitrage"*. | **UNVERIFIED DIRECT HTTP (403 BLOCKED)** | Labeled strictly as **"Gartner estimate"** on thumbnail and in script; no claim of absolute verified fact. |
| **Gartner 62.7% CAGR:** Agentic AI software spending projected to grow 62.7% CAGR (2025–2030). | `https://www.gartner.com/en/information-technology/research` | **403 Forbidden** (Cloudflare / Bot-block) | Direct HTTP GET blocked by Gartner anti-bot wall. Verified in search summaries. | **UNVERIFIED DIRECT HTTP (403 BLOCKED)** | Labeled strictly as an **industry forecast / estimate**. |
| **Gartner >40% Project Cancellation Risk:** >40% of unmanaged agentic pilots canceled by end of 2027. | `https://www.gartner.com/en/information-technology/research` | **403 Forbidden** (Cloudflare / Bot-block) | Direct HTTP GET blocked by Gartner anti-bot wall. Verified in search summaries. | **UNVERIFIED DIRECT HTTP (403 BLOCKED)** | Labeled strictly as a **risk forecast / estimate**. |

---

### Chart & Diagram Provenance Audit

All chart graphics rendered in `output/saaspocalypse-ai-agents/charts/` were audited to comply with the zero-unverified-data rule:
1. **Scene 1 (SaaS Evolution Timeline):** Labeled prominently as **"ILLUSTRATIVE EXAMPLE (CONCEPTUAL TIMELINE)"**. Zero source names attached. All arbitrary revenue figures removed.
2. **Scene 2 (Gartner Disruption Share):** Visualizes the 20% exposure proportion. Labeled clearly: **"Gartner estimate"**.
3. **Scene 3 (Workflow Comparison):** Labeled prominently as **"ILLUSTRATIVE EXAMPLE"**. Zero source names attached. All made-up numbers (42ms, \$0.002, 10,000 seats, \$45-\$65/hr) completely removed. Displays only qualitative architectural flow steps.
4. **Scene 4 (Software Resilience Matrix):** Labeled prominently as **"ILLUSTRATIVE EXAMPLE (CONCEPTUAL MATRIX)"**. Zero source names attached. All made-up share numbers (85/45/15) removed.
