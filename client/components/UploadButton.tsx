import React, { useState } from "react";
import styles from "@/styles/UploadButton.module.css";
import TextCard from "./TextCard";

function UploadButton({ type }: { type: string }) {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState("Idle");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  async function handleUpload() {
    if (file) {
      setStatus("Uploading");

      const formData = new FormData();
      formData.append("file", file);
      formData.append("type", type);

      try {
        const res = await fetch("http://localhost:8080/upload", {
          method: "POST",
          body: formData,
        });

        const data = await res.json();
        console.log(data);
        setStatus("Success");
      } catch (err) {
        console.log(err);
        setStatus("Error");
      }
    }
  };

  return (
    <div className={styles.wrapper}>
      <div className="row">
        <label className={styles.fileSelect}>
          <input
            type="file"
            onChange={handleFileChange}
            className={styles.input}
          />
          <h1>Browse file explorer</h1>
        </label>
        <button onClick={handleUpload} className={styles.button}>
          Upload {type} video
        </button>
        <h1 className={styles.text}>{status}</h1>
      </div>
    </div>
  );
}

export default UploadButton;
