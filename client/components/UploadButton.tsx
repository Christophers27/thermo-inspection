import React, { useState } from "react";
import styles from "@/styles/UploadButton.module.css";

function UploadButton({ file, type }: { file: File; type: string }) {
  const [status, setStatus] = useState("Idle");

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
  }

  return (
    <div className={styles.wrapper}>
      <div className={styles.info}>
        <h1>Status: {status}</h1>
        <h1>Name: {file.name}</h1>
      </div>

      <button className="button" onClick={handleUpload}>
        Upload
      </button>
    </div>
  );
}

export default UploadButton;
