import React, { useState } from "react";
import styles from "@/styles/FileSelectButton.module.css";
import UploadButton from "./UploadButton";

function FileSelectButton({ type }: { type: string }) {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState("Idle");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  return (
    <div className="innerWrapper">
      <div className="row">
        <label className="button">
          <input
            type="file"
            onChange={handleFileChange}
            className={styles.input}
          />
          <h1>Browse {type} video</h1>
        </label>

        {file && <UploadButton file={file} type={type} />}
      </div>
    </div>
  );
}

export default FileSelectButton;
