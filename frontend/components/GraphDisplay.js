"use client";

import { useRef, useEffect } from "react";

export default function GraphDisplay({ graphHtml }) {
  const containerRef = useRef(null);

  useEffect(() => {
    const loadPlotly = () => {
      return new Promise((resolve, reject) => {
        if (window.Plotly) {
          resolve();
        } else {
          const script = document.createElement("script");
          script.src = "https://cdn.plot.ly/plotly-3.0.1.min.js";
          script.onload = resolve;
          script.onerror = reject;
          document.head.appendChild(script);
        }
      });
    };

    loadPlotly().then(() => {
      if (containerRef.current) {
        // Inject the HTML content into the container
        containerRef.current.innerHTML = graphHtml;

        // Re-inject and execute any embedded scripts.
        // For external Plotly scripts, skip reloading since Plotly is already loaded.
        // For inline scripts, execute them using eval in a setTimeout.
        const scripts = containerRef.current.getElementsByTagName("script");
        const scriptsArr = Array.from(scripts);
        scriptsArr.forEach(oldScript => {
          if (oldScript.src) {
            if (oldScript.src.indexOf("plot.ly/plotly") !== -1) {
              // Skip reloading Plotly external script.
              return;
            }
            const newScript = document.createElement("script");
            newScript.type = oldScript.type || "text/javascript";
            newScript.src = oldScript.src;
            oldScript.parentNode.replaceChild(newScript, oldScript);
          } else {
            // Execute inline script after a short delay to ensure Plotly is available.
            setTimeout(() => {
              try {
                new Function(oldScript.innerHTML)();
              } catch (error) {
                console.error("Error executing inline script:", error);
              }
            }, 100);
            oldScript.parentNode.removeChild(oldScript);
          }
        });
      }
    }).catch(err => {
      console.error("Failed to load Plotly:", err);
    });
  }, [graphHtml]);

  return <div ref={containerRef} />;
}
