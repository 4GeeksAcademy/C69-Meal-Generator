import React from 'react';

const ToggleSwitch = ({ isOn, onToggle }) => {
  return (
    <label className="toggle-switch">
      <input type="checkbox" checked={isOn} onChange={onToggle} />
      <span className="slider">
        <span className="on">YES</span>
        <span className="off">NO</span>
      </span>
    </label>
  );
};

export default ToggleSwitch;