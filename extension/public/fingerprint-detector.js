// клауд Елдоса N1 — Qalqan AI v5.0
// Browser Fingerprint Detection — warns if site collects fingerprints
// Injected as content script, monitors suspicious API calls

(function() {
  const detected = [];

  // Monitor Canvas fingerprinting
  const origToDataURL = HTMLCanvasElement.prototype.toDataURL;
  HTMLCanvasElement.prototype.toDataURL = function(...args) {
    if (this.width > 0 && this.height > 0) {
      detected.push("canvas_fingerprint");
    }
    return origToDataURL.apply(this, args);
  };

  // Monitor WebGL fingerprinting
  const origGetParameter = WebGLRenderingContext.prototype.getParameter;
  WebGLRenderingContext.prototype.getParameter = function(param) {
    if (param === 37445 || param === 37446) { // RENDERER, VENDOR
      detected.push("webgl_fingerprint");
    }
    return origGetParameter.apply(this, arguments);
  };

  // Monitor AudioContext fingerprinting
  if (window.AudioContext || window.webkitAudioContext) {
    const OrigAC = window.AudioContext || window.webkitAudioContext;
    window.AudioContext = window.webkitAudioContext = function(...args) {
      detected.push("audio_fingerprint");
      return new OrigAC(...args);
    };
  }

  // Report after page load
  setTimeout(() => {
    if (detected.length > 0) {
      const unique = [...new Set(detected)];
      chrome.runtime.sendMessage({
        action: "FINGERPRINT_DETECTED",
        types: unique,
        url: window.location.href
      });
    }
  }, 3000);
})();
