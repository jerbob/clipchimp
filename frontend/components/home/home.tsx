import React, { useEffect } from "https://npm.tfl.dev/react";
import Helmet from "https://npm.tfl.dev/react-helmet@6.1.0";
import jumper from "https://tfl.dev/@truffle/utils@~0.0.2/jumper/jumper.ts";
import { useStyleSheet } from "https://tfl.dev/@truffle/distribute@^2.0.5/format/wc/react/index.ts";

import styleSheet from "./home.scss.js";

function ExtensionMapping() {
  useStyleSheet(styleSheet);

  useEffect(() => {
    const style = {
      width: "400px",
      height: "400px",
      background: "#fff",
      position: "fixed",
      bottom: 0,
      "z-index": "999",
    };
    // set styles for this iframe within YouTube's site
    jumper.call("layout.applyLayoutConfigSteps", {
      layoutConfigSteps: [
        { action: "useSubject" }, // start with our iframe
        { action: "setStyle", value: style },
      ],
    });
  }, []);

  return (
    <div className="c-home">
      <Helmet>
        <title>Clip Downloader</title>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
        <link href="https://fonts.googleapis.com/css2?family=Alfa+Slab+One&family=Inter:wght@400;500;600;800&display=swap" rel="stylesheet" />
      </Helmet>
      <img src="/clip_downloader_logo.svg" />
      <p class="header">Download Youtube <br/>video clips</p>
      <div class="form-container">
        <p class="form-title">Create your clip</p>
        <form action="/api/queue-download">
          <label for="url">Youtube video URL</label> <br />
          <input type="text" id="url" name="url" placeholder="enter url" /> <br />

          <div class="row">
            <div class="column">
              <label for="start">Start time</label> <br />
              <input type="text" id="start" name="start" placeholder="00:00:00" />
            </div>
            <div class="column">
              <label for="start">End time</label> <br />
              <input type="text" id="end" name="end" placeholder="00:00:00" />
            </div>
          </div>
          <input type="submit" value="Download clip" id="download" />
        </form>
      </div>

      <div class="row">
        <div class="column" id="credits-container">
          <img class="logomark" src="/logomark.svg" />
        </div>
        <div class="column">
          <p class="credits">Powered by <a href="https://truffle.vip">Truffle</a></p>
        </div>
      </div>
    </div>
  );
}

export default ExtensionMapping;
