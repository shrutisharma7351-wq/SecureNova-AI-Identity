const express = require("express");
const session = require("express-session");
const crypto = require("crypto");
require("dotenv").config();

const app = express();
const PORT = 3001;

// ----------------------------------------------------
// Auth0 configuration
// ----------------------------------------------------
const AUTH0_DOMAIN = process.env.AUTH0_DOMAIN;
const SSO_CLIENT_ID = process.env.SSO_CLIENT_ID;
const SSO_CLIENT_SECRET = process.env.SSO_CLIENT_SECRET;

// ----------------------------------------------------
// Session
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

// ----------------------------------------------------
// Home page
// ----------------------------------------------------
app.get("/", (req, res) => {
  const isLoggedIn = !!req.session.user;

  res.send(`
    <h1>SecureNova AI - SSO Client</h1>

    <p>Auth0 Single Sign-On Demonstration</p>

    ${
      isLoggedIn
        ? `
          <p><strong>Authenticated via Auth0 SSO ✅</strong></p>
          <p>User: ${req.session.user.email || "Authenticated User"}</p>
          <p>
            This is Client 2.
            No new username/password login was required.
          </p>
          <a href="/logout">Logout</a>
        `
        : `
          <a href="/login">Login with Auth0</a>
        `
    }
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

  // Store PKCE values for callback
  req.session.oauthState = state;
  req.session.codeVerifier = codeVerifier;

  const params = new URLSearchParams({
    response_type: "code",
    client_id: SSO_CLIENT_ID,
    redirect_uri: `http://localhost:${PORT}/callback`,

    // Basic OpenID scopes for SSO
    scope: "openid profile email",

    state: state,
    code_challenge: codeChallenge,
    code_challenge_method: "S256",

    // IMPORTANT:
    // No prompt=login here.
    // Auth0 can therefore reuse the existing SSO session.
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
          client_id: SSO_CLIENT_ID,
          client_secret: SSO_CLIENT_SECRET,
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
        <h2>SSO Token Exchange Failed</h2>
        <pre>${JSON.stringify(tokens, null, 2)}</pre>
      `);
    }

    // Remove temporary PKCE values
    delete req.session.oauthState;
    delete req.session.codeVerifier;

    // Store tokens
    req.session.tokens = tokens;

    // Decode ID token payload just for displaying user info.
    // This is only for this local demonstration.
    let user = {};

    if (tokens.id_token) {
      try {
        const payload = tokens.id_token.split(".")[1];

        const decoded = JSON.parse(
          Buffer.from(payload, "base64url").toString("utf8")
        );

        user = decoded;
      } catch (error) {
        console.error("Could not decode ID token:", error);
      }
    }

    req.session.user = user;

    res.redirect("/");
  } catch (error) {
    console.error(error);
    res.status(500).send("Authentication error.");
  }
});

// ----------------------------------------------------
// Logout Client 2
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
      `https://${AUTH0_DOMAIN}/v2/logout?client_id=${SSO_CLIENT_ID}&returnTo=${returnTo}`
    );
  });
});

// ----------------------------------------------------
// Start server
// ----------------------------------------------------
app.listen(PORT, () => {
  console.log(
    `SecureNova SSO Client running at http://localhost:${PORT}`
  );
});