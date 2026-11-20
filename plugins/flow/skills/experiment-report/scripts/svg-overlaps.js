// svg-overlaps.js: find collisions in every inline <svg> of a rendered page.
//
// Usage: open the page in the browser pane, then run this file's whole text with the browser's JavaScript tool
// (mcp__Claude_Browser__javascript_tool). It returns { figures, problems }: an empty problems list means no collisions.
// Check at desktop width; the figures scale with the column, so the result holds at other widths.
//
// What counts as a problem:
//   - text overlapping other text;
//   - text crossing the edge of a box, a dot or a polygon (text fully inside a box is a label in its box, which is fine);
//   - a line, an arrow, a bracket or any other path passing through text;
//   - text reaching outside the drawing, where the SVG clips it.
// Text boxes are trimmed by 15% top and bottom, since a font's ascent and descent rarely hold ink; two stacked
// lines of 11.5px text 14 units apart therefore do not count as touching.
(() => {
  const TOL = 0.5;         // px of overlap ignored
  const TRIM = 0.15;       // share of a text box's height trimmed from its top and bottom
  const SAMPLE_PX = 2;     // spacing of the points sampled along lines and paths, in screen px
  const shapeTags = new Set(['rect', 'circle', 'ellipse', 'polygon', 'line', 'polyline', 'path']);
  const boxTags = new Set(['rect', 'circle', 'ellipse', 'polygon']);
  const skipParents = 'defs, marker, clipPath, mask, pattern, symbol';

  const intersects = (a, b) =>
    a.left < b.right - TOL && b.left < a.right - TOL && a.top < b.bottom - TOL && b.top < a.bottom - TOL;
  const contains = (outer, inner) =>
    inner.left >= outer.left - TOL && inner.right <= outer.right + TOL &&
    inner.top >= outer.top - TOL && inner.bottom <= outer.bottom + TOL;
  const describe = el => {
    const cls = el.getAttribute('class');
    const txt = el.tagName === 'text' ? ` "${el.textContent.trim().slice(0, 40)}"` : '';
    return `${el.tagName}${cls ? '.' + cls.trim().split(/\s+/).join('.') : ''}${txt}`;
  };
  const visible = el => {
    const s = getComputedStyle(el);
    return s.display !== 'none' && s.visibility !== 'hidden' && Number(s.opacity) > 0;
  };

  const problems = [];
  const svgs = [...document.querySelectorAll('svg')].filter(svg => !svg.parentElement.closest('svg'));
  svgs.forEach((svg, i) => {
    const figure = svg.getAttribute('aria-label') || `svg #${i + 1}`;
    const frame = svg.getBoundingClientRect();
    if (frame.width === 0 || frame.height === 0) {
      problems.push({ figure, issue: 'figure not rendered (zero size)' });
      return;
    }
    const texts = [...svg.querySelectorAll('text')]
      .filter(t => t.textContent.trim() && visible(t) && !t.closest(skipParents))
      .map(t => {
        const r = t.getBoundingClientRect();
        const trim = r.height * TRIM;
        return { el: t, raw: r, r: { left: r.left, right: r.right, top: r.top + trim, bottom: r.bottom - trim } };
      });
    const shapes = [...svg.querySelectorAll([...shapeTags].join(','))]
      .filter(s => visible(s) && !s.closest(skipParents));

    texts.forEach(t => {
      if (!contains(frame, t.raw)) problems.push({ figure, issue: 'text outside the drawing (clipped)', a: describe(t.el) });
    });

    for (let a = 0; a < texts.length; a++)
      for (let b = a + 1; b < texts.length; b++)
        if (intersects(texts[a].r, texts[b].r))
          problems.push({ figure, issue: 'text overlaps text', a: describe(texts[a].el), b: describe(texts[b].el) });

    shapes.forEach(s => {
      const box = s.getBoundingClientRect();
      if (boxTags.has(s.tagName)) {
        texts.forEach(t => {
          if (intersects(t.r, box) && !contains(box, t.r))
            problems.push({ figure, issue: 'text crosses the edge of a shape', a: describe(t.el), b: describe(s) });
        });
        return;
      }
      // lines, polylines and paths: sample points along the stroke and test them against each text box
      const near = texts.filter(t => intersects(t.r, { left: box.left - 2, right: box.right + 2, top: box.top - 2, bottom: box.bottom + 2 }));
      if (!near.length || typeof s.getTotalLength !== 'function') return;
      const m = s.getScreenCTM();
      if (!m) return;
      const len = s.getTotalLength();
      const scale = Math.hypot(m.a, m.b) || 1;
      const n = Math.min(2000, Math.max(2, Math.ceil((len * scale) / SAMPLE_PX)));
      const hit = new Set();
      for (let k = 0; k <= n; k++) {
        const p = s.getPointAtLength((len * k) / n);
        const x = m.a * p.x + m.c * p.y + m.e;
        const y = m.b * p.x + m.d * p.y + m.f;
        near.forEach((t, j) => {
          if (!hit.has(j) && x > t.r.left + TOL && x < t.r.right - TOL && y > t.r.top + TOL && y < t.r.bottom - TOL) hit.add(j);
        });
      }
      hit.forEach(j => problems.push({ figure, issue: 'line or path runs through text', a: describe(near[j].el), b: describe(s) }));
    });
  });
  return { figures: svgs.length, problems };
})();
