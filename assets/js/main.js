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

  /* -- 1b. "What we do" dropdown (desktop) -------------------------------- */
  var triggers = document.querySelectorAll(".nav__trigger");
  var closeAll = function (except) {
    Array.prototype.forEach.call(triggers, function (t) {
      if (t !== except) { t.setAttribute("aria-expanded", "false"); }
    });
  };
  Array.prototype.forEach.call(triggers, function (t) {
    var menu = document.getElementById(t.getAttribute("aria-controls"));
    var links = function () { return menu ? menu.querySelectorAll("a") : []; };

    t.addEventListener("click", function () {
      var open = t.getAttribute("aria-expanded") === "true";
      closeAll(t);
      t.setAttribute("aria-expanded", open ? "false" : "true");
    });

    /* Arrow down opens the menu and moves into it. */
    t.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown") {
        e.preventDefault();
        t.setAttribute("aria-expanded", "true");
        if (links()[0]) { links()[0].focus(); }
      }
    });

    if (menu) {
      /* Arrow keys move between items; Escape closes and returns to the trigger. */
      menu.addEventListener("keydown", function (e) {
        var items = Array.prototype.slice.call(links());
        var i = items.indexOf(document.activeElement);
        if (e.key === "ArrowDown" || e.key === "ArrowUp") {
          e.preventDefault();
          var next = e.key === "ArrowDown" ? i + 1 : i - 1;
          if (items[(next + items.length) % items.length]) { items[(next + items.length) % items.length].focus(); }
        } else if (e.key === "Escape") {
          t.setAttribute("aria-expanded", "false");
          t.focus();
        }
      });
      /* Close once focus leaves the whole group (e.g. tabbing past it). */
      t.parentNode.addEventListener("focusout", function (e) {
        if (!t.parentNode.contains(e.relatedTarget)) { t.setAttribute("aria-expanded", "false"); }
      });
    }
  });
  if (triggers.length) {
    document.addEventListener("click", function (e) {
      if (!e.target.closest(".nav__group")) { closeAll(null); }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") {
        var open = document.querySelector('.nav__trigger[aria-expanded="true"]');
        if (open) { open.setAttribute("aria-expanded", "false"); open.focus(); }
      }
    });
  }

  /* -- 2. Contact mailto composer ---------------------------------------- */
  var form = document.getElementById("contact-form");
  if (!form) { return; }

  /* Default address; the markup is the source of truth via data-email. */
  var EMAIL = form.getAttribute("data-email") || "info@carnelianandpearls.com";
  var status = document.getElementById("form-status");

  /* Preselect the category from ?topic=... (set by calls to action on other pages). */
  try {
    var topic = new URLSearchParams(window.location.search).get("topic");
    var sel = form.querySelector('select[name="category"]');
    if (topic && sel && sel.querySelector('option[value="' + topic + '"]')) { sel.value = topic; }
  } catch (e) { /* older browsers: leave the default */ }

  /* Map each category value to a tidy subject line. */
  var SUBJECTS = {
    consulting: "Consulting enquiry",
    partnership: "Partnership enquiry",
    venture: "Venture Studio enquiry",
    academy: "Academy enquiry",
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

    /* An <option data-email="..."> sends that category to its own inbox
       (consulting goes to Tosin directly); everything else uses EMAIL. */
    var picked = form.querySelector('option[value="' + category + '"]');
    var to = (picked && picked.getAttribute("data-email")) || EMAIL;

    var lines = [];
    lines.push(message || "(No message entered.)");
    lines.push("");
    lines.push("----");
    if (name) { lines.push("Name: " + name); }
    if (email) { lines.push("Email: " + email); }
    if (company) { lines.push("Company: " + company); }
    lines.push("Enquiry type: " + subject);

    var href =
      "mailto:" + to +
      "?subject=" + encodeURIComponent(subject) +
      "&body=" + encodeURIComponent(lines.join("\n"));

    /* Trigger the visitor's own mail client. Nothing is sent anywhere else. */
    window.location.href = href;

    if (status) {
      status.textContent =
        "Opening your email app with the message ready to send. " +
        "If nothing happens, email " + to + " directly.";
    }
  });
})();
