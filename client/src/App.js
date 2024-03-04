import React from "react";
import "./App.css";
import axios from "axios";
import { useState } from "react";
import search_icon from "./Assets/search.png";

function App() {
  const [city, setCity] = useState("");
  const [surl, setSurl] = useState("");
  const [siconUrl, setSiconUrl] = useState("");
  const [title, setTitle] = useState("");
  const [wicon, setWicon] = useState("");
  const [wtitle, setWtitle] = useState("");
  const [temp, setTemp] = useState("");

  async function fetchPlaylist(city) {
    return await axios.get(`http://127.0.0.1:5000/get-weather/${city}`);
  }

  const onSubmit = async (e) => {
    e.preventDefault();
    try {
      const { data } = await fetchPlaylist(city);
      const kelvinTemperature = data.response.main.temp;
      const celsiusTemperature = kelvinTemperature - 273.15;
      setWicon(
        `https://openweathermap.org/img/wn/${data.response.weather[0].icon}@2x.png`
      );
      setTemp(celsiusTemperature.toFixed(0) + "°C");
      setWtitle(data.response.name);
      setSurl(data.playlists[0].external_urls.spotify);
      setTitle(data.playlists[0].name);
      setSiconUrl(data.playlists[0].images[0].url);
    } catch (err) {
      console.error(err.message);
    }
  };

  return (
    <div className="App">
      <h1>Sky Listener</h1>
      <form onSubmit={onSubmit} className="form">
        <input
          type="text"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          className="searchinput"
          placeholder="Search a City"
        ></input>
        <button type="submit" className="searchbutton">
          <img src={search_icon}></img>
        </button>
      </form>
      <div className="mainbody">
        <div className="wdiv">
          <img src={wicon} className="wicon"></img>
          <div className="temp">{temp}</div>
          <div className="city">{wtitle}</div>
        </div>
        <div className="sdiv">
          <div className="playlisttitle">{title}</div>
          <div>
            <img src={siconUrl} alt="Playlist Icon" className="playlistimage" />
          </div>
          <div>
            <a href={surl} className="playlistlink">{surl}</a>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
