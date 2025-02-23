import React from "react"; // ✅ Ensure React is imported
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Form from "./pages/form"; // ✅ Ensure correct import path
import "./App.css";
import logo from "./logo.svg"; // ✅ This import is unnecessary unless used

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Form />} />
      </Routes>
    </Router>
  );
}

export default App;
