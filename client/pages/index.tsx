import React, { useState } from "react";
import TextCard from "@/components/TextCard";
import ImageCard from "@/components/ImageCard";
import FileSelectButton from "@/components/FileSelectButton";
import ProcessBoard from "@/components/ProcessBoard";

function Home() {
  const [resultPath, setResultPath] = useState("");

  return (
    <div className="wrapper">
      <TextCard>AirLab Thermographic Inspection Tool</TextCard>
      <div className="row">
        <div className="column">
          <FileSelectButton type="cold" />
          <FileSelectButton type="hot" />
          <ProcessBoard setResultPath={setResultPath} />
        </div>
        <ImageCard path={resultPath} />
      </div>
    </div>
  );
}

export default Home;
