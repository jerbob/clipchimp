import React, { useState } from "https://npm.tfl.dev/react";
import Helmet from "https://npm.tfl.dev/react-helmet@6.1.0";
import { useStyleSheet } from "https://tfl.dev/@truffle/distribute@^2.0.5/format/wc/react/index.ts";

import styleSheet from "./home.scss.js";

function ExtensionMapping() {
  useStyleSheet(styleSheet);

  const [formData, setFormData] = useState({
    url: {error: false, message: "", value: ""},
    start: {error: false, message: "", value: ""},
    end: {error: false, message: "", value: ""}
  })
  const [formStatus, setFormStatus] = useState({loading: false, download: ""});

  function handleStartUpdate(event) {
    setFormData({
      url: formData.url,
      start: {
        error: formData.start.error,
        message: formData.start.message,
        value: event.target.value
      },
      end: formData.end
    })
  }

  function handleEndUpdate(event) {
    setFormData({
      url: formData.url,
      start: formData.start,
      end: {
        error: formData.end.error,
        message: formData.end.message,
        value: event.target.value
      }
    })
  }

  function handleURLUpdate(event) {
    setFormData({
      url: {
        error: formData.url.error,
        message: formData.url.message,
        value: event.target.value
      },
      start: formData.start,
      end: formData.end
    })
    fetch(
      "https://jerbob-clips-backend.sporocarp.dev/api/validate?" + new URLSearchParams(
        {url: event.target.value, start: formData.start.value, end: formData.end.value}
      )
    ).then((response) => response.json()).then(
      (response) => {
        setFormData(response);
      }
    )
  }

  function handleSubmit(event) {
    event.preventDefault();
    fetch(
      "https://jerbob-clips-backend.sporocarp.dev/api/download?" + new URLSearchParams(
        {url: formData.url.value, start: formData.start.value, end: formData.end.value}
      )
    ).then((response) => response.json()).then((downloadTask) => {
      if (downloadTask.status == "PENDING" || downloadTask.status == "SUCCESS") {
        setFormStatus({loading: true, download: ""});
        window.loading = true;
        setInterval(
          () => {
            if (!window.loading) {
              return
            }
            fetch(
              "https://jerbob-clips-backend.sporocarp.dev/api/status?" + new URLSearchParams(
                {task: downloadTask.id}
              )
            ).then((response) => response.json()).then((downloadStatus) => {
              if (downloadStatus.status == "SUCCESS") {
                setFormStatus({loading: false, download: downloadStatus.download})
                window.loading = false;
              }
            })
          }, 1000)
        }
      })
  }

  return (
    <div className="c-home">
      <Helmet>
        <title>Clip Downloader</title>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
        <link href="https://fonts.googleapis.com/css2?family=Alfa+Slab+One&family=Inter:wght@400;500;600;800&display=swap" rel="stylesheet" />
      </Helmet>

      <div id="myModal" class="modal" className={`modal${formStatus.download ? "": " hidden"}`}>
        <div class="modal-content">
          <a id="download-link" href={`${formStatus.download}`} download="clip.webm">Save clip</a>
        </div>
      </div>

      <img src="/clip_downloader_logo.svg" />
      <p class="header">Download Youtube <br/>video clips</p>

      <div class="form-container" className={`form-container${formStatus.loading ? " loading-form": ""}`}>
        <div className={`loader${formStatus.loading ? "": " hidden"}`}></div>
        <p class="form-title">Create your clip</p>
        <form onSubmit={handleSubmit}>
          <label for="url">Youtube video or clip URL</label> <br />
          <input
            type="text" id="url" name="url" placeholder="enter url"
            onChange={handleURLUpdate} value={formData.url.value}
            className={`${formData.url.error ? "error-field": ""}`}
          />
          <p class="error-message">{formData.url.message}</p>
          <br />

          <div class="row">
            <div class="column">
              <label for="start">Start time</label> <br />
              <input
                type="text" id="start" name="start" placeholder="0:00:00"
                onChange={handleStartUpdate} value={formData.start.value}
                className={`${formData.start.error ? "error-field": ""}`}
              />
              <p class="error-message">{formData.start.message}</p>
            </div>
            <div class="column">
              <label for="start">End time</label> <br />
              <input
                type="text" id="end" name="end" placeholder="0:00:00"
                onChange={handleEndUpdate} value={formData.end.value}
                className={`${formData.end.error ? "error-field": ""}`}
              />
              <p class="error-message">{formData.end.message}</p>
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
