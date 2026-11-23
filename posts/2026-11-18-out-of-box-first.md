---
title: 'Out-of-box first: keeping ServiceNow requirements on standard capability'
date: 2026-11-18
summary: 'Most ServiceNow customisation starts as a reasonable-sounding requirement. Here is how I challenge it, and how that kept 80% of an escalated change-management backlog on standard platform capability.'
minutes: 5
draft: false
---

Almost every ServiceNow instance that has become hard to upgrade got that way one sensible decision at a time. Nobody sets out to build technical debt. A stakeholder asks for a field, a form that looks like the old one, an approval step their team has always had, and each request on its own seems harmless. Multiplied across a programme, they turn a platform that should improve with every release into one that resists it.

My default on every engagement is out-of-box first. Not out-of-box only: there are good reasons to extend the platform. But custom work has to earn its place, and the way to make it earn its place is to make the decision visible.

## Ask for the need, not the field

Requirements usually arrive written as solutions. "Add a dropdown for approval type." "Copy the fields from the old change form." Taken literally, these lead straight to configuration. So the first question in every workshop is the one underneath: what decision does this field support, who makes it, and what happens if it is missing?

Very often the need is real but the platform already meets it, through an existing field, a different change model, a related list, or a report. The stakeholder had simply never seen it.

## The out-of-box versus new-field matrix

For each requirement I record five things in one place:

  - **The business need**, in the stakeholder's words.
  - **What the platform does today** out of the box.
  - **The gap**, if there genuinely is one.
  - **The decision**: use standard capability, configure, extend, or build custom.
  - **Who agreed it**, and when.

The matrix does two jobs. It forces the gap to be stated explicitly, and a surprising number of gaps disappear once someone has to write them down. And it turns every custom item into a visible cost: something that will need testing at every upgrade and maintaining after go-live. When people can see that cost next to the need, they make better choices.

## Write the decisions down so they stay made

The second tool is a decision register. Programmes lose weeks to re-opening settled questions, usually because the person who agreed the decision has moved on or the reasoning was never captured. A short record of what was decided, why, and by whom lets the team move forward and gives later stakeholders something to read instead of something to reargue.

## In practice

I used this approach to stabilise an escalated Change Management workstream for a financial-services client. The backlog needed to become groom-ready: epics, stories, non-functional requirements, personas and dependencies. Alongside that, I authored workflows for Minor, Standard, Significant and Major changes and an out-of-box versus new-field matrix covering the requirements.

The result was that 80% of requirements were directed toward standard platform capability. The remaining 20% were deliberate, documented extensions, each with a reason someone could point to.

<!-- [Tosin: add a sentence or two here on what the remaining 20% were, or what convinced the stakeholders, if you can share it without identifying the client.] -->

## When custom is the right answer

Out-of-box first is not a rule against customisation. Regulatory requirements, genuinely distinctive policy, and integrations with systems the platform does not know about are all good reasons to extend. The test is simple: can you state the need, show that standard capability does not meet it, and name who accepted the long-term cost? If you can, build it well. If you cannot, the platform probably already does what you need.
