import React, { useState } from "react";
import TextCard from "@/components/TextCard";
import UploadButton from "@/components/UploadButton";
import ProcessBoard from "@/components/ProcessBoard";

function Home() {
  const [resultPath, setResultPath] = useState("");

  return (
    <div className="wrapper">
      <TextCard>AirLab Thermographic Inspection Tool</TextCard>
      <div className="row">
        <div className="column">
          <UploadButton type="cold" />
          <UploadButton type="hot" />
          <ProcessBoard setResultPath={setResultPath} />
        </div>
        <div className="column">
          <img
            src={resultPath}
            alt="Image will appear here"
            className="image"
          />
        </div>
      </div>
    </div>
  );
}

export default Home;
