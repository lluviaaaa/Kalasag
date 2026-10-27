## What does this PR do?

## Execution Plan step(s) covered

- Step(s):  
- Phase:

## How to check it

## Handoff / notes for teammates

---

## Author checklist (tick before requesting review)

- [ ] I started from the latest `main` and merged it into my branch (`git merge main`)  
- [ ] Notebook outputs are cleared for any notebook I changed  
- [ ] No large or private files are included (datasets, models, `.pcap`, `.ova`, `.vdi`)  
- [ ] I ran `pytest` for the part I changed (or no tests exist yet)  
- [ ] I read my own changes once on the **Files changed** tab  
- [ ] This PR is small: one Execution Plan step (or a small group of steps)  
- [ ] Docs are updated, or a handoff note is added if passing work to another member

## Reviewer checklist (tick as you review)

- [ ] Was the stratified split done **before** any SMOTE/ADASYN? Was resampling applied to the training set only?  
- [ ] Is the scaler fitted on training data only, and is the saved scaler reused unchanged elsewhere?  
- [ ] Are any identifier columns (IP address, flow ID, timestamp) accidentally used as model features?  
- [ ] Are any big files included by mistake (dataset, models, `.pcap`, `.ova`, `.vdi`)?  
- [ ] Are notebook outputs cleared?  
- [ ] Does any block or firewall command run only inside the isolated lab VM, never on a host laptop or real network?  
- [ ] Can I explain what this code does? (If not, ask. Everyone has to defend all of it.)  
- [ ] Does the PR update the relevant docs, or add a handoff note when passing work to another member?

