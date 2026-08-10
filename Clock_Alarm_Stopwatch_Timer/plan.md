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
