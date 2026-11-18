# Examples

- `exemple-coach.json`: the `COACH` object of a **fictional** athlete (Camille, 10 km, goal 52:00). It serves as a filling template: every field of the schema in `kit/GUIDE-CLAUDE.md` appears in it. The `_demo` field is only read by the demo.
- `demo.html`: the dashboard filled with this example. Open it in your browser. It connects to nothing, and the dates are shifted to the current week. Generated file: don't edit it by hand.

To regenerate it after changing the template or the example:

```
python3 -I exemples/build-demo.py
```

The example never touches a real project: it goes through neither an artifact nor your database, only through this folder.
