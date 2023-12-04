import React, { useState } from "react";
import styles from "@/styles/ProcessBoard.module.css";

// The string values in the options must exactly match the names of the options
// in server/process.py
type MethodOptions = {
  [key: string]: {
    numEOFs: number[];
    normMethod: string[];
  };
};

const methodOptions: MethodOptions = {
  PCT: {
    numEOFs: [1, 2, 3, 4, 5, 6],
    normMethod: [
      "col-wise standardize",
      "row-wise standardize",
      "mean reduction",
    ],
  },
  SPCT: {
    numEOFs: [1, 2, 3, 4, 5, 6],
    normMethod: [
      "col-wise standardize",
      "row-wise standardize",
      "mean reduction",
      "col-wise mean reduction",
    ]
  }
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
        {Object.keys(methodOptions[method]).map((option) => {
          return (
            <div key={option} className={styles.optionRow}>
              <p className={styles.optionName}>{option}: </p>
              <select
                onChange={(event) =>
                  setOptions((prev) => ({
                    ...prev,
                    [option]: event.target.value,
                  }))
                }
                className={styles.select}
              >
                {methodOptions[method][option].map((value) => (
                  <option key={value} value={value}>
                    {value}
                  </option>
                ))}
              </select>
            </div>
          )
        })}
      </div>

      <button onClick={process} className="button rightAlign">
        Process
      </button>
    </div>
  );
}

export default ProcessBoard;
