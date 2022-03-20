# Changelog 

## [Quizlet 9, 0.4.1] - 2022-03-19
Revised Disease outbreak schema and HRF.
### [Disease Outbreak]
- added "modality"="negated" to negated events in the Contributory Factors episode 
- removed direct outlink from Contributory Factors to "early infections". 
- Added "Purchase Contaminated Object" event in "Onset".
- Changed "Spread Disease" to "Transmission"
- Added "Collect Lab Samples" and "Analyze Data" in Medical Response. This is meant to match the "Investigation" episode in SBU's schema.
- Rename  "Identifycategorize" to "IdentifyDiseaseSource"
- Fixed parent-child relations for Illness Outcome XOR container
- Added "Educate" event to "Civil Justice"
- Added "Inspection" event to "Authority Response"
- Added "Information Campaign" event to "Authority Response"
## [Quizlet 9, 0.4] - 2022-03-18
Refined all schemas. See sections for specific notes.
### [Business Change]
The entire schema is full of isolated events. Primitive events that do not have children still had `children_gate` and `children` in their events list, resulting in a convoluted graph.
- organized events into containers and linked events in those containers
- Recycled Civil Justice and Criminal Justice chapters, with added events to make sense in the context
### [Election]
- moved Candidate Continues into Nomination chapter as an XOR gate; created repeatable Nomination Campaign chapter
- added participants
- resolved some entities only referred to once warnings
- added relations
### [Sports]
- many events have irrelevant Qnodes and labels; double checked all Qnodes and labels and fixed them where necessary
- participant rolenames do not fit XPO format; redid all participants
- entities do not have names; fixed and added missing entities
- resolved entities only referred to once warnings
- added relations
### [Kidnapping]
- each event only had 1 or 2 participants; added missing participants and entities
- removed redundant events
- replaced Legality chapter with Criminal Justice chapter
- added relations
### [Disease Outbreak]
- added participants
- add feedback events
	- Contributory Factors: Environmental and Social Factors containers
	- Medical Response: Disinfect contaminated areas, identify and quarantine exposed group
	- Civil Justice: Contact attorney
### [Mass Shooting]
- resolved some entities only referred to once warnings
- added relations
### [Manmade Disaster and Rescue]
- fixed location of "treatment"
- added participants
- added WD descriptions
- added relations
### [International Conflict]
- added participants
- added entities and participants for all events, including finding good Qnodes for entities
- created coreferences between participants
- added the events for the two schema episodes remaining to be done based on the schemaFeedback document: government response, and battle
	- also added entities and created coreferences for them.
	- for participants, found PropBank equivalents and extracted roles from them.
- made optional and repeatable events 
### [General Attack]
- added participants
- fixed Qnodes and Qlabels
- Organized the events into containers (created a document similar to the schema feedback for international conflict)
- Linked the childs and outlinks (hierarchical and temporal links) between events and containers
- Recycled some events and their participants from other schemas, but changed the entity links to match the current schema
- added entities that match the scenarios and are important to them
- created xor gates when appropriate
- made optional and repeatable events
- found Qnodes for new (non-recyclable) entities and events 
### [Natural Disaster and Rescue]
- `damage` should be an outlink from all subtypes of natural disaster, not a type of natural disaster, as it is caused by natural disasters.
- `trap` should be an outlink in all the disaster subtypes.
- fixed some qnodes 
- added descriptions from wd descriptions
- added a second `treatment` node for onsite treatment, separate from the treatment after taking to the medical facility.
### [Civil Unrest]
- added WD descriptions
- made sure all qlabel values have underscores instead of spaces
- added some entities and removed some others
- introduced correct entity links for all participants
- made a distinction between person (as an individual) and group of humans
- fixed the Qnodes that were either mistakenly selected or were pointing to a Wikimedia Disambiguation Page.
### [General IED]
- pruned participants to form coference links
- added Criminal Justice chapter
- added relations
### [Other IEDs]
- added specific events with their corresponding participants and entities based on previous schemas to General IED template

-----

## [Quizlet 9, 0.3] - 2022-02-10
### Added 
- [Manmade Disaster Rescue] new schema 
- [Natural Disaster Rescue] new schema 
- script for checking schema 
### Fixed 
- Issues with Qnode format 
- Issues with multiple root nodes 

-----

## [Quizlet9, 0.2] - 2022-02-03
### Added 
- [Disease Outbreak] "partially coincident with" relations between entities 
- [Business Change] new schema + hrf 
- [IED] new schema + hrf 
- [Kidnapping] new schema + hrf 
- [Terrorist Attack] new schema + hrf 
- [Civil Unrest] new schema + hrf 
- [Election] new schema + hrf 
- [Sports] new schema + hrf 
- [Mass Shooting] new schema + hrf 
- [International Conflict] new schema + hrf 
- [Combined] new multiscenario schema library `resin-schemalib.json`

### Changed 
- [Disease Outbreak] update sdfVersion to 1.4.1

### Fixed
- [Disease Outbreak] added parents for dangling events 

