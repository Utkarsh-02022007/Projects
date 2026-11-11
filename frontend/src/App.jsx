
import { useState } from "react";
import "./App.css";

const initialContacts = [
  { id: 1, name: "Mum", phone: "9876543210", relation: "Family", primary: true },
  { id: 2, name: "Aarav", phone: "9876512345", relation: "Friend", primary: false },
];

const visitedPlaces = [
  {
    id: 1,
    place: "K.R. Mangalam University",
    area: "Sohna Road, Gurugram",
    date: "Today",
    time: "10:20 AM",
    type: "College",
  },
  {
    id: 2,
    place: "Huda City Centre",
    area: "Sector 29, Gurugram",
    date: "Yesterday",
    time: "6:45 PM",
    type: "Transit",
  },
  {
    id: 3,
    place: "Galleria Market",
    area: "DLF Phase 4, Gurugram",
    date: "Yesterday",
    time: "5:15 PM",
    type: "Shopping",
  },
];

function Icon({ children }) {
  return (
    <span className="app-icon" aria-hidden="true">
      {children}
    </span>
  );
}

function App() {
  const [activePage, setActivePage] = useState("map");
  const [journeyActive, setJourneyActive] = useState(false);
  const [destination, setDestination] = useState("");

  const [sosConfirm, setSosConfirm] = useState(false);
  const [sosSent, setSosSent] = useState(false);

  const [contacts, setContacts] = useState(initialContacts);
  const [showContactForm, setShowContactForm] = useState(false);

  const [contactName, setContactName] = useState("");
  const [contactPhone, setContactPhone] = useState("");
  const [contactRelation, setContactRelation] = useState("Family");

  // Start or end a demo journey
  const startJourney = () => {
    if (!journeyActive && !destination.trim()) {
      alert("Please enter your destination first.");
      return;
    }

    setJourneyActive(!journeyActive);
  };

  // Add a trusted contact
  const addContact = (event) => {
    event.preventDefault();

    if (!contactName.trim()) {
      alert("Please enter the contact name.");
      return;
    }

    if (!/^\d{10}$/.test(contactPhone)) {
      alert("Enter a valid 10-digit phone number.");
      return;
    }

    setContacts((current) => [
      ...current,
      {
        id: Date.now(),
        name: contactName.trim(),
        phone: contactPhone,
        relation: contactRelation,
        primary: current.length === 0,
      },
    ]);

    setContactName("");
    setContactPhone("");
    setContactRelation("Family");
    setShowContactForm(false);
  };

  // Remove a contact
  const removeContact = (id) => {
    setContacts((current) =>
      current.filter((contact) => contact.id !== id)
    );
  };

  // Select a primary/favourite contact
  const setPrimaryContact = (id) => {
    setContacts((current) =>
      current.map((contact) => ({
        ...contact,
        primary: contact.id === id,
      }))
    );
  };

  const navItems = [
    { id: "map", label: "Map", icon: "⌖" },
    { id: "sos", label: "SOS", icon: "!" },
    { id: "history", label: "Visited", icon: "◷" },
    { id: "contacts", label: "Contacts", icon: "▤" },
  ];

  return (
    <div className="safeher-app">

      {/* HEADER */}
      <header className="app-header">
        <a
          className="app-brand"
          href="#map"
          onClick={() => setActivePage("map")}
        >
          <span className="brand-mark">S</span>
          <span>
            SafeHer <b>AI</b>
          </span>
        </a>

        <div className="header-status">
          <span />
          Demo mode
        </div>
      </header>

      <main className="app-main">

        {/* MAP PAGE */}
        {activePage === "map" && (
          <section className="screen">

            <div className="screen-heading">
              <div>
                <p className="eyebrow">YOUR SAFETY SPACE</p>
                <h1>Live map</h1>
                <p className="screen-subtitle">
                  Check your location and manage your journey.
                </p>
              </div>

              <span className="location-status">
                <span />
                GPS preview
              </span>
            </div>

            <div className="map-panel">
              <div className="map-grid" />

              <svg
                className="map-streets"
                viewBox="0 0 600 420"
                preserveAspectRatio="none"
                aria-hidden="true"
              >
                <path d="M-20 85 L180 155 L330 90 L620 180 M-30 300 L170 230 L330 280 L630 210 M100 -20 L230 440 M420 -20 L350 440 M520 -20 L470 440" />

                <path
                  d="M-20 85 L180 155 L330 90 L620 180"
                  className="map-road-main"
                />
              </svg>

              <div className="map-place-label label-a">Sector 55</div>
              <div className="map-place-label label-b">Golf Course Road</div>
              <div className="map-place-label label-c">Sohna Road</div>

              <div className="map-route-line" />
              <div className="map-current-pin">
                <span />
              </div>
              <div className="map-destination-pin">B</div>

              <div className="map-attribution">
                Illustrative map · Not live GPS
              </div>

              <button
                className="map-locate"
                onClick={() =>
                  alert("Live GPS will be connected in the backend stage.")
                }
                aria-label="Locate me"
              >
                ◎
              </button>
            </div>

            <div className="location-summary">
              <div className="summary-icon">
                <Icon>⌖</Icon>
              </div>

              <div>
                <span className="field-label">CURRENT LOCATION</span>
                <strong>Location preview</strong>
                <p>
                  Live location will appear after GPS integration.
                </p>
              </div>
            </div>

            <div className="panel journey-panel">
              <div className="panel-heading">
                <div>
                  <h2>
                    {journeyActive
                      ? "Journey in progress"
                      : "Plan a journey"}
                  </h2>

                  <p>
                    {journeyActive
                      ? "Your demo journey is active."
                      : "Add a destination to begin."}
                  </p>
                </div>

                {journeyActive && (
                  <span className="active-pill">Active</span>
                )}
              </div>

              <label className="field-label" htmlFor="destination">
                DESTINATION
              </label>

              <input
                id="destination"
                className="text-input"
                value={destination}
                onChange={(event) =>
                  setDestination(event.target.value)
                }
                placeholder="Where are you going?"
                disabled={journeyActive}
              />

              <button
                className={`wide-button ${
                  journeyActive ? "button-stop" : ""
                }`}
                onClick={startJourney}
              >
                {journeyActive
                  ? "End demo journey"
                  : "Start journey"}
              </button>

              <p className="small-note">
                This is a frontend demonstration. Background tracking is not active.
              </p>
            </div>

            <button
              className="sos-shortcut"
              onClick={() => setActivePage("sos")}
            >
              <span className="sos-shortcut-mark">SOS</span>

              <span>
                <b>Need urgent help?</b>
                <small>Open the emergency screen</small>
              </span>

              <span className="shortcut-arrow">›</span>
            </button>

          </section>
        )}

        {/* SOS PAGE */}
        {activePage === "sos" && (
          <section className="screen sos-screen">

            <div className="screen-heading">
              <div>
                <p className="eyebrow">EMERGENCY SUPPORT</p>
                <h1>Emergency SOS</h1>
                <p className="screen-subtitle">
                  Use this if you need urgent assistance.
                </p>
              </div>
            </div>

            <div className="sos-main-panel">

              <div className="sos-ring">
                <button
                  className="sos-button"
                  onClick={() => {
                    setSosConfirm(true);
                    setSosSent(false);
                  }}
                >
                  SOS
                </button>
              </div>

              <h2>Press for emergency help</h2>

              <p>
                In a real emergency, contact local emergency services directly.
                This demo does not send an alert.
              </p>

              <button
                className="wide-button emergency-button"
                onClick={() => {
                  setSosConfirm(true);
                  setSosSent(false);
                }}
              >
                Activate SOS demo
              </button>

            </div>

            <div className="panel">
              <h2>What happens when SOS is activated?</h2>

              <ul className="sos-steps">
                <li>
                  <span>1</span>
                  <div>
                    <b>Confirm the alert</b>
                    <small>You can cancel an accidental press.</small>
                  </div>
                </li>

                <li>
                  <span>2</span>
                  <div>
                    <b>Share your situation</b>
                    <small>
                      Your configured contacts can be notified after backend integration.
                    </small>
                  </div>
                </li>

                <li>
                  <span>3</span>
                  <div>
                    <b>Get support</b>
                    <small>
                      Emergency service integration is not active in this prototype.
                    </small>
                  </div>
                </li>
              </ul>
            </div>

            {sosConfirm && (
              <div className="modal-backdrop">
                <div
                  className="confirm-modal"
                  role="dialog"
                  aria-modal="true"
                  aria-labelledby="confirm-title"
                >
                  {!sosSent ? (
                    <>
                      <div className="modal-alert-icon">!</div>

                      <h2 id="confirm-title">
                        Activate SOS demo?
                      </h2>

                      <p>
                        This will only show a demo confirmation.
                        No message or emergency call will be sent.
                      </p>

                      <button
                        className="wide-button emergency-button"
                        onClick={() => setSosSent(true)}
                      >
                        Confirm demo alert
                      </button>

                      <button
                        className="modal-cancel"
                        onClick={() => setSosConfirm(false)}
                      >
                        Cancel
                      </button>
                    </>
                  ) : (
                    <>
                      <div className="modal-success-icon">✓</div>

                      <h2 id="confirm-title">
                        Demo alert displayed
                      </h2>

                      <p>
                        No contacts were notified. Real SOS delivery will be
                        added with the backend and messaging service.
                      </p>

                      <button
                        className="wide-button"
                        onClick={() => setSosConfirm(false)}
                      >
                        Close
                      </button>
                    </>
                  )}
                </div>
              </div>
            )}

          </section>
        )}

        {/* VISITED LOCATIONS PAGE */}
        {activePage === "history" && (
          <section className="screen">

            <div className="screen-heading">
              <div>
                <p className="eyebrow">YOUR ACTIVITY</p>
                <h1>Visited locations</h1>
                <p className="screen-subtitle">
                  A sample view of places from previous journeys.
                </p>
              </div>
            </div>

            <div className="history-notice">
              <span>i</span>
              <p>
                These are sample entries. Your actual location history will
                appear after GPS and backend integration.
              </p>
            </div>

            <div className="history-date-heading">
              RECENT ACTIVITY
            </div>

            <div className="history-list">
              {visitedPlaces.map((place, index) => (
                <article className="history-item" key={place.id}>

                  <div className="history-timeline">
                    <span className="history-dot" />
                    {index !== visitedPlaces.length - 1 && (
                      <span className="history-line" />
                    )}
                  </div>

                  <div className="history-card">

                    <div className="history-card-top">
                      <span className="place-type">{place.type}</span>
                      <span className="history-time">
                        {place.date} · {place.time}
                      </span>
                    </div>

                    <h3>{place.place}</h3>

                    <p>
                      <Icon>⌖</Icon>
                      {place.area}
                    </p>

                    <button
                      className="text-action"
                      onClick={() => {
                        setActivePage("map");
                        setDestination(place.place.trim());
                      }}
                    >
                      View on map <span>↗</span>
                    </button>

                  </div>
                </article>
              ))}
            </div>

            <div className="privacy-note">
              <div>
                <b>Your location data matters</b>
                <p>
                  History controls, retention settings and deletion options
                  will be added before real data is stored.
                </p>
              </div>
            </div>

          </section>
        )}

        {/* SOS CONTACTS PAGE */}
        {activePage === "contacts" && (
          <section className="screen">

            <div className="screen-heading">
              <div>
                <p className="eyebrow">PEOPLE YOU TRUST</p>
                <h1>SOS contacts</h1>
                <p className="screen-subtitle">
                  Choose who should be contacted in an emergency.
                </p>
              </div>

              <button
                className="add-contact-top"
                onClick={() =>
                  setShowContactForm(!showContactForm)
                }
              >
                {showContactForm ? "Close" : "+ Add"}
              </button>
            </div>

            <div className="history-notice">
              <span>i</span>
              <p>
                Contacts are saved only in this page's temporary demo state.
                They are not yet stored securely or notified.
              </p>
            </div>

            {showContactForm && (
              <form
                className="panel contact-form"
                onSubmit={addContact}
              >

                <h2>Add a trusted contact</h2>

                <label className="field-label" htmlFor="contact-name">
                  NAME
                </label>

                <input
                  id="contact-name"
                  className="text-input"
                  value={contactName}
                  onChange={(event) =>
                    setContactName(event.target.value)
                  }
                  placeholder="Enter full name"
                  required
                />

                <label className="field-label" htmlFor="contact-phone">
                  PHONE NUMBER
                </label>

                <input
                  id="contact-phone"
                  className="text-input"
                  type="tel"
                  inputMode="numeric"
                  autoComplete="tel-national"
                  value={contactPhone}
                  onChange={(event) =>
                    setContactPhone(
                      event.target.value.replace(/\D/g, "").slice(0, 10)
                    )
                  }
                  placeholder="Enter 10-digit mobile number"
                  pattern="[0-9]{10}"
                  maxLength={10}
                  minLength={10}
                  required
                />

                <small className="phone-hint">
                  {contactPhone.length}/10 digits
                </small>

                <label className="field-label" htmlFor="contact-relation">
                  RELATIONSHIP
                </label>

                <select
                  id="contact-relation"
                  className="text-input"
                  value={contactRelation}
                  onChange={(event) =>
                    setContactRelation(event.target.value)
                  }
                >
                  <option>Family</option>
                  <option>Friend</option>
                  <option>Other</option>
                </select>

                <button className="wide-button" type="submit">
                  Save contact
                </button>

              </form>
            )}

            <div className="contacts-count">
              {contacts.length} trusted{" "}
              {contacts.length === 1 ? "contact" : "contacts"}
            </div>

            <div className="contacts-list">
              {contacts.map((contact) => (
                <article className="contact-card" key={contact.id}>

                  <div className="contact-avatar">
                    {contact.name.charAt(0).toUpperCase()}
                  </div>

                  <div className="contact-details">

                    <div className="contact-name-row">
                      <h3>{contact.name}</h3>

                      {contact.primary && (
                        <span className="primary-tag">Primary</span>
                      )}
                    </div>

                    <p>{contact.phone}</p>
                    <small>{contact.relation}</small>

                  </div>

                  <div className="contact-actions">

                    <button
                      className={`favorite-button ${
                        contact.primary ? "is-favorite" : ""
                      }`}
                      type="button"
                      onClick={() => setPrimaryContact(contact.id)}
                      aria-label={`Set ${contact.name} as primary`}
                      aria-pressed={contact.primary}
                    >
                      ★
                    </button>

                    <button
                      type="button"
                      onClick={() => removeContact(contact.id)}
                      aria-label={`Remove ${contact.name}`}
                    >
                      ×
                    </button>

                  </div>
                </article>
              ))}
            </div>

            {contacts.length === 0 && (
              <div className="empty-state">
                No trusted contacts added yet.
              </div>
            )}

            <div className="privacy-note contact-privacy-note">
              <div>
                <b>Keep contacts up to date</b>
                <p>
                  Only add people who have agreed to be your emergency contacts.
                </p>
              </div>
            </div>

          </section>
        )}

      </main>

      {/* BOTTOM NAVIGATION */}
      <nav className="bottom-nav" aria-label="Main navigation">

        {navItems.map((item) => (
          <button
            key={item.id}
            className={`bottom-nav-item ${
              activePage === item.id ? "selected" : ""
            } ${item.id === "sos" ? "nav-sos" : ""}`}
            onClick={() => {
              setActivePage(item.id);
              setSosConfirm(false);
            }}
            aria-current={activePage === item.id ? "page" : undefined}
          >
            <span className="bottom-nav-icon">{item.icon}</span>
            <span>{item.label}</span>
          </button>
        ))}

      </nav>
    </div>
  );
}

export default App;
