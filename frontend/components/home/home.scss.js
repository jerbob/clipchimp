import scss from "https://tfl.dev/@truffle/utils@~0.0.3/css/css.ts";

export default scss`
.error-field {
  border: 2px solid #F34444 !important;
}

.error-message {
  top: -1.5rem;
  position: relative;
  font-family: 'Inter';
  font-size: 0.8rem;
  color: #F34444;
  bottom: 0;
  margin-bottom: -1.4rem;
}

.hidden {
  display: none !important;
}

.loader {
  border: 0.5rem solid #FFC7DB; /* Light grey */
  border-top: 0.5rem solid #F8669B; /* Blue */
  border-radius: 50%;
  width: 4rem;
  height: 4rem;
  animation: spin 2s linear infinite;
  opacity: 1 !important;
  float: right;
  position: absolute;
  z-index: 999;
  left: 48vw;
  top: 32rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-form > * {
  opacity: 0.4;
}

.c-home {
  display: block;
  margin-left: 34vw;
  margin-right: 34vw;
  margin-top: 2.2rem;
}

.c-home > * {
  display: block;
  margin-left: auto;
  margin-right: auto;
}

.header {
  font-family: 'Alfa Slab One', cursive;
  color: #363636;
  font-size: 3rem;
  text-align: center;
  margin-top: 9.7rem;
  margin-bottom: 1.8rem;
}

.form-container {
  background: #FFFFFF;
  border: 3px solid #000000;
  border-radius: 0.9rem;
  padding-left: 2rem;
  padding-right: 2rem;
  padding-top: 0.3rem;
  padding-bottom: 1.5rem;
  margin-bottom: 0.2rem;
}

.form-title {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 800;
  color: #363636;
  font-size: 1.75rem;
  margin-bottom: 1.5rem;
}

#url, #start, #end, #download, #download-link {
  width: 100%;
  margin-bottom: 2rem;
  font-family: 'Inter';
  font-style: normal;
  font-weight: 400;
  font-size: 1.1rem;
  letter-spacing: 0.005em;
  border: none;
  background: #F2F2F2;
  padding: 0.8rem;
  border-radius: 0.3rem;
  outline: none !important;
  text-decoration: none;
}

#url {
  margin-bottom: 1.2rem;
  margin-top: 0.2rem;
}

#url, #start, #end {
  width: calc(100% - 1.6rem);
}

#start, #end {
  margin-top: 0.2rem;
  margin-bottom: 1.2rem;
}

#start {
  width: calc(100% - 2.6rem)
}

.logomark {
  width: 2rem;
  float: right;
  margin-top: 0.5rem;
  margin-right: 0.3rem;
}

#download, #download-link {
  background-image: linear-gradient(90.73deg, #EEB467 2.74%, #F8639C 100%);
  font-family: 'Inter';
  font-style: normal;
  font-weight: 700;
  color: #363636;
  font-size: 1rem;
  margin-bottom: 0.2rem;
  margin-top: 1rem;
}

a {
  text-underline-offset: 3px;
}

a:link {
  color: #F357A1;
}

a.personal-link {
  color: #363636 !important;
  text-decoration-style: dashed !important;
}

a:visited {
  color: #F357A1;
}

a:hover {
  color: #F357A1;
}

a:active {
  color: #F357A1;
}

#credits-container {
  width:40%;
}

::placeholder {
  color: rgba(54, 54, 54, 0.4);
  opacity: 1;
}

.column {
  float: left;
  width: 50%;
}

.credits {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 600;
  color: #363636;
  position: relative;
}

label {
  display: inline-block;
  margin-bottom: 0.3rem;
  font-family: 'Inter';
  font-style: normal;
  font-weight: 500;
  line-height: 20px;
  letter-spacing: 0.0025em;
  font-size: 0.85rem;
  color: #363636;
}

.row:after {
  content: "";
  display: table;
  clear: both;
}

.modal {
  position: fixed; /* Stay in place */
  z-index: 1; /* Sit on top */
  padding-top: 100px; /* Location of the box */
  left: 0;
  top: 0;
  width: 100%; /* Full width */
  height: 100%; /* Full height */
  overflow: auto; /* Enable scroll if needed */
  background-color: rgb(0,0,0); /* Fallback color */
  background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
}

/* Modal Content */
.modal-content {
  background-color: #fefefe;
  margin: auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
}

/* The Close Button */
.close {
  color: #aaaaaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: #000;
  text-decoration: none;
  cursor: pointer;
}`
