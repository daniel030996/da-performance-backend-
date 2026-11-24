// DA Performance backend
// The DVLA key is read ONLY from the DVLA_API_KEY environment variable.
// It is never sent to the browser.

const express = require("express");
const cors = require("cors");

const app = express();
const PORT = process.env.PORT || 3000;
const DVLA_API_KEY = process.env.DVLA_API_KEY;
const DVLA_URL =
  "https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles";

if (!DVLA_API_KEY) {
  console.error("DVLA_API_KEY is not set. Add it in your host's environment settings.");
  process.exit(1);
}

// Optional: restrict which sites may call this API, e.g.
// ALLOWED_ORIGINS=https://daperformance.co.uk,https://www.daperformance.co.uk
const allowed = (process.env.ALLOWED_ORIGINS || "")
  .split(",")
  .map((s) => s.trim())
  .filter(Boolean);
app.use(cors(allowed.length ? { origin: allowed } : {}));
app.use(express.json({ limit: "10kb" }));

app.get("/health", (_req, res) => res.json({ ok: true }));

app.post("/api/vehicle", async (req, res) => {
  const raw = (req.body && req.body.registration) || "";
  const registration = String(raw).replace(/\s+/g, "").toUpperCase();

  if (!/^[A-Z0-9]{1,8}$/.test(registration)) {
    return res.status(400).json({ error: "Please provide a valid UK registration." });
  }

  try {
    const dvlaRes = await fetch(DVLA_URL, {
      method: "POST",
      headers: {
        "x-api-key": DVLA_API_KEY,
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({ registrationNumber: registration }),
    });

    if (dvlaRes.status === 404) {
      return res.status(404).json({ error: "Vehicle not found." });
    }
    if (!dvlaRes.ok) {
      const detail = await dvlaRes.text();
      console.error("DVLA error", dvlaRes.status, detail);
      return res.status(502).json({ error: "Vehicle lookup failed. Please try again." });
    }

    const v = await dvlaRes.json();
    return res.json({
      registration: v.registrationNumber || registration,
      make: v.make || null,
      // DVLA VES does not return a model; kept for frontend compatibility.
      model: v.model || null,
      year: v.yearOfManufacture || null,
      fuel: v.fuelType || null,
      engineSize: v.engineCapacity ? `${v.engineCapacity}cc` : null,
      colour: v.colour || null,
    });
  } catch (err) {
    console.error("Lookup error", err);
    return res.status(500).json({ error: "Server error during vehicle lookup." });
  }
});

app.listen(PORT, () => console.log(`DA Performance backend listening on ${PORT}`));
