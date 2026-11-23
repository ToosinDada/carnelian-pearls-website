---
title: 'AI can draft your user stories. Someone still has to check them.'
date: 2026-11-23
summary: 'Generative AI can produce delivery artefacts fast, but fast is not the same as right. On an agentic AI proof of concept, a human-in-the-loop quality gate cut invalid stories by about 75% across four iterations.'
minutes: 4
draft: false
---

Generative AI is very good at producing user stories that look right. They have the familiar shape: a role, a need, a benefit, a list of acceptance criteria. Read quickly, they pass. That is exactly the problem. A plausible story that does not match the agreed process, misses a requirement, or describes something the platform will not do is worse than no story, because it carries its error into build looking finished.

## Put a gate between the AI and the backlog

On an AI-driven ITSM proof of concept, I was the lead business and process owner. We used AI to generate delivery artefacts, and I designed a human-in-the-loop validation layer between that output and the ServiceNow build. Nothing the AI produced went into the build backlog until it had been reviewed against delivery standards.

That checkpoint did two things. It stopped invalid stories from reaching build. And because every review was recorded, it created an auditable record of what was accepted, what was rejected and why.

## Fix the inputs, not just the outputs

The most useful lesson was that the quality of AI output depends heavily on what goes in. Rejecting bad stories one at a time does not scale. So alongside reviewing the output, I owned the inputs: the process descriptions the AI worked from, the requirement templates, and the validation artefacts we reviewed against.

Each time a pattern of errors showed up in review, we traced it back to an input that was ambiguous, incomplete or missing, and fixed that. Across four iterations, invalid user stories fell by approximately 75%.

<!-- [Tosin: if you can, add one concrete example of the kind of error the gate caught, described generically.] -->

## What this means for delivery teams

  - **Treat AI output as a draft, always.** Its speed is real, but someone accountable still has to own what goes into build.
  - **Make the review auditable.** A recorded quality gate is what lets you defend AI-assisted delivery to clients and auditors.
  - **Invest in the inputs.** Clear process descriptions and good templates improve every story the AI produces, not just the one you are fixing.

Used this way, AI and agentic tooling such as Now Assist can genuinely speed up delivery. Used without a gate, they speed up the production of rework.
