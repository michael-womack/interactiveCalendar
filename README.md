# Interactive Calendar
 A Python-based calendar application using tkinter, integrating event management, holiday APIs, and real-time weather data.
 Developed collaboratively to support event tracking, holiday integration, and live weather display.

<img src="assets/screenshot.png" width="500" alt="Calendar Screenshot">

---

## Project Goals

**Objective**  
Build a Python-based calendar app with an intuitive GUI supporting event management, holiday tracking, weather updates, and visual calendar navigation.

**Core Functions**

- View yearly and monthly calendars with smooth navigation
- Add, view, and delete single or recurring events
- Highlight user events and national holidays with color coding
- Display current weather conditions for user-selected cities
- Support multiple UI color themes for personalization
- Input validation with clear error messages

**Tech Stack**

- Core Language: Python
- GUI: tkinter
- APIs: OpenWeatherMap, Nager.Date (holidays)
- Data Persistence: JSON
- Modules: datetime, calendar, requests

---

## Team Collaboration & Individual Contributions

This project was developed collaboratively across three two-week sprints, with each team member focusing on distinct components:

### My Contributions

- Designed and implemented the initial yearly calendar GUI and monthly zoom/navigation features  
- Developed core event management: adding, viewing, deleting, and supporting recurring events  
- Created the color-coded sidebar and enabled calendar theme cycling for better UI customization  
- Integrated weather API with dynamic city input and live display  
- Optimized performance by implementing holiday API caching to reduce lag  
- Enhanced usability by refining popup event details and compact sidebar formatting  
- Led debugging efforts and kept project documentation updated throughout the development cycle

### Team Contributions

- Developed multi-layer dropdown menus and event creation interfaces  
- Integrated event creation into the main application window and implemented color coding  
- Extended theme customization features and performed extensive testing

---

## Design Phase

### Data Model

Events stored as JSON with fields:

- Date (YYYY-MM-DD)
- Event name, time, description
- Recurrence frequency (None, Weekly, Monthly, etc.)

Holiday data cached per year to reduce API calls.  
Weather info fetched live from API per city input.

---

### UI Sketch

**Main Window**

- Large text-based calendar display (year or month)
- Buttons to change year/month and cycle color themes
- Sidebar with event list and weather display
- Forms to add event details and set recurrence

---

### User Workflow

1. Open app → default yearly view displayed  
2. Enter year/month → calendar updates accordingly  
3. Add new event → specify name, date, time, description, recurrence  
4. View or delete events from monthly event list  
5. Change calendar color theme with button  
6. Update weather by entering city name  

---

## Development Plan

### Sprint 1 – Core Features (Weeks 1–2)

- Create initial calendar GUI with yearly and monthly views  
- Implement event creation system with forms  
- Develop multi-layer dropdown menus and buttons for navigation  

### Sprint 2 – Notifications, Recurring Events, Color Coding (Weeks 3–4)

- Integrate event system into main window  
- Add color coding to highlight events and holidays  
- Support recurring events with different intervals  
- Allow color theme toggling  

### Sprint 3 – Weather, Integrations, Testing (Weeks 5–6)

- Integrate weather API with city selection  
- Add holiday API integration and caching  
- Implement event deletion and popup details  
- Perform testing and bug fixes  
- Polish UI layout and update README  

---

## Testing Plan

- Validate date/time inputs and recurrence formats  
- Handle API failures gracefully with fallback messages  
- Test event addition, deletion, and persistence  
- Ensure calendar navigation works across year boundaries  
- Confirm UI updates correctly reflect data changes  

---

## Documentation & Polishing

- Comprehensive README with overview, features, and run instructions  
- Code commented with docstrings and inline notes  
- Organized file structure with clear separation of concerns  

---

## Timeline Overview

| Phase                                | Est. Time |
| ------------------------------------ | --------- |
| Requirements & Design                | 3 days    |
| Core GUI & Calendar Logic            | 5 days    |
| Event System & Recurrence            | 5 days    |
| API Integrations (Weather, Holidays) | 4 days    |
| Testing & Debugging                  | 4 days    |
| UI Polishing & Docs                  | 3 days    |

---

## Summary

This project demonstrates strong collaborative software development and my leadership in driving core calendar functionality and API integrations. It highlights proficiency with Python, GUI design, event-driven programming, and working effectively within a team to deliver a polished, user-centric product.

