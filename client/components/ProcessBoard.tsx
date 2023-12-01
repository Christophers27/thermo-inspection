import React, { useState } from "react";
import styles from "@/styles/ProcessBoard.module.css";

// The string values in the options must exactly match the names of the options
// in server/process.py
const methodOptions: { [key: string]: string[] } = {
  PCT: ["numEOFs", "normMethod"],
  SPCT: ["numEOFs", "normMethod"],
};

function ProcessBoard({ setResultPath }: { setResultPath: Function }) {
  const [method, setMethod] = useState("PCT");
  const [options, setOptions] = useState({});

  async function process() {
    const formData = new FormData();
    formData.append("method", method);
    formData.append("options", JSON.stringify(options));

    try {
      const res = await fetch("http://localhost:8080/process", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      console.log(data);
      setResultPath(data.path);
    } catch (err) {
      console.log(err);
    }
  }

  return (
    <div className={styles.wrapper}>
      <select
        onChange={(event) => setMethod(event.target.value)}
        className={styles.select}
      >
        <option value="PCT">PCT</option>
        <option value="SPCT">SPCT</option>
      </select>

      <div className={styles.options}>
        {methodOptions[method].map((option) => {
          return (
            <div key={option}>
              <label>{option}: </label>
              <input
                type="text"
                className={styles.input}
                onChange={(event) => {
                  setOptions({ ...options, [option]: event.target.value });
                }}
              />
            </div>
          );
        })}
      </div>

      <button onClick={process} className={styles.button}>
        Process
      </button>
    </div>
  );
}

export default ProcessBoard;
