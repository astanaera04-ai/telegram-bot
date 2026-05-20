bot/
│
├── main.py                # Entry point (bot запуск)
├── config.py              # Token and settings
│
├── database/
│   ├── db.py              # DB connection
│   └── models.py          # Tables creation
│
├── handlers/
│   ├── start.py           # /start command
│   ├── study.py           # Timer logic (start/stop)
│   ├── stats.py           # Statistics
│   └── settings.py        # Subjects & goals
│
├── keyboards/
│   └── inline.py          # Inline buttons
│
├── services/
│   ├── timer_service.py   # Timer logic
│   └── stats_service.py   # Stats calculations
│
└── states/
    └── form.py            # FSM states
