import React, { useEffect, useState } from "https://npm.tfl.dev/react";
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

  const [formData, setFormData] = useState({url: "", start: "", end: ""});

  function handleStartUpdate(event) {
    setFormData({url: formData.url, start: event.target.value, end: formData.end})
  }
  function handleEndUpdate(event) {
    setFormData({url: formData.url, start: formData.start, end: event.target.value})
  }
  function handleURLUpdate(event) {
    setFormData({url: event.target.value})
    fetch(
      "/api/validate?" + new URLSearchParams(
        {url: event.target.value, start: formData.start, end: formData.end}
      )
    ).then((response) => response.json()).then(
      (response) => {
        setFormData({url: response.url, start: response.start, end: response.end})
      }
  )
    console.log(formData)
  }
  function handleSubmit(event) {
    event.preventDefault();
    fetch(
      "/api/download?" + new URLSearchParams(
        {url: formData.url, start: formData.start, end: formData.end}
      )
    ).then((response) => response.json()).then(console.log)
  }

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
        <form onSubmit={handleSubmit}>
          <label for="url">Youtube video or clip URL</label> <br />
          <input type="text" id="url" name="url" placeholder="enter url" onChange={handleURLUpdate} value={formData.url} /> <br />

          <div class="row">
            <div class="column">
              <label for="start">Start time</label> <br />
              <input type="text" id="start" name="start" placeholder="0:00:00" onChange={handleStartUpdate} value={formData.start} />
            </div>
            <div class="column">
              <label for="start">End time</label> <br />
              <input type="text" id="end" name="end" placeholder="0:00:00" onChange={handleEndUpdate} value={formData.end} />
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
