import React from 'react';
import './LeafComponent.css';

const LeafComponent = ({ 
  leftContent = [], 
  rightContent = [], 
  imageSrc, 
  imageAlt = "Image",
  className = "",
  style = {}
}) => {
  return (
    <div className={`leaf-card ${className}`} style={style}>
      <div className="left-column">
        {leftContent.length > 0 ? (
          leftContent.map((item, index) => (
            <p key={index}>{item}</p>
          ))
        ) : (
          <p>-</p>
        )}
      </div>
      
      <div className="image-container">
        {imageSrc && (
          <img 
            src={imageSrc} 
            alt={imageAlt} 
            className="leaf-image"
          />
        )}
      </div>
      
      <div className="right-column">
        {rightContent.length > 0 ? (
          rightContent.map((item, index) => (
            <p key={index}>{item}</p>
          ))
        ) : (
          <p>-</p>
        )}
      </div>
    </div>
  );
};

export default LeafComponent;
