// assets/hello.js
import React from 'react';

export function Hello({ onClick, onBlur }) {
  const handleClick = (event) => {
    const buttonName = event.target.name;
    console.log(`Button clicked: ${buttonName}`);

    if (onClick) {
      onClick(buttonName);
    }
  };

  const handleBlur = (event) => {
    const inputName = event.target.name;
    const value = event.target.value;
    console.log(`Input blurred: ${inputName} = ${value}`);

    if (onBlur) {
      onBlur({ input_name: inputName, value }); // Send a dictionary
    }
  };

  return (
    <div>
      <h1>Hello!</h1>
      <button name="exampleButton" onClick={handleClick}>
        Click Me
      </button>
      <br />
      <input
        type="text"
        name="exampleInput"
        placeholder="Type something..."
        onBlur={handleBlur}
      />
    </div>
  );
}
