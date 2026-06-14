// ============================================================
// InsureVoice — Firebase Configuration
// ============================================================

const firebaseConfig = {
  apiKey:            "AIzaSyCJAM9Kou71jbVij8jzw023PLJ5h7L0rPo",
  authDomain:        "insurevoice.firebaseapp.com",
  projectId:         "insurevoice",
  messagingSenderId: "387084589751",
  appId:             "1:387084589751:web:9ecab1df8f62a619e58b32"
};

firebase.initializeApp(firebaseConfig);

const auth = firebase.auth();
const db   = firebase.firestore();

// FIX: Removed enablePersistence() entirely
// It caused "failed-precondition" errors when multiple tabs were open
// and "Loading profile..." stuck forever because it blocked Firestore queries
// Firestore works perfectly without it for a local/hosted project
