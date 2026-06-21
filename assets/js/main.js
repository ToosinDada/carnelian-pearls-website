/* ==========================================================================
   CarnelianPearls Tech - main.js
   Vanilla JS, no dependencies. Two jobs:
     1. Mobile navigation toggle (accessible).
     2. Contact form -> mailto composer (progressive enhancement).
   The site is fully usable with this file absent or blocked.
   ========================================================================== */
(function () {
  "use strict";

  /* -- 1. Mobile navigation ---------------------------------------------- */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("primary-nav");

  if (toggle && nav) {
    var closeNav = function () {
      toggle.setAttribute("aria-expanded", "false");
      nav.setAttribute("data-open", "false");
    };
    var openNav = function () {
      toggle.setAttribute("aria-expanded", "true");
      nav.setAttribute("data-open", "true");
    };

    toggle.addEventListener("click", function () {
      var expanded = toggle.getAttribute("aria-expanded") === "true";
      if (expanded) { closeNav(); } else { openNav(); }
    });

    /* Close on Escape and return focus to the toggle. */
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
        closeNav();
        toggle.focus();
      }
    });

    /* Close when a nav link is followed. */
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) { closeNav(); }
    });

    /* Reset state if resized up to desktop. */
    var mq = window.matchMedia("(min-width: 880px)");
    var handleMq = function () { if (mq.matches) { closeNav(); } };
    if (mq.addEventListener) { mq.addEventListener("change", handleMq); }
    else if (mq.addListener) { mq.addListener(handleMq); }
  }

  /* -- 2. Contact mailto composer ---------------------------------------- */
  var form = document.getElementById("contact-form");
  if (!form) { return; }

  /* Default address; the markup is the source of truth via data-email. */
  var EMAIL = form.getAttribute("data-email") || "info@carnelianandpearls.com";
  var status = document.getElementById("form-status");

  /* Map each category value to a tidy subject line. */
  var SUBJECTS = {
    partnership: "Partnership enquiry",
    venture: "Venture Studio enquiry",
    opportunity: "Opportunity enquiry",
    other: "General enquiry"
  };

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    var data = new FormData(form);
    var category = (data.get("category") || "other").toString();
    var name = (data.get("name") || "").toString().trim();
    var email = (data.get("email") || "").toString().trim();
    var company = (data.get("company") || "").toString().trim();
    var message = (data.get("message") || "").toString().trim();

    var subject = SUBJECTS[category] || "General enquiry";

    var lines = [];
    lines.push(message || "(No message entered.)");
    lines.push("");
    lines.push("----");
    if (name) { lines.push("Name: " + name); }
    if (email) { lines.push("Email: " + email); }
    if (company) { lines.push("Company: " + company); }
    lines.push("Enquiry type: " + subject);

    var href =
      "mailto:" + EMAIL +
      "?subject=" + encodeURIComponent(subject) +
      "&body=" + encodeURIComponent(lines.join("\n"));

    /* Trigger the visitor's own mail client. Nothing is sent anywhere else. */
    window.location.href = href;

    if (status) {
      status.textContent =
        "Opening your email app with the message ready to send. " +
        "If nothing happens, email " + EMAIL + " directly.";
    }
  });
})();
