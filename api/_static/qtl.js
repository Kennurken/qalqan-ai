// Qalqan tool-page localization (kk/ru). Shares the `qlang` localStorage key
// with the landing, so the language follows the user across the whole product.
// Usage: QTL.mount(DICT, onChange?) — DICT = {kk:{key:html}, ru:{key:html}}.
// Static markup opts in via data-qtl="key" (innerHTML) / data-qtl-ph="key"
// (placeholder). Runtime strings: QTL.t(DICT,'key').
window.QTL = (function () {
  "use strict";
  let L = localStorage.getItem("qlang") || "kk";
  if (L !== "kk") L = "ru";              // en visitors get ru on tool pages

  const css = document.createElement("style");
  css.textContent =
    ".qlangsw{display:inline-flex;border:1px solid var(--bd,#1e293b);border-radius:9px;overflow:hidden;vertical-align:middle;margin-right:6px}" +
    ".qlangsw button{background:none;border:none;color:var(--mut,#7d8aa0);font:700 11.5px/1 inherit;font-family:inherit;padding:9px 11px;cursor:pointer}" +
    ".qlangsw button.on{background:var(--cyan,#7aa2f7);color:#04121a}";
  document.documentElement.appendChild(css);

  function apply(dict) {
    const d = dict[L] || {};
    document.querySelectorAll("[data-qtl]").forEach((el) => {
      const v = d[el.dataset.qtl];
      if (v != null) el.innerHTML = v;
    });
    document.querySelectorAll("[data-qtl-ph]").forEach((el) => {
      const v = d[el.dataset.qtlPh];
      if (v != null) el.placeholder = v;
    });
    document.documentElement.lang = L;
  }

  function mount(dict, onChange) {
    const anchor = document.getElementById("qtgl");
    const w = document.createElement("div");
    w.className = "qlangsw";
    w.setAttribute("role", "group");
    w.setAttribute("aria-label", "Тіл / Язык");
    w.innerHTML = '<button data-l="kk">ҚАЗ</button><button data-l="ru">РУС</button>';
    if (anchor) anchor.parentNode.insertBefore(w, anchor);
    else document.body.appendChild(w);
    const sync = () => {
      w.querySelectorAll("button").forEach((b) => b.classList.toggle("on", b.dataset.l === L));
      apply(dict);
      if (onChange) onChange(L);
    };
    w.querySelectorAll("button").forEach((b) => (b.onclick = () => {
      L = b.dataset.l;
      localStorage.setItem("qlang", L);
      sync();
    }));
    sync();
  }

  return { mount, t: (dict, k) => (dict[L] || {})[k] || (dict.ru || {})[k] || "", get L() { return L; } };
})();
