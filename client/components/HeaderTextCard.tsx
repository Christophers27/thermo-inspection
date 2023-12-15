import React from "react";
import styles from "@/styles/HeaderTextCard.module.css"

function HeaderTextCard({ children }: { children: string }) {
  return <div className={styles.card}>{children}</div>;
}

export default HeaderTextCard;
