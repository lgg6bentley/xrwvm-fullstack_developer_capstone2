import React from "react";
import "./CarCard.css";

const CarCard = ({ car }) => {
  return (
    <div className="car-card">
      <img src={car.image_url} alt={`${car.make} ${car.model}`} />
      <div className="car-info">
        <h2>{car.make} {car.model}</h2>
        <p><strong>Type:</strong> {car.type}</p>
        <p><strong>Year:</strong> {car.year}</p>
      </div>
    </div>
  );
};

export default CarCard;