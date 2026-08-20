const express = require("express");
const session = require("express-session");
const crypto = require("crypto");
const {
  auth,
  requiredScopes,
} = require("express-oauth2-jwt-bearer");

require("dotenv").config();

const app = express();
const PORT = 3000;

// Auth0 configuration
const AUTH0_DOMAIN = process.env.AUTH0_DOMAIN;
const CLIENT_ID = process.env.AUTH0_CLIENT_ID;
const CLIENT_SECRET = process.env.AUTH0_CLIENT_SECRET;
const AUDIENCE = process.env.AUTH0_AUDIENCE;

// ----------------------------------------------------
// Session - temporarily stores PKCE state/verifier
// ----------------------------------------------------
app.use(
  session({
    secret: process.env.SESSION_SECRET || "change-this-secret",
    resave: false,
    saveUninitialized: false,
    cookie: {
      httpOnly: true,
      secure: false,
      sameSite: "lax",
    },
  })
);

app.use(express.urlencoded({ extended: true }));

// ----------------------------------------------------
// Auth0 JWT validation middleware
// ----------------------------------------------------
const checkJwt = auth({
  issuerBaseURL: `https://${AUTH0_DOMAIN}`,
  audience: AUDIENCE,
});

// ----------------------------------------------------
// Home page
// ----------------------------------------------------
app.get("/", (req, res) => {
  const isLoggedIn = !!req.session.tokens;

  res.send(`
    <h1>SecureNova AI - Auth0 PKCE Demo</h1>
    <p>OAuth 2.0 Authorization Code + PKCE</p>

    ${
      isLoggedIn
        ? `
          <p><strong>Authenticated ✅</strong></p>
          <a href="/logout">Logout</a>
        `
        : `
          <a href="/login">Login with Auth0</a>
        `
    }

    <hr>

    <h2>Protected API Endpoints</h2>

    <ul>
      <li>
        GET /api/chat — requires read:ai-data
      </li>

      <li>
        POST /api/admin — requires write:admin
      </li>
    </ul>
  `);
});

// ----------------------------------------------------
// Start Authorization Code + PKCE flow
// ----------------------------------------------------
app.get("/login", (req, res) => {
  const state = crypto.randomBytes(32).toString("hex");

  const codeVerifier = crypto.randomBytes(32).toString("base64url");

  const codeChallenge = crypto
    .createHash("sha256")
    .update(codeVerifier)
    .digest("base64url");

  // Store values temporarily for callback validation
  req.session.oauthState = state;
  req.session.codeVerifier = codeVerifier;

  const params = new URLSearchParams({
    response_type: "code",
    client_id: CLIENT_ID,
    redirect_uri: `http://localhost:${PORT}/callback`,
     scope: "openid profile email read:ai-data",
    audience: AUDIENCE,
    state: state,
    code_challenge: codeChallenge,
    code_challenge_method: "S256",
  });

  res.redirect(
    `https://${AUTH0_DOMAIN}/authorize?${params.toString()}`
  );
});

// ----------------------------------------------------
// Auth0 callback
// ----------------------------------------------------
app.get("/callback", async (req, res) => {
  const { code, state } = req.query;

  // Validate state
  if (!state || state !== req.session.oauthState) {
    return res.status(400).send("Invalid OAuth state.");
  }

  if (!code) {
    return res.status(400).send("Authorization code missing.");
  }

  try {
    const tokenResponse = await fetch(
      `https://${AUTH0_DOMAIN}/oauth/token`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          grant_type: "authorization_code",
          client_id: CLIENT_ID,
          client_secret: CLIENT_SECRET,
          code: code,
          redirect_uri: `http://localhost:${PORT}/callback`,
          code_verifier: req.session.codeVerifier,
        }),
      }
    );

    const tokens = await tokenResponse.json();

    if (!tokenResponse.ok) {
      console.error(tokens);

      return res.status(400).send(`
        <h2>Token exchange failed</h2>
        <pre>${JSON.stringify(tokens, null, 2)}</pre>
      `);
    }

    // Remove temporary PKCE values
    delete req.session.oauthState;
    delete req.session.codeVerifier;

    // Store tokens in session
    req.session.tokens = tokens;

    res.send(`
      <h1>Authentication Successful ✅</h1>

      <p>
        Authorization Code + PKCE flow completed successfully.
      </p>

      <h3>Token Response</h3>

      <pre>${JSON.stringify(tokens, null, 2)}</pre>

      <p>
        Scope received:
        <strong>${tokens.scope || "not returned"}</strong>
      </p>

      <p>
        <a href="/">Back to Home</a>
      </p>
    `);
  } catch (error) {
    console.error(error);
    res.status(500).send("Authentication error.");
  }
});

// ----------------------------------------------------
// Full Auth0 Logout
// ----------------------------------------------------
app.get("/logout", (req, res) => {
  req.session.destroy((err) => {
    if (err) {
      console.error(err);
      return res.status(500).send("Logout failed.");
    }

    const returnTo = encodeURIComponent(
      `http://localhost:${PORT}`
    );

    res.redirect(
      `https://${AUTH0_DOMAIN}/v2/logout?client_id=${CLIENT_ID}&returnTo=${returnTo}`
    );
  });
});


// ====================================================
// PROJECT 2 — API AUTHORIZATION
// ====================================================

// ----------------------------------------------------
// User-level endpoint
// Requires: read:ai-data
// ----------------------------------------------------
app.get(
  "/api/chat",
  checkJwt,
  requiredScopes("read:ai-data"),
  (req, res) => {
    res.json({
      status: "success",
      message: "AI chat endpoint accessed successfully.",
      required_scope: "read:ai-data",
      granted_scope: req.auth.payload.scope,
    });
  }
);

// ----------------------------------------------------
// Admin endpoint
// Requires: write:admin
// ----------------------------------------------------
app.post(
  "/api/admin",
  checkJwt,
  requiredScopes("write:admin"),
  (req, res) => {
    res.json({
      status: "success",
      message: "Admin endpoint accessed successfully.",
      required_scope: "write:admin",
      granted_scope: req.auth.payload.scope,
    });
  }
);

// ----------------------------------------------------
// Start server
// ----------------------------------------------------
app.listen(PORT, () => {
  console.log(
    `SecureNova Auth0 app running at http://localhost:${PORT}`
  );
});