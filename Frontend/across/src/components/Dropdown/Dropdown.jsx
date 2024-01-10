import React, { useState } from "react";
import { FaAngleDown } from "react-icons/fa6";
import "./Dropdown.css";

const Dropdown = ({ options, value, onChange }) => {
  const [isOpen, setIsOpen] = useState(false);

  const handleClick = () => {
    setIsOpen(currentIsOpen => !currentIsOpen);
  };

  const handleColorClick = option => {
    setIsOpen(false);
    onChange(option);
  };

  const renderedOptions = options.map(option => {
    return (
      <div
        className="renderedOptions"
        onClick={() => handleColorClick(option)}
        key={option.value}
      >
        {option.label}
      </div>
    );
  });

  return (
    <div className="dropdownWrapper">
      <div className="dropdown__options" onClick={handleClick}>
        {value?.label || "Select ..."}
        <FaAngleDown style={{ fontSize: "1.125rem", lineHeight: "1.75rem" }} />
      </div>
      {isOpen && (
        <div className="dropdown__open-options">{renderedOptions}</div>
      )}
    </div>
  );
};

export default Dropdown;
