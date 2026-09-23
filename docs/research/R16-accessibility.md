# R16: Accessibility essentials

## Answer
- Axe in Playwright: `pnpm add -D @axe-core/playwright`
```ts
import AxeBuilder from '@axe-core/playwright';
const r = await new AxeBuilder({ page }).withTags(['wcag2a','wcag2aa','wcag21aa','wcag22aa']).analyze();
const bad = r.violations.filter(v => ['critical','serious'].includes(v.impact ?? ''));
```
Warn-only until Phase 3, then `expect(bad).toEqual([])`.
- WCAG 2.2 AA items that matter for this app: **2.5.8** target size (AA minimum is 24px; we use 44px), **2.4.11** focus not obscured (the sticky banner must not cover the focused control), **2.4.7** visible focus, **3.3.7** redundant entry (don't re-ask ZIP or answers across stages; keep them in memory state), **1.4.3** contrast 4.5:1, **3.3.1/3.3.3** errors named in text plus a fix hint, **1.1.1** alt text for letter previews, **4.1.2** labels on every control.
- Also: `lang` attribute switches to `es` on toggle, headings in order, one `h1` per screen, and `aria-live="polite"` for letter progress.
- Reading level: spot-check with `uvx textstat`-style Flesch-Kincaid, or paste into https://hemingwayapp.com. Target grade 6–8. Log the results in P3-03.
- Plain language: https://www.plainlanguage.gov/guidelines/

## Impact
P0-08, P3-03.
