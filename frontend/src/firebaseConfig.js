import { initializeApp } from "firebase/app";

const firebaseConfig = {
  apiKey: "AIzaSyCEtQNM70XnhlSrWgdR830UF--AjQewnKg",
  authDomain: "media-platform-e02fa.firebaseapp.com",
  projectId: "media-platform-e02fa",
  storageBucket: "media-platform-e02fa.appspot.com",
  messagingSenderId: "66321336393",
  appId: "1:66321336393:web:REPLACE_WITH_ACTUAL_APP_ID"
};

const firebaseApp = initializeApp(firebaseConfig);

export default firebaseApp;
