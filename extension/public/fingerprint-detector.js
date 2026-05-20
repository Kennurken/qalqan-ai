// Qalqan AI v5.0
// Browser Fingerprint Detection — warns if site collects fingerprints
// Injected as content script, monitors suspicious API calls

(function() {
  "use strict";
  const detected = new Set();
  const THRESHOLD = 2;  // Need 2+ unique types before reporting (reduces false positives)

  // --- Canvas fingerprinting ---
  const origToDataURL = HTMLCanvasElement.prototype.toDataURL;
  HTMLCanvasElement.prototype.toDataURL = function(...args) {
    if (this.width > 16 && this.height > 16) {  // Skip tiny canvases (icons, etc.)
      detected.add("canvas_fingerprint");
    }
    return origToDataURL.apply(this, args);
  };
  const origGetImageData = CanvasRenderingContext2D.prototype.getImageData;
  CanvasRenderingContext2D.prototype.getImageData = function(...args) {
    detected.add("canvas_fingerprint");
    return origGetImageData.apply(this, args);
  };

  // --- WebGL fingerprinting ---
  const patchWebGL = (ctx) => {
    const orig = ctx.prototype.getParameter;
    ctx.prototype.getParameter = function(param) {
      // RENDERER(37446), VENDOR(37445), UNMASKED_RENDERER(37446+), UNMASKED_VENDOR(37445+)
      if (param === 37445 || param === 37446 || param === 33901 || param === 33902) {
        detected.add("webgl_fingerprint");
      }
      return orig.apply(this, arguments);
    };
  };
  if (window.WebGLRenderingContext) patchWebGL(WebGLRenderingContext);
  if (window.WebGL2RenderingContext) patchWebGL(WebGL2RenderingContext);

  // --- AudioContext fingerprinting ---
  const patchAudio = (AC) => {
    const orig = AC;
    window[AC.name] = function(...args) {
      detected.add("audio_fingerprint");
      return new orig(...args);
    };
    Object.setPrototypeOf(window[AC.name], orig);
  };
  if (window.AudioContext) patchAudio(AudioContext);
  if (window.webkitAudioContext) patchAudio(webkitAudioContext);

  // --- Font enumeration fingerprinting (document.fonts API) ---
  if (document.fonts && document.fonts.check) {
    const origCheck = document.fonts.check.bind(document.fonts);
    let fontCheckCount = 0;
    document.fonts.check = function(...args) {
      fontCheckCount++;
      if (fontCheckCount > 10) {  // Bulk font checking = fingerprinting
        detected.add("font_fingerprint");
      }
      return origCheck(...args);
    };
  }

  // --- Navigator property harvesting (battery, connection, etc.) ---
  if (navigator.getBattery) {
    const orig = navigator.getBattery.bind(navigator);
    navigator.getBattery = function() {
      detected.add("battery_fingerprint");
      return orig();
    };
  }

  // --- Screen properties access fingerprinting (monitor multiple reads) ---
  let screenAccessCount = 0;
  const screenProps = ["availWidth", "availHeight", "colorDepth", "pixelDepth"];
  screenProps.forEach(prop => {
    const desc = Object.getOwnPropertyDescriptor(Screen.prototype, prop);
    if (desc && desc.get) {
      Object.defineProperty(Screen.prototype, prop, {
        get: function() {
          screenAccessCount++;
          if (screenAccessCount > 8) detected.add("screen_fingerprint");
          return desc.get.call(this);
        }, configurable: true
      });
    }
  });

  // --- Report after page settles ---
  setTimeout(() => {
    const unique = [...detected];
    if (unique.length >= THRESHOLD) {
      try {
        chrome.runtime.sendMessage({
          action: "FINGERPRINT_DETECTED",
          types: unique,
          url: window.location.href,
          count: unique.length
        });
      } catch {}  // Extension context may be invalidated
    }
  }, 4000);
})();
