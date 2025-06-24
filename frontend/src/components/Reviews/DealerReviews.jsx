import React, { useState } from "react";
import axios from "axios";

const DealerReviews = () => {
  const [endpoint, setEndpoint] = useState("");
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  const handleFetch = () => {
    if (!endpoint) return;

    console.log("Fetching from endpoint:", endpoint);

    axios
      .get(endpoint)
      .then((res) => {
        setData(res.data);
        setError("");
        console.log("Response:", res.data);
      })
      .catch((err) => {
        setError("Error fetching data");
        setData(null);
        console.error("Fetch failed:", err);
      });
  };

  return (
    <div style={{ padding: "1rem", fontFamily: "Arial, sans-serif", color: "#000" }}>
      <h2>Dealer Endpoint Tester</h2>
      <input
        style={{
          width: "60%",
          marginRight: "10px",
          padding: "8px",
          fontSize: "1rem",
          border: "1px solid #ccc",
          borderRadius: "4px",
        }}
        value={endpoint}
        onChange={(e) => setEndpoint(e.target.value)}
        placeholder="/djangoapp/dealer/29/reviews/"
      />
      <button
        onClick={handleFetch}
        style={{
          padding: "8px 16px",
          fontSize: "1rem",
          backgroundColor: "#007bff",
          color: "#fff",
          border: "none",
          borderRadius: "4px",
          cursor: "pointer",
        }}
      >
        Fetch
      </button>

      <div style={{ marginTop: "20px" }}>
        {error ? (
          <p style={{ color: "red" }}>{error}</p>
        ) : data ? (
          <pre
            style={{
              background: "#f4f4f4",
              padding: "10px",
              color: "#000",
              fontSize: "1rem",
              borderRadius: "4px",
              overflowX: "auto",
              whiteSpace: "pre-wrap",
              wordWrap: "break-word",
            }}
          >
            {JSON.stringify(data, null, 2)}
          </pre>
        ) : (
          <p style={{ color: "#555" }}>No data returned</p>
        )}
      </div>
    </div>
  );
};

export default DealerReviews;