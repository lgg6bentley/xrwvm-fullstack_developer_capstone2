import React, { useEffect, useState } from "react";
import axios from "axios";
import CarCard from "./CarCard"; // Adjust the path as needed
import "./FleetList.css"; // Ensure styling is applied

const FleetList = () => {
  const [cars, setCars] = useState([]);

  // Fetch car data when component loads
  useEffect(() => {
    axios.get("http://localhost:8000/api/cars/")
      .then(res => {
        console.log("Fetched fleet:", res.data);
        setCars(res.data);
      })
      .catch(err => console.error("Error fetching fleet:", err));
  }, []);

  return (
    <div>
      <h2>Fleet Listings</h2>
      {cars.length === 0 ? (
        <p>No cars available.</p>
      ) : (
        <div className="fleet-list">
          {cars.map(car => (
            <CarCard key={car.id} car={car} />
          ))}
        </div>
      )}
    </div>
  );
};

export default FleetList;