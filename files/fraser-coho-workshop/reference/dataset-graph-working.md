# Fraser Coho conceptual graph — draft for review

Status: draft working example; independent scientific review pending.

This is a comparison aid for a learner-created diagram. It is not an approved
ontology, a source-data product, or an assertion that every source record
represents one observation event. No new ontology identifiers are minted.

## Read the graph

Open [the SVG overview](dataset-graph-working.svg). The full editable statements
are in [dataset-nodes-working.csv](dataset-nodes-working.csv) and
[dataset-edges-working.csv](dataset-edges-working.csv). The SVG shows a selected
set of relationships; the tables record evidence, uncertainty and the two
example values from the first source record.

- A source record refers to a source population, names a waterbody, specifies
  a species and carries the year the estimate is for.
- A source population identifier and a source record identifier are different
  roles. `POP_ID` plus `ANALYSIS_YR` is not unique: 173 records contain 164
  distinct pairs.
- The estimation activity uses a method, applies a variable and can generate a
  result. Its exact relationship to source records and field visits needs
  review.
- The variable concerns an entity and represents a property. Abundance is the
  working characteristic; the full adult-spawner variable has additional scope.
- The reported result has a value and a unit. The first record's value `758`
  and population identifier `46200` are examples, not class definitions.
- Conservation Unit membership is a disconnected question because the slice
  supplies no CU field or membership crosswalk. Do not connect it as an asserted
  assignment without an appropriate dated source.

## Evidence and limits

The current official DFO dictionary supports year-of-estimate wording, dates
of inspections, subdistrict wording for AREA, and mature adults excluding
jacks. Its adult-spawner definition does not establish natural origin. The
official dictionary was retrieved on 2026-09-08 and may postdate the workbook
used for the 2023–2024 slice; retain that temporal distinction.

The supplied starter dictionary is separate evidence. It uses a natural-origin
description and PFMA wording that the current official dictionary does not
support. Preserve those original descriptions while explaining the working
correction; do not quietly replace provenance with an apparent consensus.

See [scientific-review-packet.md](scientific-review-packet.md) for source
references, the proposed six-field exercise and the requested scientific review.

## Future OWL work

Local IDs, typed nodes, directed verbs, evidence and uncertainty are retained
so a later ontology specialist can choose appropriate classes, individuals,
properties and mapping strengths. These choices have not already been made by
the diagram. The Salmon Domain Ontology metamodel is an optional orientation
view, while its core and conventions supply reusable modeling guidance.
