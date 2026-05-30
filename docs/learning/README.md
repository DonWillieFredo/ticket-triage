# Learning log

The [training console](../../tools/training-console.html) is a convenience dashboard for tracking weekly goals, hours, tasks, and portfolio artifacts while you build ticket-triage.

**Browser localStorage is not the permanent source of truth.** Data lives only in your browser until you export it or copy summaries elsewhere.

## What to commit here

At the end of each week, copy your week summary from the console (or an exported JSON backup) into a Markdown file:

```
docs/learning/week-01.md
docs/learning/week-02.md
...
```

Each file should capture what shipped, blockers, reflections, and any resume bullets or artifacts produced that week. These files travel with the repo and survive browser clears, machine changes, and collaborator review.

## Backup habit

Use **Export data** in the console regularly to download `ticket-triage-training-console-backup.json`. Store backups locally if you want, but treat `docs/learning/week-XX.md` as the canonical weekly record in Git.
