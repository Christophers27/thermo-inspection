import React, { useState } from "react";
import styles from "@/styles/ProcessBoard.module.css";

import TextCard from "./TextCard";

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
    numEOFs: [2, 4, 6],
    normMethod: [
      "col-wise standardize",
      "row-wise standardize",
      "mean reduction",
    ],
  },
  SPCT: {
    numEOFs: [2, 4, 6],
    normMethod: [
      "col-wise standardize",
      "row-wise standardize",
      "mean reduction",
      "col-wise mean reduction",
    ],
  },
};

function ProcessBoard({ setResultPath }: { setResultPath: Function }) {
  const [method, setMethod] = useState("PCT");
  const [options, setOptions] = useState({});

  async function process() {
    setResultPath("");

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

  function readJSON(event: React.ChangeEvent<HTMLInputElement>) {
    if (!event.target.files) {
      console.log("No valid file selected");
      return;
    } else {
      const file = event.target.files[0];
      const reader = new FileReader();
      reader.readAsText(file, "UTF-8");
      reader.onload = (event) => {
        if (event.target) {
          const result = JSON.parse(event.target.result as string);

          setMethod(result.method);
          setOptions(result.options);

          console.log(event.target.result);
        }
      };
      reader.onerror = (event) => {
        console.log("Error reading file: ", event.target?.error);
      };
    }
  }

  return (
    <div className={styles.outerWrapper}>
      <TextCard>Select Method</TextCard>
      <div className={styles.innerWrapper}>
        <select
          onChange={(event) => setMethod(event.target.value)}
          className={styles.select}
        >
          <option value="PCT">PCT</option>
          <option value="SPCT">SPCT</option>
          <option value="import JSON">Import JSON</option>
        </select>
        <div className={styles.options}>
          {method != "import JSON" &&
            Object.keys(methodOptions[method]).map((option) => {
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
              );
            })}
          {method === "import JSON" && <input type="file" accept=".json" onChange={readJSON} />}
        </div>
        <button onClick={process} className="button rightAlign">
          Process
        </button>
      </div>
    </div>
  );
}

export default ProcessBoard;
