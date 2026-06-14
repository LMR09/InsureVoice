// ============================================================
// InsureVoice — Auth Helper  (FINAL FIX v2)
// - Event delegation for logout/avatar (fixes innerHTML onclick issue)
// - Self-healing: auto-creates missing users/{uid} doc on every load
// ============================================================

// ── Single delegated listener on the whole page ──
document.addEventListener('click', function (e) {

  if (e.target.closest('#logoutBtn')) {
    e.preventDefault();
    auth.signOut().then(() => {
      window.location.href = 'index.html';
    }).catch(err => console.error('Logout error:', err));
  }

  if (e.target.closest('#avatarBtn')) {
    window.location.href = 'profile.html';
  }

});

// ── Update navbar whenever auth state changes ──
auth.onAuthStateChanged((user) => {
  updateNavbar(user);
  if (user) ensureUserDoc(user);   // self-heal missing Firestore doc
});

function updateNavbar(user) {
  const navActions = document.getElementById('navActions');
  if (!navActions) return;

  if (user) {
    const initial = (user.displayName || user.email || 'U')[0].toUpperCase();
    const name    = user.displayName || user.email.split('@')[0];

    navActions.innerHTML = `
      <a href="review.html" class="btn btn-primary btn-sm">+ Write Review</a>
      <div style="display:flex;align-items:center;gap:10px;">
        <div id="avatarBtn"
             class="avatar-sm"
             title="Go to Profile (${user.email})"
             style="cursor:pointer;">${initial}</div>
        <a href="profile.html"
           style="color:var(--slate-light);font-size:0.88rem;font-weight:500;text-decoration:none;">
          ${name}
        </a>
        <button id="logoutBtn" class="btn btn-outline btn-sm">Logout</button>
      </div>`;

  } else {
    navActions.innerHTML = `
      <a href="login.html"  class="btn btn-outline btn-sm">Login</a>
      <a href="signup.html" class="btn btn-primary btn-sm">Sign Up</a>`;
  }
}

// ── Self-healing: ensure users/{uid} Firestore doc exists ──
// Runs on every page load for logged-in users.
// If the doc is missing (e.g. signup partially failed, or account
// was created via a different flow), it creates it WITHOUT touching
// createdAt/reviewCount if it already exists.
async function ensureUserDoc(user) {
  try {
    const ref  = db.collection('users').doc(user.uid);
    const snap = await ref.get();
    if (!snap.exists) {
      await ref.set({
        uid:         user.uid,
        name:        user.displayName || '',
        email:       user.email,
        createdAt:   firebase.firestore.FieldValue.serverTimestamp(),
        reviewCount: 0,
      });
      console.log('Created missing user profile document for', user.uid);
    }
  } catch (err) {
    console.error('ensureUserDoc error:', err);
  }
}

// ── Auth guard — redirect to login if not authenticated ──
function requireAuth() {
  return new Promise((resolve, reject) => {
    const unsub = auth.onAuthStateChanged((user) => {
      unsub();
      if (user) {
        resolve(user);
      } else {
        window.location.href = 'login.html?redirect='
          + encodeURIComponent(window.location.pathname);
        reject('Not authenticated');
      }
    });
  });
}

// ── Get Firestore user profile document ──
async function getUserProfile(uid) {
  try {
    const doc = await db.collection('users').doc(uid).get();
    return doc.exists ? doc.data() : null;
  } catch (err) {
    console.error('getUserProfile error:', err);
    return null;
  }
}

// ── logoutUser kept as named function (called from profile.html) ──
async function logoutUser() {
  try {
    await auth.signOut();
    window.location.href = 'index.html';
  } catch (err) {
    console.error('Logout error:', err);
  }
}
