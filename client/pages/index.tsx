import React, { useState } from "react";
import TextCard from "@/components/TextCard";
import ImageCard from "@/components/ImageCard";
import FileSelectButton from "@/components/FileSelectButton";
import ProcessBoard from "@/components/ProcessBoard";
import HeaderTextCard from "@/components/HeaderTextCard";

function Home() {
  const [resultPath, setResultPath] = useState("");
  const [status, setStatus] = useState(false)

  return (
    <div className="wrapper">
      <HeaderTextCard>AirLab Thermographic Inspection Tool</HeaderTextCard>
      <div className="row">
        <div className="column">
          <FileSelectButton type="cold" />
          <FileSelectButton type="hot" />
          <ProcessBoard setResultPath={setResultPath} setStatus={setStatus} />
        </div>
        <ImageCard path={resultPath} status={status} />
      </div>
    </div>
  );
}

export default Home;
