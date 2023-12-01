import React from "react";
import styles from "@/styles/TextCard.module.css";

function TextCard({ children }: { children: string }) {
  return <div className={styles.card}>{children}</div>;
}

export default TextCard;
