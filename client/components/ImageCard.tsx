import React from "react";
import styles from "@/styles/ImageCard.module.css";
import TextCard from "./TextCard";

function ImageCard({ path, status }: { path: string; status: boolean }) {
  const download = (fileName, content) => {
    var element = document.createElement("a");
    element.setAttribute("href", content);
    element.setAttribute("download", fileName);
    element.style.display = "none";
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
  };

  const handleDownload = async (e) => {
    try {
      const result = await fetch(path, {
        method: "GET",
        headers: {},
      });

      const blob = await result.blob();
      const url = URL.createObjectURL(blob);
      download("result.png", url);

      URL.revokeObjectURL(url);
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div className={styles.container}>
      {status ? (
        <p>Processing ...</p>
      ) : (
        <div>
          <TextCard>Image Viewer</TextCard>
          <img
            src={path}
            alt="Image will appear here"
            className={styles.image}
          />
          <button onClick={handleDownload} type="button" className="button">
            Download
          </button>
        </div>
      )}
    </div>
  );
}

export default ImageCard;
