# Project Plan: Modern Desktop Clock Suite

## 1. Project Overview
A modern, highly accurate utility desktop clock application built in Python, featuring a local digital/analog clock face, customizable multiple alarm settings, stopwatch lap counters, and countdown timers.

## 2. Development Milestones
- **Milestone 1: Core Clock & Timing Engine**
  - Implement tick loops and accurate datetime poll logic.
  - Write stopwatch lap recorder and count-down timer controllers.
- **Milestone 2: Multi-threaded Alarm Manager**
  - Design alarm scheduling logic.
  - Implement asynchronous audio playback thread for alarm triggers.
- **Milestone 3: World Clock & Timezones**
  - Add zone lookup support using `zoneinfo` or `pytz`.
- **Milestone 4: Modern CustomTkinter GUI**
  - Design visual clock faces, alarm cards, and tab navigations.
- **Milestone 5: System Tray & Floating Overlay Overlay**
  - Add minimize-to-tray pystray logic and always-on-top window configurations.

## 3. Technical Stack
- **GUI Engine**: `CustomTkinter`
- **Audio Output Mixer**: `pygame.mixer` (runs asynchronously)
- **Timezone Library**: Native Python `zoneinfo` (fallback to `pytz`)
- **System Tray Bridger**: `pystray` + `Pillow`

## 4. Required Assets Structure
- `assets/alarms/` - Audio tone files (e.g. `chime.wav`, `alarm_tone.mp3`)
- `assets/icons/` - Application logo and system tray icons (.ico, .png)

## 5. UI/UX Style Guide
- **Visual Themes**:
  - *Dark Cyberpunk*: Background (`#09090E`), Primary Accent (`#EC4899` - Hot Pink), Secondary Accent (`#06B6D4` - Cyber Cyan).
  - *Light Minimalist*: Background (`#F9FAFB`), Primary Accent (`#3B82F6` - Royal Blue).
- **Core Views Layout**:
  - Main dial displaying current local time in large digital format.
  - Slide panels to toggle between Stopwatch (with split laps table), Timer presets, World Clock list, and Alarm schedule list.

## 6. Architecture & Concurrency Model
- **Avoiding Clock Drift**: The UI loop updates text values every 100ms, but instead of incrementing a local integer counter, it polls the actual system time via `datetime.now()` to prevent processing delays from causing time drift.
- **Asynchronous Audio Threading**: Alarm chimes are triggered in an isolated background thread to prevent the main GUI loop from blocking or hanging while playing audio files.
- **Always-On-Top State**: Uses the window flag `-topmost` to enable a floating overlay mode so users can keep the stopwatch or timer visible on top of full-screen work files.


## 7. Extended Specs: Alarm State & Settings Persistence (Day 1)
To ensure the application retains scheduled alarms, favorite world clocks, and user settings across restarts, a local configuration serialization system will be designed.
- **Data format**: JSON file representation (`settings.json`).
- **Location**: Packaged in the root directory under `config/settings.json`.
- **Data Schema**:
  ```json
  {
    "active_theme": "Dark Cyberpunk",
    "alarms": [
      {
        "id": "alarm_01",
        "time": "07:30",
        "repeat": ["Monday", "Wednesday", "Friday"],
        "tone": "chime.wav",
        "enabled": true
      }
    ],
    "world_clocks": ["UTC", "America/New_York", "Asia/Tokyo"]
  }
  ```
- **Trigger Events**:
  - **Save events**: Triggered automatically whenever an alarm is toggled, created, deleted, or when the theme preference changes.
  - **Load events**: Triggered during application initialization (`__init__` sequence of the Main Window) to mount current configuration states.


## 8. Extended Specs: Audio Fail-Safe & Fallback Engine (Day 2)
To guarantee that alarm alerts always sound even in the event of missing or corrupted files, a fallback audio validation tree is established.
- **Pre-play Check**: The system validates the absolute path of the chosen audio file prior to initiating playback.
- **Fallback Tree**:
  1. Attempt to play user selected tone (`user_alarm.mp3`).
  2. If file missing, fall back to default tone packaged with app (`assets/alarms/chime.wav`).
  3. If default wav file is missing/inaccessible, execute system hardware buzzer fallback.
- **Hardware Beep Code**:
  - Leverages Python's native `winsound.Beep` on Windows:
    ```python
    import winsound
    winsound.Beep(frequency=1000, duration=1000)
    ```
  - This ensures a physical alert sounds using the motherboard/OS buzzer if the sound card is locked or file access fails.


## 9. Extended Specs: Alarm Snooze & Volume Fade-In (Day 3)
A gradual wake-up experience and snooze function will be designed to enhance the sleep utility dashboard.
- **Snooze Logic**: When the alarm window triggers, clicking 'Snooze' adds a delayed alarm event (5 or 10 minutes offset) to the queue and shuts down the active audio player.
- **Progressive Volume Ramping**:
  - Prevents sudden loud alarms by ramping up volume levels:
    - Initial volume setting: `0.1` (10%).
    - Automatically increment volume by `0.1` every 3 seconds.
    - Max volume limit: `1.0` (100% after 30 seconds of play).
- **Auto-Snooze Timeout**:
  - To prevent continuous audio playing if the user is away, the audio player will automatically stop and snooze after 10 minutes of continuous alert ring state.


## 10. Extended Specs: Compact Overlay Mini-Widget (Day 4)
For users who wish to keep their stopwatch or count-down timer visible while working in other full-screen apps, a floating overlay view is implemented.
- **Mini layout toggle**: Clicking the icon in the header switches the GUI style sheet.
- **Glassmorphism Attributes**:
  - Sets window flags to override title borders:
    - Always-on-top: `self.attributes("-topmost", True)`.
    - Borderless: `self.overrideredirect(True)`.
    - Transparency alpha background: `self.attributes("-alpha", 0.85)`.
- **Drag-to-Move bindings**:
  - Since the title bar is removed, mouse bind triggers are set to reposition the window coordinate axes:
    ```python
    self.bind("<Button-1>", self.start_drag)
    self.bind("<B1-Motion>", self.drag_window)
    ```


## 11. Extended Specs: High-Resolution Timing & Thread safety (Day 5)
Precise timing measurements require bypassing typical scheduling lag issues in standard UI loops.
- **Eliminating Time Drift**: The stopwatch avoids using local counter increments which accumulate delay.
